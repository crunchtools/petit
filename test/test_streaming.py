"""Streaming (#38): input of any size in bounded memory, output unchanged.

petit reads a file in passes and a pipe once, keeping only counts and a
few samples. These tests hold it to three things: every way in — a path, a
pipe, the library's iterables — gives the batch answer; a pipe longer than
the head window still does; and memory does not grow with the input. The
big inputs are generated here, not committed.
"""

from __future__ import annotations

import datetime
import json
import os
import random
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

from petit import analyze_lines, analyze_text, hash_lines
from petit.CrunchLog import HEAD_CHARS, CrunchLog, LogEntry, LogStream
from petit.errors import PetitError
from petit.LogGraph import (
    GRAPH_FOR_UNIT,
    LADDER,
    MIN_SPAN,
    _align,
    _floor,
    _offset,
    fit_graph,
    time_range,
)
from petit.LogHash import SuperHash
from petit.records import HEADER_FIELD, MessageFramer
from petit.sources import ListSource, source_for

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"
FIXTURES = sorted(p for p in DATA_DIR.glob("test*.log") if p.stem != "test13")

MODES = [
    ["--hash"],
    ["--hash", "--fingerprint"],
    ["--hash", "--nosample"],
    ["--hash", "--nofilter"],
    ["--wordcount"],
    ["--host"],
    ["--daemon"],
    ["--sgraph"],
    ["--mgraph"],
    ["--hgraph"],
    ["--dgraph"],
    ["--mograph"],
    ["--ygraph"],
    ["--graph"],
    ["--span", "90m"],
]

USERS = ["root", "admin", "scott", "oracle", "test", "ubuntu", "git", "deploy"]
MESSAGES = [
    "Accepted publickey for {u} from 10.{a}.{b}.{c} port {p} ssh2",
    "Failed password for invalid user {u} from 192.168.{a}.{b} port {p} ssh2",
    "Failed password for {u} from 172.16.{a}.{b} port {p} ssh2",
    "Connection closed by 10.{a}.{b}.{c} port {p} [preauth]",
    "Received disconnect from 10.{a}.{b}.{c} port {p}:11: disconnected by user",
    "pam_unix(sshd:session): session opened for user {u} by (uid=0)",
    "pam_unix(sshd:session): session closed for user {u}",
    "Invalid user {u} from 203.0.{a}.{b} port {p}",
]


def sshd_log(lines: int, seed: int = 38) -> Iterator[str]:
    """A secure log two seconds a line, the shape #38 was measured on.

    Every address and port is random, so nearly every line is distinct
    text, but they fingerprint to a handful of groups: memory should follow
    the groups, not the lines.
    """
    rng = random.Random(seed)
    for i in range(lines):
        day, rest = divmod(i * 2, 86400)
        hour, rest = divmod(rest, 3600)
        minute, second = divmod(rest, 60)
        text = rng.choice(MESSAGES).format(
            u=rng.choice(USERS),
            a=rng.randint(0, 255),
            b=rng.randint(0, 255),
            c=rng.randint(0, 255),
            p=rng.randint(1024, 65535),
        )
        yield (
            f"Sep {1 + day % 28:2d} {hour:02d}:{minute:02d}:{second:02d} host01 "
            f"sshd[{rng.randint(1000, 1400)}]: {text}\n"
        )


