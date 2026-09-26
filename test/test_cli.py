"""CLI integration tests: the exit code contract and output regression.

Runs the real `petit` entry point as a subprocess (not by importing cli.py
directly) so these tests exercise argument parsing exactly as a user would,
and diffs the output against the fixtures in test/data + test/output that
have been part of this repo since 2009 — the safety net for the
optparse-to-argparse migration.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from petit.api import analyze_text

# Syslog/secure-log/snort entries carry no year, so CrunchLog stamps them
# with the current year (see CrunchLog.py's SyslogEntry/SecureLogEntry/
# SnortEntry). The graph fixtures built from those formats bake in whatever
# year they were captured in (e.g. "2022-10-02") and would otherwise fail
# every year going forward — not a regression, just the wall clock moving.
# Normalize 4-digit year-like tokens out of both sides before comparing so
# the fixtures stay useful indefinitely.
_YEAR_RE = re.compile(r"(?<!\d)(19|20)\d{2}(?!\d)")

# --ygraph additionally prints each axis label as the year mod 2000
# (GraphHash.display(): `graph_value["begin"] % 2000`), so for those same
# year-less formats it also carries a 2-digit, wall-clock-derived token that
# _YEAR_RE alone won't catch. ygraph has no other 2-digit content on those
# label lines, so blanking every standalone 2-digit number is safe there —
# it would not be safe for the second/minute/hour/day/month graphs, whose
# 2-digit axis labels are real content (an actual hour or day-of-month) that
# a regression should still be able to break.
_TWO_DIGIT_RE = re.compile(r"(?<!\d)\d{2}(?!\d)")


def _normalize_years(text: str, *, aggressive: bool = False) -> str:
    text = _YEAR_RE.sub("YYYY", text)
    if aggressive:
        text = _TWO_DIGIT_RE.sub("YY", text)
    return text

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

MODES = [
    "hash", "wordcount", "host", "daemon",
    "sgraph", "mgraph", "hgraph", "dgraph", "mograph", "ygraph",
]
HASH_OPTIONS = ["fingerprint", "nosample", "nofilter"]

# test13.log is the empty-log fixture. It has no output fixtures: an empty
# log raises EmptyLogError, which the CLI reports on stderr and turns into
# exit code 1, so there is nothing to capture on stdout. It is exercised
# separately, in test_empty_log_exits_1_with_no_stdout below.
EMPTY_LOG_TEST_ID = "test13"


def run_petit(*args: str, columns: int = 80) -> subprocess.CompletedProcess[str]:
    # COLUMNS pins shutil.get_terminal_size(), which --span checks against.
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), COLUMNS=str(columns))
    return subprocess.run(
        [sys.executable, "-m", "petit.cli", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def _fixture_cases() -> list[tuple[str, list[str], Path]]:
    """One case per test/output/<testNN>-<mode[-option]>.output fixture."""
    cases = []
    for output_file in sorted(OUTPUT_DIR.glob("*.output")):
        test_id, _, rest = output_file.stem.partition("-")
        if rest in MODES:
            cases.append((test_id, [f"--{rest}"], output_file))
            continue
        mode, _, option = rest.partition("-")
        if mode == "hash" and option in HASH_OPTIONS:
            cases.append((test_id, [f"--{mode}", f"--{option}"], output_file))
    return cases


@pytest.mark.parametrize(
    ("test_id", "flags", "output_file"),
    _fixture_cases(),
    ids=[f"{t}-{'-'.join(f.lstrip('-') for f in flags)}" for t, flags, _ in _fixture_cases()],
)
def test_output_matches_fixture(test_id: str, flags: list[str], output_file: Path) -> None:
    data_file = DATA_DIR / f"{test_id}.log"
    result = run_petit(*flags, str(data_file))
    assert result.returncode == 0, result.stderr
    aggressive = "--ygraph" in flags
    assert _normalize_years(result.stdout, aggressive=aggressive) == \
        _normalize_years(output_file.read_text(), aggressive=aggressive)


def test_identifiers_are_listed_under_their_group(tmp_path: Path) -> None:
    records = [{"key": f"PROJ-{n}", "summary": "Nightly build failed"} for n in range(5)]
    data = tmp_path / "issues.json"
    data.write_text(json.dumps(records))
    result = run_petit("--hash", "--nosample", "--identifiers", "10", str(data))
    assert result.returncode == 0, result.stderr
    assert result.stdout == ('5:\t{"key":<ID>,"summary":"Nightly build failed"}\n'
                             "\t/key: PROJ-0, PROJ-1, PROJ-2, PROJ-3, PROJ-4\n")


def test_identifier_field_names_are_escaped(tmp_path: Path) -> None:
    data = tmp_path / "issues.json"
    data.write_text(json.dumps([{"\x1b[2Jk": f"PROJ-{n}"} for n in range(3)]))
    result = run_petit("--hash", "--nosample", "--identifiers", "10", str(data))
    assert result.returncode == 0, result.stderr
    assert "\x1b" not in result.stdout
    assert "/\\u001b[2Jk: PROJ-0, PROJ-1, PROJ-2" in result.stdout


def test_help_exits_0() -> None:
    result = run_petit("--help")
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_unknown_flag_exits_2() -> None:
    result = run_petit("--not-a-real-flag")
    assert result.returncode == 2


def test_too_many_positional_args_exits_2() -> None:
    result = run_petit("--hash", "one.log", "two.log")
    assert result.returncode == 2


def test_missing_file_exits_1() -> None:
    result = run_petit("--hash", str(DATA_DIR / "does-not-exist.log"))
    assert result.returncode == 1
    assert "petit:" in result.stderr


def test_empty_log_exits_1_with_no_stdout() -> None:
    data_file = DATA_DIR / f"{EMPTY_LOG_TEST_ID}.log"
    result = run_petit("--hash", str(data_file))
    assert result.returncode == 1
    assert result.stdout == ""
    assert "no data found" in result.stderr


def test_cli_hash_is_the_library_hash() -> None:
    """The CLI is a shell over petit.api: same text in, same groups out."""
    data_file = DATA_DIR / "test08.log"
    result = run_petit("--hash", "--nosample", str(data_file))
    expected = "".join(
        f"{g.count}:\t{g.pattern}\n" for g in analyze_text(data_file.read_text()).groups
    )
    assert result.stdout == expected


def test_undecodable_file_exits_1(tmp_path: Path) -> None:
    target = tmp_path / "binary.log"
    target.write_bytes(b"\xff\xfe\x00garbage\n")
    result = run_petit("--hash", str(target))
    assert result.returncode == 1
    assert "not valid text" in result.stderr


GRAPH_TEST_IDS = [f"test{i:02d}" for i in range(1, 13)]


def _drawing(stdout: str) -> list[str]:
    """The bar rows, the baseline and the axis labels: everything above the
    blank line that starts the summary."""
    return stdout.strip("\n").split("\n\n")[0].splitlines()


@pytest.mark.parametrize("test_id", GRAPH_TEST_IDS)
@pytest.mark.parametrize("columns", [40, 80, 200])
@pytest.mark.parametrize("wide", [False, True])
def test_graph_fits_the_terminal(test_id: str, columns: int, wide: bool) -> None:
    flags = ["--graph", "--wide"] if wide else ["--graph"]
    result = run_petit(*flags, str(DATA_DIR / f"{test_id}.log"), columns=columns)
    assert result.returncode == 0, result.stderr
    assert all(len(line) <= columns for line in _drawing(result.stdout))


def test_graph_wide_uses_half_the_columns() -> None:
    result = run_petit("--graph", "--wide", str(DATA_DIR / "test09.log"), columns=80)
    assert result.returncode == 0, result.stderr
    # test09 covers 6.5 days: 2- and 3-hour columns need 79 and 53, over 40.
    assert "Duration:\t 162 hours (6-hour columns)" in result.stdout


def test_graph_names_multi_unit_columns() -> None:
    result = run_petit("--graph", str(DATA_DIR / "test05.log"), columns=80)
    assert result.returncode == 0, result.stderr
    assert "(6-hour columns)" in result.stdout


@pytest.mark.parametrize("test_id", GRAPH_TEST_IDS)
@pytest.mark.parametrize(("span", "mode"), [("60s", "sgraph"), ("60m", "mgraph"),
                                            ("24h", "hgraph"), ("31d", "dgraph"),
                                            ("12mo", "mograph"), ("10y", "ygraph")])
def test_span_matching_a_fixed_graph_is_that_graph(test_id: str, span: str, mode: str) -> None:
    data_file = str(DATA_DIR / f"{test_id}.log")
    result = run_petit("--span", span, data_file)
    assert result.returncode == 0, result.stderr
    assert result.stdout == run_petit(f"--{mode}", data_file).stdout


def test_span_draws_one_column_per_unit() -> None:
    result = run_petit("--span", "90m", str(DATA_DIR / "test01.log"), columns=120)
    assert result.returncode == 0, result.stderr
    assert all(len(line) <= 120 for line in _drawing(result.stdout))
    assert "#" * 90 + "\n" in result.stdout
    assert "Duration:\t 90 minutes" in result.stdout


@pytest.mark.parametrize("args", [
    ("--span", "5m"),                 # too few units to label
    ("--span", "3x"),                 # unknown unit
    ("--span", "60m", "--wide"),      # 122 columns on an 80-column terminal
    ("--span", "79m"),                # the axis labels need 81
    ("--hash", "--span", "1h"),       # --span is a graph option
    ("--sgraph", "--span", "1h"),     # and replaces the fixed graphs
])
def test_bad_span_exits_2(args: tuple[str, ...]) -> None:
    result = run_petit(*args, str(DATA_DIR / "test01.log"))
    assert result.returncode == 2
    assert result.stdout == ""


def test_graph_on_empty_log_exits_1() -> None:
    result = run_petit("--graph", str(DATA_DIR / f"{EMPTY_LOG_TEST_ID}.log"))
    assert result.returncode == 1
    assert "petit:" in result.stderr
