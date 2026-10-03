"""Text bar graphs of how many log entries fall in each slice of time.

A graph is a row of columns. Each column counts the entries in `step` units
of time, where the unit is one of second, minute, hour, day, month or year.
The window starts at the first entry's timestamp, floored to the unit, and
runs for `duration` columns. When a column spans several units (15 minutes,
2 hours, a quarter) the start is also floored to a multiple of that size, so
columns begin at :00/:15/:30/:45, on even hours, on Jan/Apr/Jul/Oct, and so
on. Days are the exception: a month doesn't divide evenly into 2 or 7 days,
so multi-day columns start on the first entry's day.

The axis under the graph labels the first, middle and last column with the
starting value of that column's unit: second of the minute, minute of the
hour, hour of the day (00-23), day of the month, month (01-12), or the year's
last two digits.

Months and years are stepped on the calendar, never as a fixed number of
days, so every column is exactly one (or `step`) calendar month or year.
"""

from __future__ import annotations

import datetime
import logging
import sys
from collections import Counter, UserDict
from collections.abc import Iterable, Iterator
from itertools import chain
from math import ceil
from typing import TYPE_CHECKING

from .errors import EmptyLogError

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .CrunchLog import LogEntry

# Calendar constants used to size and label graphs.
HOURS_PER_DAY = 24
MONTHS_PER_YEAR = 12
# Not a true calendar constant — how many days DaysGraph shows (roughly a month).
DAYS_GRAPH_WINDOW = 31
# GraphHash.display() prints the year's last two digits on the x-axis.
YEAR_LABEL_MODULUS = 2000
# set_abnormal()/set_blank() stamp unparseable lines with this year.
SENTINEL_YEAR = 1900
# Fewest columns a graph draws: enough room for the begin/middle/end labels.
MIN_SPAN = 6

# Timestamp fields, coarsest first. A graph in unit U buckets on the fields up
# to and including U; everything finer is floored away.
_FIELDS = ("year", "month", "day", "hour", "minute", "second")
# What each field floors to; the year is never floored.
_FLOOR_VALUES = (0, 1, 1, 0, 0, 0)
_SECONDS_IN = {"second": 1, "minute": 60, "hour": 3600, "day": 86400}

# Column sizes fit_graph() tries, finest first. Each unit's multiples are the
# ones that divide its parent evenly (5/15/30 of 60; 2/3/6/12 of 24; 3/6 of
# 12), so aligned columns never straddle a boundary. 7 days is a week; 5 and
# 10 years are what's left once decades are wider than the terminal.
LADDER: tuple[tuple[str, int], ...] = (
    ("second", 1), ("second", 5), ("second", 15), ("second", 30),
    ("minute", 1), ("minute", 5), ("minute", 15), ("minute", 30),
    ("hour", 1), ("hour", 2), ("hour", 3), ("hour", 6), ("hour", 12),
    ("day", 1), ("day", 2), ("day", 7),
    ("month", 1), ("month", 3), ("month", 6),
    ("year", 1), ("year", 5), ("year", 10),
)


def _floor(when: datetime.datetime, unit: str) -> datetime.datetime:
    """`when` with every field finer than `unit` reset: month and day to 1,
    the clock fields to 0."""
    depth = _FIELDS.index(unit) + 1
    year, month, day, hour, minute, second = (
        getattr(when, field) if i < depth else _FLOOR_VALUES[i]
        for i, field in enumerate(_FIELDS)
    )
    return datetime.datetime(year, month, day, hour, minute, second)


def _entry_time(entry: LogEntry, unit: str) -> datetime.datetime:
    """The entry's timestamp floored to `unit`. Raises ValueError when the
    driver left a field that isn't a number or a real date."""
    year, month, day, hour, minute, second = (int(getattr(entry, f)) for f in _FIELDS)
    return _floor(datetime.datetime(year, month, day, hour, minute, second), unit)


def _align(start: datetime.datetime, unit: str, step: int) -> datetime.datetime:
    """Floor `start` to a multiple of `step` units within the parent unit, so
    multi-unit columns begin on round values. Days aren't aligned."""
    if step == 1 or unit == "day":
        return start
    if unit == "year":
        return start.replace(year=start.year - start.year % step)
    if unit == "month":
        return start.replace(month=start.month - (start.month - 1) % step)
    return start - datetime.timedelta(**{unit + "s": getattr(start, unit) % step})


def _step(start: datetime.datetime, unit: str, i: int) -> datetime.datetime:
    """`start` moved forward `i` units, on the calendar for months and years."""
    if unit == "year":
        return start.replace(year=start.year + i)
    if unit == "month":
        months = start.month - 1 + i
        return start.replace(year=start.year + months // MONTHS_PER_YEAR,
                             month=months % MONTHS_PER_YEAR + 1)
    return start + datetime.timedelta(**{unit + "s": i})


