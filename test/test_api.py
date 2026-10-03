"""Library API: text in, data out, exceptions on failure."""

import itertools
import json
import os
import re
import subprocess
import sys
import textwrap
from typing import ClassVar

import pytest

from petit import (
    IDENTIFIER,
    DataFileError,
    EmptyLogError,
    LogHash,
    ParseError,
    PetitError,
    analyze_lines,
    analyze_text,
    detect_format,
    hash_lines,
    hash_text,
    pull_identifiers,
    resources,
)
from petit.CrunchLog import CrunchLog
from petit.Filter import Filter
from petit.LogHash import SuperHash


def secure_log(lines=200, pids=(1234, 5678)):
    """Realistic sshd output: a few PIDs across many lines.

    Deliberately not one PID per line — petit keys on the daemon field, which
    includes the PID, so a log with a unique PID per line cannot group and
    would make this suite pass for the wrong reason.
    """
    return "\n".join(
        f"Aug 18 10:{i % 60:02d}:{i % 60:02d} host01 sshd[{pids[i % len(pids)]}]: "
        f"Accepted publickey for scott from 10.0.0.{i % 250} port {3000 + i}"
        for i in range(lines)
    )


class TestDetection:
    def test_picks_a_driver_for_secure_logs(self):
        assert detect_format(secure_log()) == "SecureLogEntry"

    def test_unrecognised_text_falls_back_to_raw(self):
        prose = "\n".join("the quick brown fox jumps over it" for _ in range(30))
        assert detect_format(prose) == "RawEntry"


class TestHashText:
    def test_collapses_repetitive_lines(self):
        groups = hash_text(secure_log())
        assert len(groups) < 10
        assert sum(g.count for g in groups) == 200

    def test_sorted_by_descending_count(self):
        counts = [g.count for g in hash_text(secure_log())]
        assert counts == sorted(counts, reverse=True)

    def test_samples_are_the_original_lines(self):
        """Samples must be exactly what was in the input.

        They used to be rebuilt from parsed fields, and SecureLogHash had
        already overwritten the payload in place, so the caller got
        "Accepted publickey for #" — the user and source address, the only
        reason to look at a sample, were gone.
        """
        text = secure_log()
        top = hash_text(text)[0]
        assert top.samples
        sample = top.samples[0]
        assert "object at 0x" not in sample
        assert sample in text.splitlines()
        assert "Accepted publickey for scott" in sample

    def test_max_samples_is_honoured(self):
        top = hash_text(secure_log(), max_samples=1)[0]
        assert len(top.samples) == 1


class TestFailureModes:
    def test_empty_input_raises_instead_of_exiting(self):
        """The whole point of the library API: a bad payload must not take
        the caller's process down with it."""
        with pytest.raises(EmptyLogError):
            hash_text("")

    def test_hostile_input_does_not_escape_as_systemexit(self):
        for payload in ("\x00\x00\x00", "[" * 5000, "\n" * 100):
            try:
                hash_text(payload)
            except SystemExit:  # pragma: no cover - the regression guard
                pytest.fail("library raised SystemExit on hostile input")
            except Exception:
                pass


class TestPackagedData:
    def test_stopword_files_ship_with_the_package(self):
        """These used to live only in /var/lib/petit, so a pip install had no
        data at all and filtering silently did nothing."""
        assert resources.find("filters", "hash.stopwords") is not None

    def test_legacy_system_paths_are_still_searched_last(self):
        prefixes = resources.search_prefixes("fingerprints")
        assert "/var/lib/petit/fingerprints/" in prefixes
        assert prefixes[0] != "/var/lib/petit/fingerprints/"

    def test_opt_prefix_is_a_separate_entry(self):
        """Regression: the old list was missing a comma, so two paths were
        concatenated into one and /opt was never actually searched."""
        prefixes = resources.search_prefixes("fingerprints")
        assert "/opt/petit/var/lib/fingerprints/" in prefixes


class TestWordStopwords:
    """words.stopwords drops whole words; it used to cut them out of others."""

    FILTER = Filter("words.stopwords")

    def test_every_listed_word_is_stopped(self):
        path = resources.find("filters", "words.stopwords")
        with open(path) as f:
            words = re.findall(r"\^\[\^\\w#\]\*(\w+)\[\^\\w#\]\*\$", f.read())
        assert len(words) > 150
        assert [w for w in words if not self.FILTER.bleach(w)] == []

    @pytest.mark.parametrize("word", ["I", "The", "there.", "___", "Stopped", "(of)", "--",
                                      "addr=?",
                                      "5e307723-75a3-4ee9-912d-a813e8cfe18f"])
    def test_stopped(self, word):
        assert self.FILTER.bleach(word)

    @pytest.mark.parametrize("word", ["target.service", "command", "unreachable:", "ACPI",
                                      "NVMe", "thermal", "shutdown", "i#", "a#"])
    def test_kept_whole(self, word):
        assert self.FILTER.scrub(word) == word


