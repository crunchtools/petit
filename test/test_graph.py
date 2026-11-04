"""Window arithmetic behind the time graphs."""

from __future__ import annotations

import datetime
from pathlib import Path

import pytest

from petit.CrunchLog import CrunchLog
from petit.LogGraph import (
    GRAPH_FOR_UNIT,
    GRAPHS,
    LADDER,
    MIN_SPAN,
    SENTINEL_YEAR,
    MonthsGraph,
    YearsGraph,
    _align,
    _floor,
    _offset,
    _step,
    fit_graph,
    time_range,
)


def test_months_step_on_the_calendar_across_a_year_boundary() -> None:
    start = datetime.datetime(2025, 11, 1)
    assert [_step(start, "month", i).strftime("%Y-%m") for i in (0, 1, 2, 11)] == [
        "2025-11",
        "2025-12",
        "2026-01",
        "2026-10",
    ]


def test_years_step_on_the_calendar_across_leap_days() -> None:
    start = datetime.datetime(2009, 1, 1)
    assert _step(start, "year", 9) == datetime.datetime(2018, 1, 1)


def _log(text: str) -> CrunchLog:
    return CrunchLog.from_text(text)


APACHE = (
    '127.0.0.1 - - [15/Nov/2025:10:00:00 -0500] "GET / HTTP/1.1" 200 1 "-" "-"\n'
    '127.0.0.1 - - [03/Jan/2026:10:00:00 -0500] "GET / HTTP/1.1" 200 1 "-" "-"\n'
)


def test_month_graph_has_a_bucket_for_every_month() -> None:
    graph = MonthsGraph(_log(APACHE))
    assert len(graph) == 12
    assert graph["202511"] == 1
    assert graph["202601"] == 1
    assert graph.end_date == datetime.datetime(2026, 10, 1)


def test_year_graph_has_a_bucket_for_every_year() -> None:
    graph = YearsGraph(_log(APACHE))
    assert sorted(graph) == [str(y) for y in range(2025, 2035)]


# --- fit_graph(): --graph's choice of column size -------------------------

DATA_DIR = Path(__file__).resolve().parent / "data"
GRAPH_FIXTURES = [DATA_DIR / f"test{i:02d}.log" for i in range(1, 13)]


def _syslog_hours(first: datetime.datetime, hours: int) -> CrunchLog:
    lines = []
    for h in range(hours):
        when = first + datetime.timedelta(hours=h)
        lines.append(when.strftime("%b %d %H:%M:%S") + " host sshd[1]: hello")
    return _log("\n".join(lines) + "\n")


def _real_timestamps(log: CrunchLog) -> int:
    """Entries with a real timestamp, counted without LogGraph."""
    count = 0
    for entry in log:
        try:
            when = datetime.datetime(
                int(entry.year),
                int(entry.month),
                int(entry.day),
                int(entry.hour),
                int(entry.minute),
                int(entry.second),
            )
        except ValueError:
            continue
        count += when.year != SENTINEL_YEAR
    return count


def test_three_and_a_half_days_fit_as_two_hour_columns_on_80() -> None:
    log = _syslog_hours(datetime.datetime(2026, 9, 20, 0, 30), 84)
    graph = fit_graph(log, 80)
    assert (graph.unit, graph.step, len(graph)) == ("hour", 2, 42)
    assert sum(graph.values()) == 84


def test_three_and_a_half_days_fit_as_one_hour_columns_on_120() -> None:
    log = _syslog_hours(datetime.datetime(2026, 9, 20, 0, 30), 84)
    graph = fit_graph(log, 120)
    assert (graph.unit, graph.step, len(graph)) == ("hour", 1, 84)
    assert sum(graph.values()) == 84


@pytest.mark.parametrize("path", GRAPH_FIXTURES, ids=lambda p: p.stem)
def test_fit_graph_counts_every_timestamped_entry(path: Path) -> None:
    log = _log(path.read_text())
    graph = fit_graph(log, 80)
    real = _real_timestamps(log)
    assert sum(graph.values()) == (real or len(log))


@pytest.mark.parametrize("path", GRAPH_FIXTURES, ids=lambda p: p.stem)
def test_fit_graph_takes_the_finest_size_that_fits(path: Path) -> None:
    log = _log(path.read_text())
    graph = fit_graph(log, 80)
    assert MIN_SPAN <= len(graph) <= 80
    rung = LADDER.index((graph.unit, graph.step))
    if rung > 0:
        unit, step = LADDER[rung - 1]
        earliest, latest = time_range(log)
        start = _align(_floor(earliest, unit), unit, step)
        assert _offset(start, _floor(latest, unit), unit) // step + 1 > 80


@pytest.mark.parametrize("path", GRAPH_FIXTURES, ids=lambda p: p.stem)
def test_one_unit_columns_count_like_the_fixed_graphs(path: Path) -> None:
    log = _log(path.read_text())
    for fixed in GRAPHS:
        assert dict(GRAPH_FOR_UNIT[fixed.unit](log, fixed.duration, 1)) == dict(fixed(log))


_dt = datetime.datetime


@pytest.mark.parametrize(
    ("unit", "step", "first", "start"),
    [
        ("minute", 15, _dt(2026, 9, 20, 10, 7, 12), _dt(2026, 9, 20, 10, 0)),
        ("hour", 2, _dt(2026, 9, 20, 13, 40), _dt(2026, 9, 20, 12, 0)),
        ("month", 3, _dt(2026, 5, 17), _dt(2026, 4, 1)),
        ("year", 5, _dt(2027, 3, 1), _dt(2025, 1, 1)),
        ("day", 7, _dt(2026, 9, 20, 13, 40), _dt(2026, 9, 20)),
    ],
)
def test_multi_unit_columns_start_on_round_values(
    unit: str,
    step: int,
    first: datetime.datetime,
    start: datetime.datetime,
) -> None:
    graph = GRAPH_FOR_UNIT[unit](_syslog_hours(first, 1), 10, step, first)
    assert graph.start_date == start