def _offset(start: datetime.datetime, when: datetime.datetime, unit: str) -> int:
    """Whole units from `start` to `when`, both already floored to `unit`.
    Negative when `when` is earlier. The inverse of _step()."""
    if unit == "year":
        return when.year - start.year
    if unit == "month":
        return (when.year - start.year) * MONTHS_PER_YEAR + when.month - start.month
    return int((when - start).total_seconds()) // _SECONDS_IN[unit]


def _time_key(when: datetime.datetime, unit: str) -> str:
    # Same shape as the drivers' zero-padded fields joined together, so keys
    # sort in time order.
    return when.strftime("%Y%m%d%H%M%S")[:4 + 2 * _FIELDS.index(unit)]


class GraphHash(UserDict[str, int]):
    """Entry counts per column, keyed by each column's start time.

    Subclasses set the unit and the default number of columns. `duration`
    overrides the number of columns, `step` makes each column span that many
    units, and `start` moves the window off the first entry's timestamp; see
    the module docstring for how the start is floored.
    """

    start_date: datetime.datetime
    # Start of the last column, not the end of the window.
    end_date: datetime.datetime
    middle_date: datetime.datetime
    max_value = 0
    min_value = 0
    scale = 0.0
    tick = "#"
    # Set by the CLI after construction (`x.wide = options.wide`); never
    # mutated by GraphHash itself.
    wide = False
    duration: int = 0
    step = 1
    unit = ""
    _keys: list[str]

    def __init__(
        self,
        log: Iterable[LogEntry],
        duration: int | None = None,
        step: int = 1,
        start: datetime.datetime | None = None,
    ) -> None:
        UserDict.__init__(self)

        entries = iter(log)
        first = next(entries, None)
        if first is None:
            raise EmptyLogError("no entries to graph")

        if start is None:
            start = _entry_time(first, "second")
        self._open(start, duration, step)

        # Entries before the window, after it, or with fields that aren't a
        # real time are left out.
        for entry in chain((first,), entries):
            try:
                when = _entry_time(entry, self.unit)
            except ValueError:
                continue
            self.add(when)

        self.build_calculations()

    @classmethod
    def from_histogram(
        cls, histogram: TimeHistogram, duration: int, step: int, start: datetime.datetime,
    ) -> GraphHash:
        """The graph of entries a TimeHistogram has already counted.

        The histogram's buckets must be no wider than this graph's unit.
        """
        graph = cls.__new__(cls)
        UserDict.__init__(graph)
        graph._open(start, duration, step)
        for when, count in histogram.buckets():
            graph.add(_floor(when, cls.unit), count)
        graph.build_calculations()
        return graph

    def _open(self, start: datetime.datetime, duration: int | None, step: int) -> None:
        """Lay out the columns from `start`, every one zeroed so quiet
        stretches in sparse logs still get drawn."""
        if duration is not None:
            self.duration = duration
        self.step = step
        self.start_date = _align(_floor(start, self.unit), self.unit, step)
        self._keys = []
        for i in range(self.duration):
            self.end_date = _step(self.start_date, self.unit, i * step)
            self._keys.append(_time_key(self.end_date, self.unit))
            self.zero(self._keys[-1])
            if i == self.duration // 2:
                self.middle_date = self.end_date

    def add(self, when: datetime.datetime, count: int = 1) -> None:
        """Count `count` entries at `when`, already floored to the unit."""
        column = _offset(self.start_date, when, self.unit) // self.step
        if 0 <= column < self.duration:
            self[self._keys[column]] += count

    def increment(self, key: str) -> None:
        """Adds new entry. Similar to append method on list"""

        # Check to make sure it exists
        if key not in self:
            self[key] = 0

        # Increment the hashed count
        self[key] += 1

    def zero(self, key: str) -> None:
        """Creates empty entry"""

        # Check to make sure it exists
        if key not in self:
            self[key] = 0

    def build_calculations(self) -> None:
        """Calculates and saves important graph information"""

        # find max value of any key
        for key in list(self.keys()):
            self.max_value = max(self.max_value, self[key])

        # find the minimum value of any key
        self.min_value = self.max_value
        for key in list(self.keys()):
            self.min_value = min(self.min_value, self[key])

    def duration_text(self) -> str:
        """`86 hours (2-hour columns)`, or just `24 hours` for one-unit columns."""
        text = f"{self.duration * self.step} {self.unit}s"
        if self.step > 1:
            text += f" ({self.step}-{self.unit} columns)"
        return text

    def display(self) -> None:
        """Common display function used by all graph subtypes"""

        # Declarations & Variables
        graph_height = 6
        graph_width = len(self)
        scale = float(float(self.max_value - self.min_value) / float(graph_height))
        graph_position: dict[str, int] = {}
        graph_value: dict[str, int] = {}

        # Debug output
        logger.debug("length: %s", graph_width)

        # Use wide scale or small scale
        if self.wide:
            char_fill = self.tick + " "
            char_blank = "  "
        else:
            char_fill = self.tick
            char_blank = " "

        # Calculate the graph min/max, so that the information is better normalized
        graph_max_value = self.max_value

        # Find the real minimum, could very well be zero
        graph_min_value: float = self.max_value
        for key in list(self.keys()):
            graph_min_value = min(graph_min_value, self[key])

        if graph_min_value == 0:

            # Recalculate
            graph_min_value = self.max_value
            for key in list(self.keys()):
                if self[key] < graph_min_value and self[key] != 0:
                    graph_min_value = self[key] / 2

        # Normalize data
        for key in list(self.keys()):
            if self[key] > 0:

                # Ensure difference between min/max or don't normalize
                if graph_max_value > graph_min_value:
                    self[key] = ceil(
                        (float(self[key] - graph_min_value)
                         / float(graph_max_value - graph_min_value)) * graph_height
                    )

                # Normalize because of difference between min/max
                else:
                    self[key] = ceil((float(self[key]) / float(graph_max_value)) * graph_height)

        # Start Graph Printing
        print()

        # Print out the dictionary first sorted by the word with
        # the most entries with an alphabetical subsort
        for i in reversed(list(range(1, graph_height))):
            for key in sorted(self.keys()):

                if self[key] >= i:
                    sys.stdout.write(char_fill)
                else:
                    sys.stdout.write(char_blank)
            print()

        # Print line of '#' charachters at bottom of screen
        for _ in range(len(self)):
            sys.stdout.write(char_fill)
        print()

        if self.wide:

            graph_width = graph_width * 2

            # Calculate Positions
            graph_position["begin"] = 1
            graph_position["middle"] = graph_width // 2 - ((graph_width // 2) % 2)
            graph_position["end"] = graph_width - 3

        else:

            # Calculate Positions
            graph_position["begin"] = 1
            graph_position["middle"] = graph_width // 2
            graph_position["end"] = graph_width - 2

        # Calculate Values
        graph_value["begin"] = getattr(self.start_date, self.unit)
        graph_value["middle"] = getattr(self.middle_date, self.unit)
        graph_value["end"] = getattr(self.end_date, self.unit)

        # Draw numbers at bottom of the screen
        for i in range(1, graph_width):

            # Beginning
            if i == graph_position["begin"]:
                sys.stdout.write(f"{graph_value['begin'] % YEAR_LABEL_MODULUS:02d}")
            # Half
            elif i == graph_position["middle"]:
                sys.stdout.write(f"{graph_value['middle'] % YEAR_LABEL_MODULUS:02d}")
            # Last
            elif i == graph_position["end"]:
                sys.stdout.write(f"{graph_value['end'] % YEAR_LABEL_MODULUS:02d}")
            else:
                sys.stdout.write(" ")
        print()

        print()
        print("Start Time:\t", str(self.start_date), "\t\tMinimum Value:", self.min_value)
        print("End Time:\t", str(self.end_date), "\t\tMaximum Value:", self.max_value)
        print("Duration:\t", self.duration_text(), "\t\t\tScale:", str(scale))
        print()