class TestDaemonStopwords:
    """Classic syslog pseudo-daemons are dropped only as the whole field."""

    FILTER = Filter("daemon.stopwords")

    @pytest.mark.parametrize("field", ["last", "--", "exiting", "ISO"])
    def test_pseudo_daemon_is_dropped(self, field):
        assert self.FILTER.bleach(field)

    @pytest.mark.parametrize(("field", "key"), [
        ("lastlog[12]:", "lastlog[#]:"),
        ("exiting-helper:", "exiting-helper:"),
        ("ISOmount[3]:", "ISOmount[#]:"),
        ("dm--event[4]:", "dm--event[#]:"),
    ])
    def test_longer_field_is_kept(self, field, key):
        assert self.FILTER.scrub(field) == key


class TestFileErrors:
    """Issue #16: an unreadable or missing file used to escape as a raw
    traceback. Reported by Pablo Iranzo Gomez in 2022; PR #17 proposed an
    os.access() check and was closed unmerged, so it stayed broken."""

    def test_unreadable_file_raises_cleanly(self, tmp_path):
        target = tmp_path / "noperm.log"
        target.write_text("Aug 18 10:00:00 host sshd[1]: test\n")
        os.chmod(target, 0o000)
        try:
            if os.access(target, os.R_OK):  # running as root; nothing to test
                pytest.skip("cannot make a file unreadable as this user")
            with pytest.raises(DataFileError):
                CrunchLog(str(target))
        finally:
            os.chmod(target, 0o644)

    def test_missing_file_raises_cleanly(self, tmp_path):
        with pytest.raises(DataFileError):
            CrunchLog(str(tmp_path / "does-not-exist.log"))


def mixed_log(syslog_fraction=0.7, lines=40):
    """A buffer whose shape changes part way through — the ordinary case for
    application logs and for tool output that interleaves JSON with prose."""
    k = int(lines * syslog_fraction)
    return "\n".join(
        [f"Sep 19 04:00:{i:02d} host01 sshd[{i}]: Accepted publickey for scott "
         f"from 10.0.0.{i} port 22" for i in range(k)]
        + ["an ordinary prose sentence slipped into the stream here"
           for _ in range(lines - k)]
    )


class TestDeterminism:
    """Selection used to draw sample lines with random.choice, so the driver
    — and therefore the whole result — depended on the RNG as well as the
    input. The same bytes could parse two different ways, or succeed on one
    call and raise on the next."""

    def test_detection_is_stable_across_calls(self):
        text = mixed_log()
        assert len({detect_format(text) for _ in range(50)}) == 1

    def test_grouping_is_stable_across_calls(self):
        text = mixed_log()
        shapes = {
            tuple((g.pattern, g.count) for g in hash_text(text))
            for _ in range(50)
        }
        assert len(shapes) == 1

    def test_stable_at_every_mixture(self):
        for fraction in (0.3, 0.5, 0.7, 0.9):
            text = mixed_log(fraction)
            assert len({detect_format(text) for _ in range(30)}) == 1


class TestMixedInput:
    """A driver is chosen from a sample and then applied to every line, so
    one line in another shape used to abort the entire run."""

    def test_unparseable_line_degrades_instead_of_raising(self):
        text = secure_log() + "\nan ordinary prose sentence in the stream"
        result = analyze_text(text)
        assert result.degraded is True
        assert result.driver == "RawEntry"

    def test_degraded_run_still_accounts_for_every_line(self):
        text = secure_log() + "\nan ordinary prose sentence in the stream"
        result = analyze_text(text)
        assert result.lines_in == 201
        assert result.lines_grouped == 201

    def test_the_odd_line_out_survives_into_a_sample(self):
        """The interloper is the interesting line. Losing it to a parse
        error, or silently dropping it, defeats the point of the tool."""
        text = secure_log() + "\nan ordinary prose sentence in the stream"
        groups = hash_text(text)
        assert any(
            "ordinary prose sentence" in sample
            for group in groups
            for sample in group.samples
        )

    def test_strict_restores_the_old_raising_behaviour(self):
        text = secure_log() + "\nan ordinary prose sentence in the stream"
        with pytest.raises(ParseError):
            analyze_text(text, strict=True)

    def test_a_clean_log_is_not_marked_degraded(self):
        assert analyze_text(secure_log()).degraded is False


