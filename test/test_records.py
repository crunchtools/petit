"""Framing: records that are not lines, and what that does to the accounting."""

from __future__ import annotations

import json
import os
from typing import ClassVar

import pytest

from petit import PetitError, analyze_text, hash_text
from petit.CrunchLog import (
    ApacheAccessEntry,
    ApacheErrorEntry,
    CrunchLog,
    RawEntry,
    RSyslogEntry,
    SecureLogEntry,
    SnortEntry,
    SyslogEntry,
    entry_types,
)
from petit.LogGraph import fit_graph
from petit.LogHash import (
    ApacheLogHash,
    RawLogHash,
    SecureLogHash,
    SnortLogHash,
    SuperHash,
    SyslogHash,
    hash_for,
)
from petit.records import (
    HEAD_PATTERNS,
    MAX_RECORD_LINES,
    JsonFramer,
    LineFramer,
    MessageFramer,
    MultilineFramer,
    Record,
)

DATA = os.path.join(os.path.dirname(__file__), "data")


def fixture_lines(name: str) -> list[str]:
    with open(os.path.join(DATA, name)) as handle:
        return handle.readlines()


class TestBackwardCompatibility:
    @pytest.mark.parametrize("number", range(1, 13))
    def test_only_the_line_framer_claims_the_2009_corpus(self, number):
        """The load-bearing fact: test01-test13 frame exactly as before."""
        buf = fixture_lines(f"test{number:02d}.log")
        assert not JsonFramer.claims(buf)
        assert not MessageFramer.claims(buf)
        assert not MultilineFramer.claims(buf)

    def test_line_records_are_the_lines(self):
        buf = ["one\n", "two\n"]
        assert LineFramer.frame(buf) == [Record(["one\n"], 0, 1), Record(["two\n"], 1, 2)]


class TestJsonFramer:
    ARRAY = '[\n  {"a": 1},\n  {"a": 2,\n   "b": "x"}\n]\n'

    def test_array_elements_map_to_their_source_lines(self):
        records = JsonFramer.frame(self.ARRAY.splitlines(keepends=True))
        assert [(r.start, r.end) for r in records] == [(1, 2), (2, 4)]
        assert [json.loads(r.text) for r in records] == [{"a": 1}, {"a": 2, "b": "x"}]

    def test_compact_array_shares_one_line(self):
        records = JsonFramer.frame(['[{"a": 1}, {"a": 2}]\n'])
        assert [r.text for r in records] == ['{"a": 1}', '{"a": 2}']
        assert all((r.start, r.end) == (0, 1) for r in records)

    def test_json_lines_skip_blank_lines(self):
        buf = ['{"a": 1}\n', "\n", '{"a": 2}\n']
        assert JsonFramer.claims(buf)
        assert [(r.start, r.end) for r in JsonFramer.frame(buf)] == [(0, 1), (2, 3)]

    @pytest.mark.parametrize(
        "text",
        [
            "[1, 2, 3]\n",
            "[]\n",
            '{"a": 1}\nnot json\n',
            '{"a": 1,\n "b": 2}\n',
            '"just a string"\n',
        ],
    )
    def test_declines_what_is_not_objects(self, text):
        assert not JsonFramer.claims(text.splitlines(keepends=True))


class TestMessageFramer:
    def test_splits_a_thread_on_header_blocks(self):
        buf = fixture_lines("test15.log")
        assert MessageFramer.claims(buf)
        records = MessageFramer.frame(buf)
        assert len(records) == 4
        assert all(r.text.startswith("From: ") for r in records)
        assert records[-1].end == len(buf)

    def test_thread_is_grouped_per_message(self):
        result = analyze_text("".join(fixture_lines("test15.log")))
        assert result.driver == "EmailEntry"
        assert result.records_in == 4
        assert [g.count for g in result.groups] == [2, 1, 1]

    def test_mbox_separators(self):
        buf = [
            "From a@x Mon Sep 22\n",
            "Subject: one\n",
            "\n",
            "body\n",
            "\n",
            "From b@x Mon Sep 22\n",
            "Subject: two\n",
            "\n",
            "body\n",
        ]
        assert [(r.start, r.end) for r in MessageFramer.frame(buf)] == [(0, 5), (5, 9)]

    def test_a_single_message_is_not_a_thread(self):
        assert not MessageFramer.claims(["From: a@x\n", "Subject: s\n", "\n", "body\n"])

    def test_key_value_prose_is_not_mail(self):
        buf = ["Note: one\n", "Status: ok\n", "\n", "Note: two\n", "Status: ok\n"]
        assert not MessageFramer.claims(buf)