class SecondsGraph(GraphHash):
    """--sgraph: 60 one-second columns from the first entry."""
    unit = "second"
    duration = 60


class MinutesGraph(GraphHash):
    """--mgraph: 60 one-minute columns from the first entry."""
    unit = "minute"
    duration = 60


class HoursGraph(GraphHash):
    """--hgraph: 24 one-hour columns from the first entry."""
    unit = "hour"
    duration = HOURS_PER_DAY


class DaysGraph(GraphHash):
    """--dgraph: 31 one-day columns from the first entry."""
    unit = "day"
    duration = DAYS_GRAPH_WINDOW


class MonthsGraph(GraphHash):
    """--mograph: 12 one-month columns from the first entry's month."""
    unit = "month"
    duration = MONTHS_PER_YEAR


class YearsGraph(GraphHash):
    """--ygraph: 10 one-year columns from the first entry's year."""
    unit = "year"
    duration = 10


GRAPHS: tuple[type[GraphHash], ...] = (
    SecondsGraph, MinutesGraph, HoursGraph, DaysGraph, MonthsGraph, YearsGraph,
)
GRAPH_FOR_UNIT: dict[str, type[GraphHash]] = {g.unit: g for g in GRAPHS}


def time_range(log: Iterable[LogEntry]) -> tuple[datetime.datetime, datetime.datetime]:
    """The earliest and latest entry timestamps, to the second.

    Logs aren't always in order (rotated files concatenated, or year-less
    syslog stamped with the current year), so this is a scan, not the first
    and last line. Lines stamped with the sentinel year by set_abnormal()
    carry no real time and only count when nothing else does.
    """
    real: list[datetime.datetime] = []
    sentinel: list[datetime.datetime] = []
    for entry in log:
        try:
            when = _entry_time(entry, "second")
        except ValueError:
            continue
        (sentinel if when.year == SENTINEL_YEAR else real).append(when)
    times = real or sentinel
    if not times:
        raise EmptyLogError("no timestamps to graph")
    return min(times), max(times)