class TestDriverOverride:
    """A caller that must not have per-format vocabulary applied to its
    payloads pins RawEntry and gets purely structural grouping."""

    def test_pinning_raw_skips_detection(self):
        assert analyze_text(secure_log(), driver="RawEntry").driver == "RawEntry"

    def test_pinned_raw_does_not_generalise_the_payload(self):
        """A pinned RawEntry applies no sshd vocabulary at all."""
        text = "\n".join(
            f"Sep 19 04:00:{i:02d} host01 sshd[{i}]: Accepted publickey for u{i} from 10.0.0.{i}"
            for i in range(50)
        )
        assert len(analyze_text(text).groups) == 1
        pinned = analyze_text(text, driver="RawEntry", filter_name="__none__")
        assert len(pinned.groups) == 50

    def test_detected_secure_log_keeps_the_user_name(self):
        """"Invalid user.*" used to swallow the name a client chose, so an
        odd one merged into the crowd. The rule now collapses only the
        source address after it."""
        boilerplate = "\n".join(
            f"Sep 19 04:00:{i:02d} host01 sshd[{i}]: Invalid user bob{i} from 10.0.0.{i}"
            for i in range(50)
        )
        text = boilerplate + (
            "\nSep 19 04:59:59 host01 sshd[99]: Invalid user DISTINCTIVE from 10.0.0.99"
        )
        detected = analyze_text(text)
        assert detected.driver == "SecureLogEntry"
        assert any("DISTINCTIVE" in g.pattern for g in detected.groups)

    def test_unknown_driver_is_rejected(self):
        with pytest.raises(PetitError):
            analyze_text(secure_log(), driver="NoSuchEntry")

    def test_driver_name_cannot_reach_arbitrary_attributes(self):
        for name in ("re", "sys", "CrunchLog", "__builtins__"):
            with pytest.raises(PetitError):
                analyze_text(secure_log(), driver=name)


class TestNoFabricatedFields:
    def test_raw_text_samples_do_not_invent_an_envelope(self):
        """Raw text has no timestamp, host or daemon. Rendering from parsed
        fields supplied placeholders for all three, so a JSON line came back
        as "01 01 01:01:01 # # ..." — data the input never contained."""
        text = "\n".join(f'  "key": "PROJ-{i}",' for i in range(30))
        for group in hash_text(text):
            for sample in group.samples:
                assert "01 01 01:01:01" not in sample
                assert sample in text.splitlines()


class TestSecureLogIsNotConsumed:
    def test_hashing_does_not_mutate_the_log(self):
        """fill() used to assign its generalised form back onto the entry,
        so hashing a log destroyed it for every later reader."""
        log = CrunchLog.from_text(secure_log())
        before = [entry.log_entry for entry in log]
        SuperHash.manufacture(log, "hash.stopwords")
        assert [entry.log_entry for entry in log] == before


class TestSampleLineNumbers:
    """Grouping reorders by definition. A caller that wants to present
    samples in written order needs to know where they came from."""

    def test_sample_lines_are_parallel_to_samples(self):
        for group in hash_text(secure_log()):
            assert len(group.sample_lines) == len(group.samples)

    def test_sample_lines_point_at_the_right_lines(self):
        text = secure_log()
        lines = text.splitlines()
        for group in hash_text(text):
            for number, sample in zip(group.sample_lines, group.samples, strict=True):
                assert lines[number] == sample

    def test_sample_lines_survive_the_degraded_path(self):
        text = secure_log() + "\nan ordinary prose sentence in the stream"
        lines = text.splitlines()
        result = analyze_text(text)
        assert result.degraded is True
        for group in result.groups:
            for number, sample in zip(group.sample_lines, group.samples, strict=True):
                assert lines[number] == sample


class TestCallerSuppliedStopwords:
    """Normalisation policy belongs to whoever reads the output. The
    packaged hash.stopwords is right for system logs and wrong for a caller
    that needs two distinct values to stay distinct."""

    NAMES = "\n".join(
        [f"user bob{i} logged in" for i in range(15)]
        + [f"user boa{i} logged in" for i in range(15)]
    )

    def test_packaged_filter_collapses_adjacent_letters(self):
        """Documents the behaviour that motivates the option: `[a-f]+#`
        eats the letter next to a scrubbed number, so two different names
        share a fingerprint."""
        groups = hash_text(self.NAMES, driver="RawEntry", filter_name="hash.stopwords")
        assert len(groups) == 1
        assert groups[0].pattern == "user bo# logged in"

    def test_raw_text_defaults_to_the_strict_filter(self):
        """RawLogHash declares strict.stopwords: a number glued to a word is
        part of an identifier and stays; only standalone numbers go."""
        assert len(hash_text(self.NAMES, driver="RawEntry")) == 30
        spaced = self.NAMES.replace("bob", "bob ").replace("boa", "boa ")
        patterns = {g.pattern for g in hash_text(spaced, driver="RawEntry")}
        assert patterns == {"user bob <N> logged in", "user boa <N> logged in"}

    def test_a_missing_filter_file_is_an_error(self):
        with pytest.raises(DataFileError):
            hash_text(self.NAMES, filter_name="no-such.stopwords")

    def test_caller_patterns_keep_distinct_words_distinct(self):
        groups = hash_text(self.NAMES, driver="RawEntry", stopwords=[r"[0-9]+"])
        patterns = {g.pattern for g in groups}
        assert patterns == {"user bob# logged in", "user boa# logged in"}

    def test_caller_patterns_still_normalise_what_they_are_given(self):
        groups = hash_text(self.NAMES, driver="RawEntry", stopwords=[r"[0-9]+"])
        assert sum(g.count for g in groups) == 30
        assert all(g.count == 15 for g in groups)

    def test_empty_pattern_list_means_no_normalisation(self):
        groups = hash_text(self.NAMES, driver="RawEntry", stopwords=[])
        assert len(groups) == 30

    def test_stopwords_override_filter_name(self):
        groups = hash_text(
            self.NAMES,
            driver="RawEntry",
            filter_name="hash.stopwords",
            stopwords=[r"[0-9]+"],
        )
        assert len(groups) == 2

    def test_samples_are_still_verbatim_with_caller_patterns(self):
        lines = self.NAMES.splitlines()
        for group in hash_text(self.NAMES, driver="RawEntry", stopwords=[r"[0-9]+"]):
            for number, sample in zip(group.sample_lines, group.samples, strict=True):
                assert lines[number] == sample