class TestMultilineFramer:
    # One message head per HEAD_PATTERNS entry, as the format writes it.
    HEADS: ClassVar[dict[str, tuple[str, str]]] = {
        "bsd": (
            "Sep 19 15:41:27 host gnome-shell[2856]: first",
            "Sep 19 15:41:28 host gnome-shell[2856]: second",
        ),
        "iso": (
            "2026-09-20T08:00:00.101-04:00 host app[1]: first",
            "2026-09-20 08:00:01,202 ERROR app: second",
        ),
        "iso_bracket": (
            "[2026-09-20T08:00:00,101][WARN ][o.e.c] first",
            "[2026-09-20 08:00:01] ERROR second",
        ),
        "level_iso": ("ERROR 2026-09-20 08:00:00 first", "[INFO] 2026-09-20 08:00:01 second"),
        "slash": ("2026/09/20 08:00:00 [error] 12#12: first", "2026/09/20 08:00:01 second"),
        "ctime_bracket": (
            "[Sun Apr 10 04:04:00 2011] [error] first",
            "[Sun Apr 10 04:04:01.123456 2011] [error] second",
        ),
        "clf": (
            '1.2.3.4 - - [10/Apr/2011:04:04:00 -0400] "GET / HTTP/1.1" 200 1',
            '1.2.3.4 - - [10/Apr/2011:04:04:01 -0400] "GET /x HTTP/1.1" 200 1',
        ),
        "snort": ("09/29-08:25:54.519035 [**] first", "09/29-08:25:55.100000 [**] second"),
        "klog": (
            "I0920 08:00:00.123456    1 main.go:42] first",
            "E0920 08:00:01.000001    1 main.go:43] second",
        ),
        "kernel": ("[    0.000000] Linux version 6.12.0", "[ 1234.567890] usb 3-2: second"),
        "epoch": (
            "1789845105.816 12 10.0.0.1 TCP_MISS/200 first",
            "1789845106 12 10.0.0.1 TCP_HIT/200 second",
        ),
        "jul": (
            "Sep 20, 2026 8:00:00 AM org.apache.catalina.Foo first",
            "Sep 20, 2026 8:00:01 PM org.apache.catalina.Foo second",
        ),
        "tomcat": (
            "20-Sep-2026 08:00:00.101 SEVERE [main] first",
            "20-Sep-2026 08:00:01.202 INFO [main] second",
        ),
        "us_date": ("09/20/2026 08:00:00 first", "09/20/2026 8:00:01 second"),
        "redis": (
            "12345:M 20 Sep 2026 08:00:00.101 * first",
            "12345:C 20 Sep 2026 08:00:01.202 # second",
        ),
        "time_ms": ("08:00:00.101 [main] ERROR first", "08:00:01,202 [main] INFO second"),
    }

    def test_every_head_pattern_is_covered(self):
        assert set(self.HEADS) == set(HEAD_PATTERNS)

    @pytest.mark.parametrize("name", sorted(HEADS))
    def test_each_timestamp_format_starts_records(self, name):
        first, second = self.HEADS[name]
        buf = [first + "\n", "    continued\n", "\tat more\n", second + "\n"]
        assert HEAD_PATTERNS[name].match(first)
        assert MultilineFramer.claims(buf)
        assert [(r.start, r.end) for r in MultilineFramer.frame(buf)] == [(0, 3), (3, 4)]

    def test_unindented_continuations_fold_once_claimed(self):
        buf = fixture_lines("test18.log")
        records = MultilineFramer.frame(buf)
        assert len(records) == 7
        checkout = records[2].text
        assert "Caused by: java.sql" in checkout
        assert "... 12 more" in checkout

    def test_python_traceback_is_one_record(self):
        records = MultilineFramer.frame(fixture_lines("test17.log"))
        worker = next(r for r in records if "job 88" in r.text)
        assert "During handling of the above exception" in worker.text
        assert worker.text.rstrip().endswith("ConnectionError: report endpoint unreachable")

    def test_journald_markers_are_not_records(self):
        buf = fixture_lines("test16.log")
        records = MultilineFramer.frame(buf)
        assert not any(r.text.startswith("-- ") for r in records)
        # Every line but the two boot markers is in exactly one record.
        covered = [i for r in records for i in range(r.start, r.end)]
        assert len(covered) == len(set(covered)) == len(buf) - 2

    def test_journal_parses_as_syslog_not_raw(self):
        result = analyze_text("".join(fixture_lines("test16.log")))
        assert (result.framer, result.driver) == ("multiline", "SyslogEntry")
        assert (result.lines_in, result.records_in, result.records_grouped) == (33, 16, 16)
        traces = [g for g in result.groups if "GProxyVolume" in g.pattern]
        assert sorted(g.count for g in traces) == [1, 2]

    def test_a_multiline_message_graphs_once(self):
        log = CrunchLog.from_text("".join(fixture_lines("test16.log")))
        assert sum(fit_graph(log, 80).values()) == 16

    def test_a_different_timestamp_inside_a_record_does_not_split_it(self):
        buf = [
            "2026-09-20 08:00:00 ERROR first\n",
            "08:00:00.500 this line only looks like a head\n",
            "    indented\n",
            "2026-09-20 08:00:01 INFO second\n",
        ]
        assert [(r.start, r.end) for r in MultilineFramer.frame(buf)] == [(0, 3), (3, 4)]

    @pytest.mark.parametrize(
        ("why", "text"),
        [
            (
                "no indented line",
                "Sep 19 15:41:27 h a[1]: x\nnot indented\nSep 19 15:41:28 h a[1]: y\n",
            ),
            ("first line is not a head", "hello\n    world\nSep 19 15:41:28 h a[1]: y\n"),
            ("indented prose", "Dear reader,\n    this is a letter\n    with indents\n"),
            ("YAML", "server:\n  port: 8080\n  host: 0.0.0.0\n"),
            ("only blank lines", "\n\n\n"),
        ],
    )
    def test_declines(self, why, text):
        assert not MultilineFramer.claims(text.splitlines(keepends=True)), why

    def test_declines_a_record_longer_than_the_cap(self):
        buf = ["Sep 19 15:41:27 h a[1]: x\n"] + ["    more\n"] * MAX_RECORD_LINES
        assert not MultilineFramer.claims(buf)
        assert MultilineFramer.claims(buf[:MAX_RECORD_LINES])

    def test_can_be_forced_and_named(self):
        text = "".join(fixture_lines("test16.log"))
        assert analyze_text(text, framer="multiline").framer == "multiline"
        assert analyze_text(text, framer="line").framer == "line"