def run_petit(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), COLUMNS="120")
    return subprocess.run(
        [sys.executable, "-m", "petit.cli", *args],
        input=stdin,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def summary(analysis):
    return (
        [(g.pattern, g.count) for g in analysis.groups],
        analysis.driver,
        analysis.degraded,
        analysis.framer,
        analysis.lines_in,
        analysis.lines_grouped,
        analysis.records_in,
        analysis.records_grouped,
        analysis.fingerprints_matched,
    )


# --- every way in gives the same answer ------------------------------------


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
@pytest.mark.parametrize("flags", MODES, ids=lambda f: "".join(f).replace("--", "-"))
def test_a_pipe_reads_like_the_file(path: Path, flags: list[str]) -> None:
    by_path = run_petit(*flags, str(path))
    by_pipe = run_petit(*flags, stdin=path.read_text())
    assert by_path.returncode == 0, by_path.stderr
    assert (by_pipe.returncode, by_pipe.stdout) == (0, by_path.stdout)


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
@pytest.mark.parametrize("hash_mode", ["auto", "daemon", "host", "wordcount"])
def test_every_library_entry_point_agrees(path: Path, hash_mode) -> None:
    text = path.read_text()
    expected = summary(analyze_text(text, hash_mode=hash_mode))
    with path.open() as handle:
        assert summary(analyze_lines(handle, hash_mode=hash_mode)) == expected
        assert not handle.closed, "voting stops reading early and must not close the file"
    assert summary(analyze_lines(text.splitlines(keepends=True), hash_mode=hash_mode)) == expected
    assert (
        summary(analyze_lines(iter(text.splitlines(keepends=True)), hash_mode=hash_mode))
        == expected
    )


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_keeping_one_sample_changes_nothing_but_the_samples(path: Path) -> None:
    text = path.read_text()
    one = analyze_text(text, max_samples=1, collapse_fingerprints=True)
    every = analyze_text(text, max_samples=10**9, collapse_fingerprints=True)
    assert summary(one) == summary(every)
    assert all(len(g.samples) <= 1 for g in one.groups)


def test_samples_are_bounded_per_group() -> None:
    log = LogStream(ListSource(list(sshd_log(2000))))
    hashed = log.build(lambda s: SuperHash.manufacture(s, max_samples=2))
    assert all(len(members) <= 2 for _count, members in hashed.values())
    assert sum(count for count, _members in hashed.values()) == 2000
    assert hashed.records_grouped == hashed.lines_grouped == 2000


def test_universal_newlines_on_a_pipe() -> None:
    text = "Sep  1 00:00:00 h a[1]: one\r\nSep  1 00:00:01 h a[1]: two\rSep  1 00:00:02 h a[1]: x\n"
    assert run_petit("--hash", stdin=text).stdout == analyze_text_output(text)


def analyze_text_output(text: str) -> str:
    return "".join(
        f"{g.count}:\t{g.sample_payloads[0] if g.count <= 3 else g.pattern}\n"
        for g in analyze_text(text, max_samples=1).groups
    )


# --- a pipe longer than the head window --------------------------------------


@pytest.fixture(scope="module")
def big_log(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """About 6 MB: past the 4 MB head window a pipe is held to."""
    path = tmp_path_factory.mktemp("big") / "sshd.log"
    with path.open("w") as handle:
        handle.writelines(sshd_log(60_000))
    assert path.stat().st_size > HEAD_CHARS
    return path


@pytest.mark.parametrize(
    "flags",
    [["--hash"], ["--daemon"], ["--wordcount"], ["--mgraph"], ["--graph"]],
    ids=lambda f: f[0],
)
def test_a_pipe_past_the_head_window_reads_like_the_file(big_log: Path, flags) -> None:
    by_path = run_petit(*flags, str(big_log))
    by_pipe = run_petit(*flags, stdin=big_log.read_text())
    assert by_path.returncode == 0, by_path.stderr
    assert (by_pipe.returncode, by_pipe.stdout) == (0, by_path.stdout)


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_a_tiny_head_window_still_counts_every_line(path: Path, monkeypatch) -> None:
    """With the window forced down to 200 characters every fixture streams
    past its head. Framer and driver come from the head, so only the input
    whose format the head misjudges may group differently — but no line is
    ever lost."""
    text = path.read_text()
    expected = analyze_text(text)
    monkeypatch.setattr("petit.CrunchLog.HEAD_CHARS", 200)
    streamed = analyze_lines(iter(text.splitlines(keepends=True)))
    assert streamed.lines_in == expected.lines_in
    if (streamed.framer, streamed.driver) == (
        expected.framer,
        expected.driver,
    ) and not streamed.degraded:
        assert summary(streamed) == summary(expected)


def test_a_record_the_head_did_not_foresee_is_read_raw(monkeypatch) -> None:
    monkeypatch.setattr("petit.CrunchLog.HEAD_CHARS", 1000)
    lines = [*sshd_log(100), "not a log line at all\n", *sshd_log(10, seed=1)]
    streamed = analyze_lines(iter(lines))
    assert streamed.driver == "SecureLogEntry"
    assert streamed.degraded
    assert streamed.records_grouped == 111
    # A file is re-read with RawEntry throughout, as batch mode always has.
    assert analyze_lines(lines).driver == "RawEntry"


def test_a_one_pass_source_cannot_be_read_twice(monkeypatch) -> None:
    monkeypatch.setattr("petit.CrunchLog.HEAD_CHARS", 100)
    stream = LogStream(source_for(iter(list(sshd_log(20)))))
    assert sum(1 for _ in stream) == 20
    with pytest.raises(PetitError):
        list(stream)


# --- memory ----------------------------------------------------------------

PEAK_SCRIPT = """
import resource, sys
sys.path.insert(0, {test_dir!r})
from test_streaming import sshd_log
from petit.api import analyze_lines
from petit.CrunchLog import LogStream
from petit.LogGraph import fit_graph
from petit.sources import source_for
lines = sshd_log(int(sys.argv[1]))
if sys.argv[2] == "graph":
    LogStream(source_for(lines)).build(lambda log: fit_graph(log, 80))
else:
    analyze_lines(lines, hash_mode=sys.argv[2])
print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
"""


def peak_kb(lines: int, mode: str) -> int:
    script = PEAK_SCRIPT.format(test_dir=str(Path(__file__).parent))
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    result = subprocess.run(
        [sys.executable, "-c", script, str(lines), mode],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    return int(result.stdout)


@pytest.mark.skipif(sys.platform != "linux", reason="ru_maxrss is KB on Linux")
@pytest.mark.parametrize("mode", ["auto", "wordcount", "graph"])
def test_memory_does_not_grow_with_the_input(mode: str) -> None:
    """#38: petit held every line, 1.4 GB for a 96 MB log. Four times the
    input must not cost more than a little more memory: the first 4 MB are
    held as the head window, and past that only groups and samples."""
    small = peak_kb(60_000, mode)
    large = peak_kb(240_000, mode)
    assert large < small * 1.25, (small, large)


# --- the pieces that make streaming exact ----------------------------------


def _old_message_starts(buf: list[str]) -> list[int]:
    """MessageFramer's whole-buffer rule before streaming, as reference."""

    def header_block_at(i: int) -> bool:
        fields, known = 0, False
        for line in buf[i:]:
            match = HEADER_FIELD.match(line)
            if match:
                fields += 1
                known = known or match.group(1).lower() in {
                    "from",
                    "to",
                    "cc",
                    "subject",
                    "date",
                    "message-id",
                    "received",
                    "reply-to",
                    "in-reply-to",
                    "references",
                    "return-path",
                    "mime-version",
                }
            elif not (fields and line[:1] in (" ", "\t")):
                break
        return fields >= 2 and known

    boundary = [i for i in range(len(buf)) if i == 0 or not buf[i - 1].strip()]
    mbox = [i for i in boundary if buf[i].startswith("From ")]
    return mbox if len(mbox) >= 2 else [i for i in boundary if header_block_at(i)]


def test_streamed_message_starts_match_the_whole_buffer_rule() -> None:
    vocab = [
        "From a@b Sat\n",
        "From: x@y\n",
        "Subject: hi\n",
        "X-Foo: 1\n",
        "To: z\n",
        " cont\n",
        "\tcont\n",
        "\n",
        "  \n",
        "body text\n",
        "a: b\n",
    ]
    rng = random.Random(5)
    for _ in range(5000):
        buf = [rng.choice(vocab) for _ in range(rng.randint(0, 30))]
        starts = _old_message_starts(buf)
        assert MessageFramer.claims(buf) == (len(starts) >= 2), buf
        if len(starts) >= 2:
            bounds = [0, *starts] if starts[0] else starts
            assert [r.start for r in MessageFramer.frame(buf)] == bounds, buf


def test_overlapping_header_candidates_stay_linear() -> None:
    """Every whitespace-only line opens a candidate that overlaps the rest;
    grouping them by state keeps this from going quadratic."""
    buf = ["a: b\n", " \n"] * 50_000
    assert not MessageFramer.claims(buf)


def _old_fit_graph(entries: list[LogEntry], columns: int) -> dict[str, int]:
    """--graph before streaming: the range first, then a second pass."""
    earliest, latest = time_range(entries)
    for unit, step in LADDER:
        start = _align(_floor(earliest, unit), unit, step)
        needed = _offset(start, _floor(latest, unit), unit) // step + 1
        if needed <= columns:
            return dict(GRAPH_FOR_UNIT[unit](entries, max(needed, MIN_SPAN), step, earliest))
    unit, step = LADDER[-1]
    return dict(GRAPH_FOR_UNIT[unit](entries, max(columns, MIN_SPAN), step, earliest))


@pytest.mark.parametrize("span_seconds", [50, 3_000, 200_000, 5_000_000, 90_000_000, 2 * 10**9])
@pytest.mark.parametrize("columns", [40, 80, 200])
def test_one_pass_graph_matches_the_two_pass_graph(span_seconds: int, columns: int) -> None:
    rng = random.Random(span_seconds + columns)
    base = datetime.datetime(1970, 3, 7, 11, 22, 33)
    times = [base + datetime.timedelta(seconds=rng.randrange(span_seconds)) for _ in range(3000)]
    times.append(datetime.datetime(1900, 1, 1, 1, 1, 1))
    entries = []
    for when in times:
        entry = LogEntry("")
        entry.year, entry.month, entry.day = (
            f"{when.year:04d}",
            f"{when.month:02d}",
            f"{when.day:02d}",
        )
        entry.hour, entry.minute, entry.second = (
            f"{when.hour:02d}",
            f"{when.minute:02d}",
            f"{when.second:02d}",
        )
        entries.append(entry)
    assert dict(fit_graph(entries, columns)) == _old_fit_graph(entries, columns)


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_one_pass_graph_matches_on_every_fixture(path: Path) -> None:
    log = CrunchLog(str(path))
    assert dict(fit_graph(log, 80)) == _old_fit_graph(list(log), 80)


def test_hash_lines_is_the_groups_of_analyze_lines() -> None:
    lines = list(sshd_log(500))
    assert hash_lines(lines) == analyze_lines(lines).groups


def test_json_lines_still_frame_as_json() -> None:
    lines = [json.dumps({"level": "info", "n": i}) + "\n" for i in range(50)]
    assert analyze_lines(iter(lines)).framer == "json"