class TestPatternReplacements:
    """A fingerprint that says what it normalised away is worth more than
    one that only says something was there."""

    TEXT = "\n".join(
        f"2026-09-19T04:00:{i:02d} host sshd[{i}]: login from 10.0.0.{i}"
        for i in range(30)
    )
    RULES: ClassVar[list[tuple[str, str]]] = [
        (r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", "<TS>"),
        (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "<IP>"),
        (r"\d+", "<N>"),
    ]

    def test_replacements_appear_in_the_pattern(self):
        groups = hash_text(self.TEXT, driver="RawEntry", stopwords=self.RULES)
        assert len(groups) == 1
        assert groups[0].pattern == "<TS> host sshd[<N>]: login from <IP>"

    def test_bare_regexes_still_scrub_to_hash(self):
        groups = hash_text(self.TEXT, driver="RawEntry", stopwords=[r"\d+"])
        assert groups[0].pattern == "#-#-#T#:#:# host sshd[#]: login from #.#.#.#"

    def test_bare_and_paired_rules_can_be_mixed(self):
        groups = hash_text(
            self.TEXT, driver="RawEntry",
            stopwords=[(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "<IP>"), r"\d+"],
        )
        assert groups[0].pattern == "#-#-#T#:#:# host sshd[#]: login from <IP>"

    def test_rule_order_is_preserved(self):
        """Specific before generic, or an ISO timestamp becomes six <N>s."""
        reversed_rules = list(reversed(self.RULES))
        groups = hash_text(self.TEXT, driver="RawEntry", stopwords=reversed_rules)
        assert "<TS>" not in groups[0].pattern


DATA = os.path.join(os.path.dirname(__file__), "data")


def fixture_text(name):
    with open(os.path.join(DATA, name)) as handle:
        return handle.read()


class TestHashModes:
    """Every grouping the CLI offers is reachable from the library."""

    def test_daemon_mode_groups_by_daemon(self):
        result = analyze_text(fixture_text("test01.log"), hash_mode="daemon")
        assert result.groups
        assert all(" " not in g.pattern for g in result.groups)

    def test_host_mode_groups_by_host(self):
        result = analyze_text(fixture_text("test01.log"), hash_mode="host")
        assert result.groups

    def test_wordcount_samples_are_the_lines_the_word_came_from(self):
        text = fixture_text("test01.log")
        lines = text.splitlines()
        for group in analyze_text(text, hash_mode="wordcount").groups:
            for number, sample in zip(group.sample_lines, group.samples, strict=True):
                assert lines[number] == sample

    def test_unknown_mode_is_rejected(self):
        with pytest.raises(PetitError):
            analyze_text(secure_log(), hash_mode="nonsense")


class TestFingerprintCollapse:
    """Reboot-sequence collapsing used to be reachable only from --fingerprint."""

    def test_off_by_default(self):
        result = analyze_text(fixture_text("test05.log"))
        assert result.fingerprints_matched == []

    def test_matches_are_reported_and_collapsed(self):
        text = fixture_text("test05.log")
        plain = analyze_text(text)
        collapsed = analyze_text(text, collapse_fingerprints=True)
        assert collapsed.fingerprints_matched == ["rhel4-reboot.fp"]
        assert len(collapsed.groups) < len(plain.groups)
        assert any(g.pattern == "rhel4-reboot.fp" for g in collapsed.groups)

    def test_nothing_matched_is_distinguishable_from_off(self):
        result = analyze_text(fixture_text("test01.log"), collapse_fingerprints=True)
        assert result.fingerprints_matched == []

    def test_repeat_calls_agree(self):
        """Corpora are cached between calls; the first match used to
        overwrite a corpus entry in place, which a cache would carry into
        every later call."""
        text = fixture_text("test06.log")
        first = analyze_text(text, collapse_fingerprints=True)
        second = analyze_text(text, collapse_fingerprints=True)
        assert first.fingerprints_matched == second.fingerprints_matched
        assert first.groups == second.groups

    def test_corpora_are_parsed_once(self, monkeypatch):
        first = analyze_text(fixture_text("test05.log"), collapse_fingerprints=True)

        def boom(*_args, **_kwargs):
            raise AssertionError("corpus re-read from disk")

        monkeypatch.setattr("petit.LogHash.CrunchLog", boom)
        second = analyze_text(fixture_text("test05.log"), collapse_fingerprints=True)
        assert second.fingerprints_matched == first.fingerprints_matched == ["rhel4-reboot.fp"]


class TestOneParser:
    """The CLI reads a file and hands its text to the same splitter the
    library uses; the two used to disagree about what ends a line."""

    def test_form_feed_does_not_split_a_line(self):
        result = analyze_text("one\x0ctwo\n", driver="RawEntry")
        assert result.lines_in == 1

    def test_crlf_is_not_kept_in_samples(self):
        groups = hash_text("alpha beta\r\nalpha beta\r\n", driver="RawEntry")
        assert groups[0].samples == ["alpha beta", "alpha beta"]

    def test_file_and_text_parse_identically(self):
        path = os.path.join(DATA, "test08.log")
        from_file = CrunchLog(path)
        from_text = CrunchLog.from_text(fixture_text("test08.log"))
        assert [e.raw for e in from_file] == [e.raw for e in from_text]

    def test_undecodable_file_raises_cleanly(self, tmp_path):
        target = tmp_path / "binary.log"
        target.write_bytes(b"\xff\xfe\x00garbage\n")
        with pytest.raises(DataFileError):
            CrunchLog(str(target))


class TestSiteLocalFingerprints:
    def test_site_local_corpus_is_read_alongside_packaged(self, tmp_path, monkeypatch):
        """The packaged directory always has files, and only the first
        directory with files used to be read, so site-local corpora never
        were."""
        corpus = "\n".join(
            f"Sep 22 10:00:{i:02d} host01 custom[1]: step {w} done"
            for i, w in enumerate(["alpha", "bravo", "charlie", "delta"])
        )
        (tmp_path / "custom-event.fp").write_text(corpus + "\n")
        packaged = resources.search_prefixes("fingerprints")[0]
        monkeypatch.setattr(
            LogHash, "search_prefixes", lambda _kind: [packaged, str(tmp_path) + "/"]
        )
        result = analyze_text(corpus + "\nSep 22 10:01:00 host01 other[2]: unrelated",
                              collapse_fingerprints=True)
        assert result.fingerprints_matched == ["custom-event.fp"]


def _word(i):
    """A distinct lowercase word per integer. Digits would be normalised
    away, so synthetic corpora spell their lines out."""
    word = ""
    i += 1
    while i:
        i, rest = divmod(i - 1, 26)
        word = "abcdefghijklmnopqrstuvwxyz"[rest] + word
    return word


def _event(tag, words):
    """A corpus text: one line per word, all from the same daemon."""
    return "\n".join(f"Sep 22 10:00:00 host01 unit[1]: {tag} {_word(i)} reached" for i in words)


class TestFingerprintVote:
    """#49: corpora used to be tried largest first, and the first past the
    threshold took the input and removed its lines. Overlapping corpora
    claimed each other's reboots — rhel4 took a rhel5 reboot, ubuntu10.04 an
    ubuntu9.04 one."""

    PACKAGED = sorted(os.listdir(os.path.join(os.path.dirname(LogHash.__file__),
                                              "data", "fingerprints")))

    @staticmethod
    def corpus_text(name):
        path = os.path.join(os.path.dirname(LogHash.__file__), "data", "fingerprints", name)
        with open(path) as handle:
            return handle.read()

    @staticmethod
    def only(monkeypatch, directory, **corpora):
        """Load exactly these corpora, written to `directory`."""
        for name, text in corpora.items():
            (directory / f"{name}.fp").write_text(text + "\n")
        monkeypatch.setattr(LogHash, "search_prefixes", lambda _kind: [str(directory) + "/"])

    @pytest.mark.parametrize("name", PACKAGED)
    def test_every_packaged_corpus_names_only_itself(self, name):
        result = analyze_text(self.corpus_text(name), collapse_fingerprints=True)
        assert result.fingerprints_matched == [name]

    # ubuntu10.04 is RSyslog's format and the rest classic syslog. A log
    # that mixes the two is read as raw text, which none of them match.
    @pytest.mark.parametrize(("a", "b"), list(itertools.combinations(
        [name for name in PACKAGED if name != "ubuntu10.04-reboot.fp"], 2)))
    def test_two_reboots_in_one_log_both_collapse(self, a, b):
        text = self.corpus_text(a) + self.corpus_text(b)
        result = analyze_text(text, collapse_fingerprints=True)
        assert sorted(result.fingerprints_matched) == [a, b]

    def test_small_corpus_inside_a_large_one_keeps_its_own_log(self, tmp_path, monkeypatch):
        """First-fit gave this log to the large corpus: it clears 31% of it."""
        self.only(monkeypatch, tmp_path,
                  large=_event("common", range(400)),
                  small=_event("common", range(150)) + "\n" + _event("own", range(20)))
        log = _event("common", range(150)) + "\n" + _event("own", range(20))
        assert analyze_text(log, collapse_fingerprints=True).fingerprints_matched == ["small.fp"]

    def test_large_corpus_keeps_its_own_log(self, tmp_path, monkeypatch):
        self.only(monkeypatch, tmp_path,
                  large=_event("common", range(400)),
                  small=_event("common", range(150)) + "\n" + _event("own", range(20)))
        log = _event("common", range(400))
        assert analyze_text(log, collapse_fingerprints=True).fingerprints_matched == ["large.fp"]

    def test_superset_log_is_not_tied_with_its_subset(self, tmp_path, monkeypatch):
        """A corpus wholly inside another is fully covered by the larger
        one's log. Scoring coverage alone calls that a tie."""
        self.only(monkeypatch, tmp_path,
                  large=_event("common", range(400)),
                  subset=_event("common", range(150)))
        whole = analyze_text(_event("common", range(400)), collapse_fingerprints=True)
        part = analyze_text(_event("common", range(150)), collapse_fingerprints=True)
        assert whole.fingerprints_matched == ["large.fp"]
        assert part.fingerprints_matched == ["subset.fp"]

    def test_twins_are_told_apart_by_their_own_lines(self, tmp_path, monkeypatch):
        self.only(monkeypatch, tmp_path,
                  el9=_event("common", range(300)) + "\n" + _event("nine", range(15)),
                  el10=_event("common", range(300)) + "\n" + _event("ten", range(15)))
        log = _event("common", range(300)) + "\n" + _event("nine", range(15))
        assert analyze_text(log, collapse_fingerprints=True).fingerprints_matched == ["el9.fp"]

    def test_twins_with_nothing_to_tell_them_apart_are_both_named(self, tmp_path, monkeypatch):
        """An honest "one of these two" beats a confident wrong answer."""
        self.only(monkeypatch, tmp_path,
                  el9=_event("common", range(300)) + "\n" + _event("nine", range(3)),
                  el10=_event("common", range(300)) + "\n" + _event("ten", range(3)))
        log = _event("common", range(300)) + "\n" + _event("nine", range(3))
        result = analyze_text(log, collapse_fingerprints=True)
        assert result.fingerprints_matched == ["el10.fp|el9.fp"]
        assert any(g.pattern == "el10.fp|el9.fp" for g in result.groups)

    def test_both_twins_rebooting_collapse_separately(self, tmp_path, monkeypatch):
        self.only(monkeypatch, tmp_path,
                  el9=_event("common", range(300)) + "\n" + _event("nine", range(15)),
                  el10=_event("common", range(300)) + "\n" + _event("ten", range(15)))
        log = "\n".join([_event("common", range(300)), _event("nine", range(15)),
                         _event("ten", range(15))])
        result = analyze_text(log, collapse_fingerprints=True)
        assert sorted(result.fingerprints_matched) == ["el10.fp", "el9.fp"]

    def test_adding_a_corpus_reweighs_the_vote(self, tmp_path, monkeypatch):
        """Weights belong to the whole set of corpora, so a cached set must
        not outlive a corpus added beside it."""
        log = _event("common", range(300))
        self.only(monkeypatch, tmp_path,
                  el9=_event("common", range(300)) + "\n" + _event("nine", range(3)))
        assert analyze_text(log, collapse_fingerprints=True).fingerprints_matched == ["el9.fp"]
        self.only(monkeypatch, tmp_path,
                  el10=_event("common", range(300)) + "\n" + _event("ten", range(3)))
        assert analyze_text(log, collapse_fingerprints=True).fingerprints_matched == \
            ["el10.fp|el9.fp"]

    def test_scores_show_the_vote(self):
        text = fixture_text("test06.log")
        first = analyze_text(text, collapse_fingerprints=True)
        second = analyze_text(text, collapse_fingerprints=True)
        assert first.fingerprint_scores == second.fingerprint_scores
        names = [score.name for score in first.fingerprint_scores]
        assert names == sorted(names)
        assert set(first.fingerprints_matched) <= set(names)
        for score in first.fingerprint_scores:
            assert 0 < score.detection <= 1
            assert 0 < score.identity <= 1

    def test_no_scores_when_not_asked(self):
        assert analyze_text(fixture_text("test06.log")).fingerprint_scores == []


# Reboot logs captured to verify the corpora (#37), one directory per corpus
# they must match: test/data/verify/<corpus>.fp/<capture>.log.
VERIFY = os.path.join(DATA, "verify")
VERIFY_CASES = sorted(
    (corpus, capture)
    for corpus in (os.listdir(VERIFY) if os.path.isdir(VERIFY) else [])
    for capture in os.listdir(os.path.join(VERIFY, corpus))
    if capture.endswith(".log")
)


@pytest.mark.skipif(not VERIFY_CASES, reason="no verification captures yet (#37)")
@pytest.mark.parametrize(("corpus", "capture"), VERIFY_CASES or [("", "")])
def test_verification_capture_matches_its_corpus_first(corpus, capture):
    with open(os.path.join(VERIFY, corpus, capture)) as handle:
        result = analyze_text(handle.read(), collapse_fingerprints=True)
    assert result.fingerprints_matched
    assert corpus in result.fingerprints_matched[0].split("|")


class TestWordcountMerge:
    """#33: words that scrub to the same key used to have their
    [count, members] lists concatenated, so the count stayed the first
    word's and the rest were lost."""

    TEXT = "\n".join(
        ["Sep 22 10:00:00 h d[1]: foo1 x"] * 3 + ["Sep 22 10:00:00 h d[1]: foo2 x"] * 5
    )

    def test_counts_add_up(self):
        groups = {g.pattern: g for g in analyze_text(self.TEXT, hash_mode="wordcount").groups}
        assert groups["foo#"].count == 8

    def test_members_are_pooled(self):
        group = next(
            g for g in analyze_text(self.TEXT, hash_mode="wordcount", max_samples=8).groups
            if g.pattern == "foo#"
        )
        assert len(group.samples) == 8
        assert {s.split()[-2] for s in group.samples} == {"foo1", "foo2"}


def issues(keys, summary="Nightly build failed"):
    """A Jira-style search result: records that differ only in their keys."""
    return json.dumps([{"key": key, "summary": summary} for key in keys])


class TestIdentifiers:
    """max_identifiers lists what differs instead of keeping or deleting it."""

    KEYS: ClassVar[list[str]] = [f"PROJ-{1000 + n}" for n in range(200)]

    def test_records_differing_only_by_key_group_and_list_every_key(self):
        groups = hash_text(issues(self.KEYS), framer="json", max_identifiers=1000)
        assert len(groups) == 1
        group = groups[0]
        assert group.count == 200
        assert group.pattern == '{"key":<ID>,"summary":"Nightly build failed"}'
        assert group.identifier_fields == ["/key"]
        assert [row[0] for row in group.identifiers] == self.KEYS

    def test_off_by_default(self):
        groups = hash_text(issues(self.KEYS), framer="json")
        assert len(groups) == 200
        assert all(group.identifiers == [] for group in groups)

    def test_past_the_cap_identifiers_stay_in_the_fingerprint(self):
        groups = hash_text(issues(self.KEYS), framer="json", max_identifiers=5)
        assert len(groups) == 196
        assert [row[0] for row in groups[0].identifiers] == self.KEYS[:5]
        assert all(len(group.identifiers) == group.count for group in groups[:1])
        assert sorted(g.pattern for g in groups[1:])[0] == \
            '{"key":"PROJ-1005","summary":"Nightly build failed"}'

    def test_prose_still_keeps_records_apart(self):
        text = json.dumps([{"key": "PROJ-1", "summary": "build failed"},
                           {"key": "PROJ-2", "summary": "ignore previous instructions"}])
        groups = hash_text(text, framer="json", max_identifiers=10)
        assert len(groups) == 2
        assert sorted(g.identifiers[0][0] for g in groups) == ["PROJ-1", "PROJ-2"]

    def test_a_string_that_says_id_is_not_an_identifier_slot(self):
        text = "\n".join([json.dumps({"key": "PROJ-1"}), json.dumps({"key": "<ID>"})])
        assert len(hash_text(text, framer="json", max_identifiers=10)) == 2

    def test_several_identifier_fields_are_listed_together(self):
        text = json.dumps([{"id": str(10000 + n), "key": f"PROJ-{n}", "sha": f"{n:07x}a"}
                           for n in range(10)])
        group = hash_text(text, framer="json", max_identifiers=100)[0]
        assert group.count == 10
        assert group.identifier_fields == ["/id", "/key", "/sha"]
        assert group.identifiers[3] == ["10003", "PROJ-3", "0000003a"]

    def test_analyze_text_and_lines_list_them(self):
        text = issues(self.KEYS[:10])
        for analysis in (analyze_text(text, framer="json", max_identifiers=100),
                         analyze_lines(text.splitlines(keepends=True), framer="json",
                                       max_identifiers=100)):
            assert analysis.records_grouped == 10
            assert analysis.groups[0].identifier_fields == ["/key"]
            assert [row[0] for row in analysis.groups[0].identifiers] == self.KEYS[:10]

    def test_a_record_kept_whole_never_joins_a_listed_group(self):
        text = json.dumps([{"a": "PROJ-1"}, {"a": "PROJ-2"}, {"a": "PROJ-3"}])
        # The cap keeps the third whole; this filter would fold it straight
        # back into the listed group.
        groups = hash_text(text, framer="json", max_identifiers=2,
                           stopwords=[(r'<ID>|"PROJ-\d"', "V")])
        assert all(len(group.identifiers) in (0, group.count) for group in groups)
        assert sum(group.count for group in groups) == 3

    def test_a_record_with_no_identifiers_never_joins_a_listed_group(self):
        text = json.dumps([{"a": "PROJ-1"}, {"a": "PROJ-2"}, {"a": "plain"}])
        groups = hash_text(text, framer="json", max_identifiers=10,
                           stopwords=[(r'<ID>|"plain"', "V")])
        assert sorted((g.count, len(g.identifiers)) for g in groups) == [(1, 0), (2, 2)]
        assert any(g.pattern.endswith("<UNLISTED>") for g in groups)

    def test_a_listed_record_never_joins_an_unlisted_group(self):
        text = json.dumps([{"a": "plain"}, {"a": "PROJ-1"}])
        groups = hash_text(text, framer="json", max_identifiers=10,
                           stopwords=[(r'<ID>|"plain"', "V")])
        assert len(groups) == 2
        assert all(group.identifiers == [] for group in groups)

    def test_collapsing_fingerprints_leaves_listed_groups_alone(self):
        text = issues(self.KEYS)
        plain = hash_text(text, framer="json", max_identifiers=1000)
        assert hash_text(text, framer="json", max_identifiers=1000,
                         collapse_fingerprints=True) == plain

    def test_line_input_lists_identifiers_too(self):
        lines = [json.dumps({"key": key, "summary": "x"}) + "\n" for key in self.KEYS[:10]]
        group = hash_lines(lines, framer="json", max_identifiers=100)[0]
        assert group.count == 10
        assert [row[0] for row in group.identifiers] == self.KEYS[:10]

    def test_a_key_too_long_to_place_its_identifiers_is_left_whole(self):
        long_tail = ["y" * 190 + str(n) for n in range(30)]
        text = json.dumps([{"key": key, "more": long_tail} for key in self.KEYS[:5]])
        groups = hash_text(text, framer="json", max_identifiers=100, max_record_chars=1000)
        assert all(group.identifiers == [] for group in groups)

    def test_a_filter_that_folds_shapes_together_never_mixes_fields(self):
        text = json.dumps([{"a": "PROJ-1", "b": "x"}, {"a": "x", "b": "PROJ-2"}])
        # Folds the two keys together, so the second record's fields (/b)
        # would otherwise land under the first's (/a).
        groups = hash_text(text, framer="json", max_identifiers=10,
                           stopwords=[(r'"a"|"b"', '"k"'), (r'<ID>|"x"', "V")])
        for group in groups:
            assert all(len(row) == len(group.identifier_fields) for row in group.identifiers)
        assert sum(len(group.identifiers) for group in groups) == 1

    def test_a_record_that_is_mostly_identifiers_is_left_whole(self):
        text = json.dumps([{f"k{f}": f"PROJ-{n * 10 + f}" for f in range(5)} for n in range(10)])
        groups = hash_text(text, framer="json", max_identifiers=100)
        assert len(groups) == 10
        assert all(group.identifiers == [] for group in groups)

    @pytest.mark.parametrize("value", [
        "10234", "PROJ-1234", "gh-12", "#42", "3f2c9a1e-1b2c-4d5e-8f90-0123456789ab",
        "adddc55", "4731ad4e9f",
    ])
    def test_identifier_shapes(self, value):
        assert pull_identifiers({"v": value})[2] == (value,)

    @pytest.mark.parametrize("value", [
        "done", "Nightly build failed", "deadbeef", "2026-09-22", "PROJ-1 and more",
        "PROJ-" + "1" * 13, "a" * 65, "1" * 21, "-5", "1.5",
    ])
    def test_not_identifiers(self, value):
        assert pull_identifiers({"v": value}) == ({"v": value}, (), ())

    def test_max_fields_is_all_or_nothing(self):
        record = {"a": "PROJ-1", "b": "PROJ-2", "c": "text"}
        assert pull_identifiers(record, max_fields=2)[1] == ("/a", "/b")
        assert pull_identifiers(record, max_fields=1) == (record, (), ())

    def test_numbers_are_not_pulled(self):
        assert pull_identifiers({"id": 10234}) == ({"id": 10234}, (), ())

    def test_fields_are_json_pointers_in_sorted_key_order(self):
        masked, fields, values = pull_identifiers(
            {"z": "PROJ-1", "a/b": [{"~": "#2"}], "m": "text"})
        assert fields == ("/a~1b/0/~0", "/z")
        assert values == ("#2", "PROJ-1")
        assert list(masked) == ["a/b", "m", "z"]
        assert json.loads(json.dumps(masked)) == {"z": "<ID>", "a/b": [{"~": "<ID>"}], "m": "text"}
        assert masked["z"] is IDENTIFIER


def test_library_leaves_root_logger_alone():
    """A host's basicConfig() must still take effect after petit has run (#89).

    Module-level logging.info() installs a default root handler, after which
    the host's own basicConfig() is a silent no-op. Run in a fresh
    interpreter: pytest configures logging itself.
    """
    script = textwrap.dedent(f"""
        import logging
        from petit import analyze_text, hash_text
        from petit.Filter import Filter
        Filter("words.stopwords")
        text = {secure_log()!r}
        analyze_text(text)
        hash_text(text)
        print(logging.getLogger().handlers)
    """)
    child = subprocess.run([sys.executable, "-c", script],
                           check=True, capture_output=True, text=True)
    assert child.stdout.strip() == "[]"