class TestAccounting:
    def test_line_framed_counts_are_unchanged(self):
        result = analyze_text("".join(fixture_lines("test08.log")))
        assert result.framer == "line"
        assert result.records_in == result.lines_in == 1500
        assert result.records_grouped == result.lines_grouped

    def test_json_counts_source_lines_not_records(self):
        result = analyze_text("".join(fixture_lines("test14.log")))
        assert result.framer == "json"
        assert result.driver == "StructuredEntry"
        assert result.records_in == 11
        assert result.lines_in == 168
        # Every line but the array's own brackets belongs to a record.
        assert result.lines_grouped == 166

    def test_compact_json_lines_are_not_double_counted(self):
        result = analyze_text('[{"a": 1}, {"a": 2}, {"a": 3}]\n')
        assert result.records_in == 3
        assert result.lines_grouped == 1

    def test_sample_spans_are_parallel_and_honest(self):
        lines = fixture_lines("test14.log")
        for group in analyze_text("".join(lines)).groups:
            assert len(group.sample_spans) == len(group.samples)
            for (start, end), sample in zip(group.sample_spans, group.samples, strict=True):
                assert sample.strip() in "".join(lines[start:end])
                assert group.sample_lines[0] >= 0

    def test_framer_can_be_forced(self):
        text = "".join(fixture_lines("test14.log"))
        assert analyze_text(text, framer="line").framer == "line"

    def test_forcing_a_framer_that_does_not_fit_is_an_error(self):
        with pytest.raises(PetitError):
            analyze_text("plain text\n", framer="json")

    def test_unknown_framer_is_rejected(self):
        with pytest.raises(PetitError):
            analyze_text("plain text\n", framer="xml")


class TestStructuredGrouping:
    def test_injected_instruction_stays_its_own_group(self):
        groups = hash_text("".join(fixture_lines("test14.log")))
        odd = [g for g in groups if "ignore previous instructions" in g.pattern]
        assert len(odd) == 1
        assert odd[0].count == 1


class TestHashDispatch:
    """manufacture() used to be an if/elif over the class of the last
    entry, with RawEntry tested before SecureLogEntry. A subclass of an
    entry driver fell to whichever branch came first."""

    @staticmethod
    def old_chain(entry_cls: type) -> type[SuperHash]:
        chain = [
            ((SyslogEntry, RSyslogEntry), SyslogHash),
            ((ApacheAccessEntry, ApacheErrorEntry), ApacheLogHash),
            ((SnortEntry,), SnortLogHash),
            ((RawEntry,), RawLogHash),
            ((SecureLogEntry,), SecureLogHash),
        ]
        for classes, hash_cls in chain:
            if issubclass(entry_cls, classes):
                return hash_cls
        raise AssertionError(f"old chain had no branch for {entry_cls.__name__}")

    @pytest.mark.parametrize(
        "entry_cls",
        [e for e in entry_types if e.__name__ not in ("StructuredEntry", "EmailEntry")],
        ids=lambda e: e.__name__,
    )
    def test_table_matches_the_old_chain(self, entry_cls):
        assert hash_for(entry_cls) is self.old_chain(entry_cls)

    def test_subclass_inherits_its_parents_hash_driver(self):
        class CustomSecure(SecureLogEntry):
            pass

        assert hash_for(CustomSecure) is SecureLogHash

    def test_manufacture_follows_the_parsed_driver(self):
        log = CrunchLog.from_text("".join(fixture_lines("test08.log")))
        assert type(SuperHash.manufacture(log)) is SecureLogHash