class _Buckets:
    """Entry counts per time bucket, the buckets as fine as they can afford.

    Counting starts per second. When there are more distinct buckets than
    `limit(unit)`, the timestamps span more units than any LADDER column
    size at that unit could fit into the graph, so no graph will be drawn
    at that unit and the counts merge into the next unit up. Memory stays
    bounded by the graph's width, not the log's length, and every graph
    that can still be chosen is counted exactly.
    """

    def __init__(self, columns: int) -> None:
        self.unit = "second"
        self.counts: Counter[datetime.datetime] = Counter()
        # N distinct buckets span at least N - 1 units, and a column size of
        # `step` units needs span // step + 1 columns. Years never coarsen.
        widest: dict[str, int] = {}
        for unit, step in LADDER:
            widest[unit] = max(widest.get(unit, 0), step)
        self.limits = {unit: step * columns + 1 for unit, step in widest.items()}
        self.limits["year"] = sys.maxsize

    def add(self, when: datetime.datetime) -> None:
        self.counts[_floor(when, self.unit)] += 1
        while len(self.counts) > self.limits[self.unit]:
            self.unit = _FIELDS[_FIELDS.index(self.unit) - 1]
            merged: Counter[datetime.datetime] = Counter()
            for bucket, count in self.counts.items():
                merged[_floor(bucket, self.unit)] += count
            self.counts = merged


class TimeHistogram:
    """One pass over a log: its time range and entry counts, for fit_graph().

    Lines stamped with the sentinel year by set_abnormal() carry no real
    time. They are counted apart, and only set the range when nothing else
    does, as time_range() rules.
    """

    def __init__(self, columns: int) -> None:
        self.entries = 0
        self.real = _Buckets(columns)
        self.sentinel = _Buckets(columns)
        self.bounds: dict[bool, tuple[datetime.datetime, datetime.datetime]] = {}

    def add(self, entry: LogEntry) -> None:
        self.entries += 1
        try:
            when = _entry_time(entry, "second")
        except ValueError:
            return
        real = when.year != SENTINEL_YEAR
        (self.real if real else self.sentinel).add(when)
        low, high = self.bounds.get(real, (when, when))
        self.bounds[real] = (min(low, when), max(high, when))

    def range(self) -> tuple[datetime.datetime, datetime.datetime]:
        """What time_range() gives for the same log."""
        bounds = self.bounds.get(True) or self.bounds.get(False)
        if bounds is None:
            raise EmptyLogError("no timestamps to graph")
        return bounds

    def buckets(self) -> Iterator[tuple[datetime.datetime, int]]:
        # Sentinel buckets only land inside a graph of real times if the
        # log's real times are near 1900 themselves.
        yield from self.real.counts.items()
        yield from self.sentinel.counts.items()


def fit_graph(log: Iterable[LogEntry], columns: int) -> GraphHash:
    """--graph: the finest column size in LADDER that fits the whole log,
    earliest entry to latest, into `columns`.

    The graph draws only the columns the log covers, with MIN_SPAN as the
    floor. A log too long even for 10-year columns gets `columns` of them.
    One pass: the counts are kept per time bucket while the range is
    found, and the graph is drawn from the buckets.
    """
    histogram = TimeHistogram(columns)
    for entry in log:
        histogram.add(entry)
    if histogram.entries == 0:
        raise EmptyLogError("no entries to graph")
    earliest, latest = histogram.range()
    for unit, step in LADDER:
        start = _align(_floor(earliest, unit), unit, step)
        needed = _offset(start, _floor(latest, unit), unit) // step + 1
        if needed <= columns:
            return GRAPH_FOR_UNIT[unit].from_histogram(
                histogram, max(needed, MIN_SPAN), step, earliest)
    unit, step = LADDER[-1]
    return GRAPH_FOR_UNIT[unit].from_histogram(histogram, max(columns, MIN_SPAN), step, earliest)
