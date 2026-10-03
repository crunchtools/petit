"""
Reading a log: frame the input into records, pick the entry driver that
parses them, and yield LogEntry objects one at a time.

LogStream does this in bounded memory for input of any size. CrunchLog is
the same thing collected into a list, for callers that want every entry in
hand — the fingerprint corpora, the tests, and code written before petit
streamed.
"""

from __future__ import annotations

import datetime
import io
import logging
import re
import sys
import time
from collections import UserList
from collections.abc import Callable, Iterator
from itertools import chain
from typing import Any, TypeVar

from .errors import EmptyLogError, ParseError, PetitError
from .records import (
    FRAMER_NAMES,
    HEADER_FIELD,
    MAX_JSON_CHARS,
    Claim,
    Framer,
    Record,
    framers,
    parse_json_object,
)
from .sources import ListSource, PathSource, Source, TextSource

logger = logging.getLogger(__name__)

# Bound on how many times select() will resample before giving up and
# using RawEntry. Without a bound, input that no driver claims spins forever.
MAX_SELECT_ROUNDS = 5

# Lines drawn per selection round. Each further round widens the sample.
SAMPLE_LINES_PER_ROUND = 10

# Characters of a record that driver detection looks at. Splitting a 300 KB
# email body into words just to vote on its format is work an attacker can
# buy cheaply; the first 2000 characters are plenty to recognise a format.
DETECT_MAX_CHARS = 2000

# Input that can only be read once — a pipe — is held up to this many
# characters. If it ends inside the window it is read exactly like a file;
# if not, the framer and driver are chosen from this head and the rest
# streams past. The size is MAX_JSON_CHARS because the JSON framer declines
# anything larger anyway, so the head can never pick a different framer
# than the whole input would.
HEAD_CHARS = MAX_JSON_CHARS

# A wall-clock time, HH:MM:SS, with an optional fraction of 1-9 digits:
# `-o short-precise` and RFC 3339 write microseconds, some loggers write
# milliseconds or nanoseconds. The fraction is dropped; petit counts whole
# seconds.
CLOCK = r"([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.[0-9]{1,9})?"

# RFC 3339 as rsyslog and journalctl -o short-iso(-precise) write it:
# 2010-06-24T17:56:32.197716-04:00, ...+05:30, ...Z, or -0400. The offset is
# not applied; times stay the wall clock the host logged.
RFC3339 = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})T" + CLOCK
                     + r"(?:Z|[+-][0-9]{2}:?[0-9]{2})?")

T = TypeVar("T")


def _clock_fields(clocktime: str) -> tuple[str, str, str]:
    """Hour, minute and second of a CLOCK column, fraction dropped."""
    match = re.fullmatch(CLOCK, clocktime)
    if match is None:
        raise ValueError(f"not a clock time: {clocktime!r}")
    hour, minute, second = match.groups()
    return hour, minute, second


def _candidates(name: str) -> list[type[Framer]]:
    if name not in FRAMER_NAMES:
        raise PetitError("unknown framer: " + str(name))
    return [framer for framer in framers if name in ("auto", framer.name)]


def _decide(
    surveyed: list[tuple[type[Framer], Claim | None]], name: str,
) -> tuple[type[Framer], Claim]:
    """The first framer that claimed the input, or the one named.

    A named framer that does not claim the input is an error rather than a
    silent fallback, because the caller said what the input is.
    """
    for framer, claim in surveyed:
        if claim is not None:
            return framer, claim
    if name != "auto":
        raise PetitError(f"the {name} framer does not recognise this input")
    raise RuntimeError("unreachable: LineFramer claims every input")  # pragma: no cover


def select_framer(buf: list[str], name: str = "auto") -> type[Framer]:
    """The framer for `buf`: the first that claims it, or the one named."""
    return _decide([(f, f.claim(buf)) for f in _candidates(name)], name)[0]


def sample_indices(total: int, count: int) -> list[int]:
    """Evenly spaced record numbers across an input of `total` records.

    Deterministic by construction. Selection used to draw with
    random.choice(), which made the driver — and therefore the entire
    output — a function of the RNG as well as the input: the same bytes
    could come back parsed two different ways, or parse cleanly on one call
    and fail on the next. Anything that caches on petit's output, diffs two
    runs, or simply expects a log tool to be reproducible could not rely on
    it.

    Spreading the sample evenly is also better evidence than drawing at
    random, because it is guaranteed to look at the head and the tail. An
    input whose format changes half way through is a real shape, and random
    draws can miss it entirely.
    """
    if count >= total:
        return list(range(total))
    step = total / count
    return [int(i * step) for i in range(count)]


def sample_plan(total: int) -> set[int]:
    """Every record number any round of voting could look at."""
    wanted: set[int] = set()
    for round_number in range(1, MAX_SELECT_ROUNDS + 1):
        wanted.update(sample_indices(total, SAMPLE_LINES_PER_ROUND * round_number))
    return wanted


def vote(total: int, sample: dict[int, list[str]]) -> type[LogEntry]:
    """
    Determines which type of entry to use by sampling the records and using
    a quorum based on votes for each log type. `sample` holds the words of
    every record in sample_plan(total).
    """
    if total < 1:
        return RawEntry

    # This loop used to be `while (1)`, which never terminated when no
    # driver reached quorum — and sample_lines grew on every pass, so it
    # burned memory while it span. A buffer of blank lines does exactly
    # that: an empty split() yields [], and every is_type() rejects an
    # empty list, RawEntry's included, so nothing ever votes.
    #
    # Resampling more than a few times means the input is not giving a
    # clear answer, and more rounds will not change that. Cap it and fall
    # back to RawEntry, which is what the registry already appoints as the
    # last resort.
    for round_number in range(1, MAX_SELECT_ROUNDS + 1):

        # Widen the sample each round rather than accumulating votes on
        # top of the previous round's. The old code reused one Tally and
        # re-counted every line it had ever sampled, so round three
        # weighed the first ten lines three times over.
        indices = sample_indices(total, SAMPLE_LINES_PER_ROUND * round_number)
        sample_lines = [sample[i] for i in indices]

        # Quorum is judged against the lines actually drawn, not the
        # number requested, so a log shorter than the sample size can
        # still satisfy a driver that demands unanimity.
        t = Tally(entry_types, len(sample_lines))

        # Build tallies for the collected samples
        for line in sample_lines:
            for entry_type in entry_types:
                if entry_type.is_type(line):
                    t.append(entry_type)
                    break

        # Tally logic is determined by driver
        for entry_type in entry_types:
            if t.is_type(entry_type):
                logger.info("Determined %s: %s", entry_type.__name__, t.matrix[entry_type])

                return entry_type

        # Already looked at every record; another round sees the same data.
        if len(indices) >= total:
            break

    logger.info("No driver reached quorum after %d rounds; using RawEntry",
                MAX_SELECT_ROUNDS)
    return RawEntry


def _words(record: Record) -> list[str]:
    return record.text[:DETECT_MAX_CHARS].split()


def split_lines(text: str) -> list[str]:
    """Break `text` into lines the way reading a file in text mode does.

    Universal newlines: `\\r\\n` and `\\r` become `\\n`, and nothing else
    ends a line.
    """
    return io.StringIO(text, newline=None).readlines()


def read_source(filename: str) -> str:
    """Text of `filename`, or of stdin when it is "__none__".

    Reads the whole input into memory. petit itself streams instead; see
    petit.sources.
    """
    if filename == "__none__":
        return sys.stdin.read()
    return "".join(PathSource(filename).lines())


class Tally:

    def __init__(self, entry_types: list[type[LogEntry]], max_sample_lines: int) -> None:
        self.matrix: dict[type[LogEntry], int] = {}
        self.max_sample_lines = max_sample_lines
        self.tally_threshold = max_sample_lines / 4

        for entry_type in entry_types:
            self.matrix[entry_type] = 0

    def append(self, entry_type: type[LogEntry]) -> None:
        self.matrix[entry_type] += 1

    def is_type(self, entry_type: type[LogEntry]) -> bool:

        # Setup the correct tally logic method
        tally_logic = entry_type.tally_logic

        m = self.matrix[entry_type]
        th = self.tally_threshold
        msl = self.max_sample_lines

        return tally_logic(m, th, msl)


class DriverMismatchError(ParseError):
    """The chosen driver met a record it cannot parse part way through.

    LogStream.build() catches it and starts again with RawEntry. Iterating
    a LogStream directly lets it through, as the ParseError it is.
    """


class LogStream:
    """The entries of an input, parsed one record at a time.

    Deciding how to read an input needs the whole of it: a framer claims
    the input or not, and drivers vote on records sampled evenly from head
    to tail. A source that can be read again gets exactly that, in passes:

    1. every framer surveys every line, and the first to claim it wins;
    2. the records voting will look at are collected, and the drivers vote
       (skipped when the framer or the caller names the driver);
    3. iterating the stream frames and parses the input once more.

    Nothing but counters and a sample of records is held, so memory does
    not grow with the input.

    A pipe can be read once. Up to HEAD_CHARS of it is held; if it ends
    there it is read like a file. If not, the framer and the driver are
    chosen from that head and the rest streams past, and a record the
    driver cannot parse is read by RawEntry on its own rather than sending
    the whole input back to be re-read.
    """

    def __init__(
        self,
        source: Source,
        driver: type[LogEntry] | None = None,
        strict: bool = False,
        framer: str = "auto",
    ) -> None:
        self.source = source
        self.source_name = source.name
        self.strict = strict
        self.degraded = False
        self.lines_in = 0
        self.records_in = 0
        self._rest: Iterator[str] | None = None
        self._head: list[str] = []

        candidates = _candidates(framer)
        if not source.rewindable:
            self._take_head()
        if self._rest is None:
            self._framer, self._claim = self._survey(candidates, framer)
        else:
            self._framer, self._claim = _decide(
                [(f, f.claim(self._head)) for f in candidates], framer)
        self.framer = self._framer.name

        # A framer that knows what its records are names their driver; the
        # line framer leaves it to the drivers' vote, as always.
        if driver is not None:
            self.Entry = driver
        elif self._framer.entry_name is not None:
            self.Entry = globals()[self._framer.entry_name]
        else:
            self.Entry = self._select()

    @property
    def payload_type(self) -> str:
        return self.Entry.__name__

    def _take_head(self) -> None:
        """Hold the first HEAD_CHARS of a one-pass source."""
        lines = self.source.lines()
        size = 0
        for line in lines:
            self._head.append(line)
            size += len(line)
            if size > HEAD_CHARS:
                self._rest = lines
                break
        else:
            # It all fit: read it like a file.
            self.source = ListSource(self._head, self.source_name)
            self._head = []
        if not self._head and self._rest is None and not self.source.rewindable:
            raise EmptyLogError("no data found in " + (self.source_name or "input"))

    def _survey(self, candidates: list[type[Framer]], name: str) -> tuple[type[Framer], Claim]:
        surveys = [(f, f.survey()) for f in candidates]
        lines = 0
        for line in self.source.lines():
            lines += 1
            for _framer, survey in surveys:
                survey.feed(line)
        if lines < 1:
            raise EmptyLogError("no data found in " + (self.source_name or "input"))
        return _decide([(f, s.result()) for f, s in surveys], name)

    def _select(self) -> type[LogEntry]:
        """The drivers' vote on records sampled across the whole input."""
        if self._rest is not None:
            records = list(self._claim.frame(self._head))
            plan = sample_plan(len(records))
            return vote(len(records), {i: _words(records[i]) for i in plan})

        total = self._claim.records
        plan = sample_plan(total)
        last = max(plan, default=-1)
        sample: dict[int, list[str]] = {}
        for i, record in enumerate(self._claim.frame(self.source.lines())):
            if i in plan:
                sample[i] = _words(record)
            if i >= last:
                break
        return vote(total, sample)

    def _lines(self) -> Iterator[str]:
        if self._rest is None:
            lines: Iterator[str] = self.source.lines()
        else:
            if not self._head:
                raise PetitError(f"{self.source_name} can only be read once")
            lines = chain(self._head, self._rest)
            self._head = []
        for line in lines:
            self.lines_in += 1
            yield line

    def __iter__(self) -> Iterator[LogEntry]:
        self.lines_in = 0
        self.records_in = 0
        entry_type = self.Entry
        for record in self._claim.frame(self._lines()):
            self.records_in += 1
            text = record.text
            try:
                entry = entry_type(text)
            except (ValueError, TypeError, IndexError):
                entry = self._mismatch(record)
            # Keep the record exactly as it arrived. Every driver normalises
            # while parsing — collapsing runs of whitespace, substituting
            # placeholder dates for formats that carry none — so the parsed
            # fields cannot reconstruct the original. A caller that wants to
            # show a human what was actually in the log needs the bytes.
            entry.raw = text.rstrip("\n")
            entry.line_number = record.start
            entry.span = (record.start, record.end)
            yield entry

    def _mismatch(self, record: Record) -> LogEntry:
        """A record the driver could not parse.

        The driver was chosen from a sample and then applied to every
        record, so one in a different shape used to abort the whole run.
        That is not an exotic input: application logs interleave stack
        traces, and tool output mixes JSON with prose. Dying on line 400 of
        401 serves nobody. `strict` keeps that behaviour for callers that
        would rather hear about it.
        """
        if self.strict or self.Entry is RawEntry:
            raise ParseError(record.start, record.text)
        if self._rest is None:
            raise DriverMismatchError(record.start, record.text)
        # One pass only: this record alone is read structurally.
        self.degraded = True
        return RawEntry(record.text)

    def build(self, consume: Callable[[LogStream], T]) -> T:
        """`consume(self)`, done again with RawEntry if the driver fails.

        Falling back to RawEntry, which parses anything, keeps the run
        going; `degraded` records that the grouping is structural rather
        than format-aware, so the caller can say so.
        """
        try:
            return consume(self)
        except DriverMismatchError as exc:
            logger.info("%s could not parse line %d; falling back to RawEntry",
                        self.Entry.__name__, exc.line_number)
            self.Entry = RawEntry
            self.degraded = True
            return consume(self)


class CrunchLog(UserList["LogEntry"]):
    """
    Every entry of a log, in a list. Reads through LogStream, so it parses
    exactly as petit's streaming paths do; it just keeps what it reads.
    """

    # True when the detected driver could not parse the whole buffer and
    # RawEntry was used instead, so grouping is structural only.
    degraded = False

    Entry: type[LogEntry]
    payload_type: str
    file_name: str
    build_date: datetime.datetime
    # Name of the framer that cut the buffer into records.
    framer = "line"
    # Source lines in the buffer, however many records they made.
    lines_in = 0

    def __init__(self, filename: str = "") -> None:
        UserList.__init__(self)

        if filename == "":
            return
        self._build(PathSource(filename))

    @classmethod
    def from_text(
        cls,
        text: str,
        source_name: str = "<text>",
        driver: type[LogEntry] | None = None,
        strict: bool = False,
        framer: str = "auto",
    ) -> CrunchLog:
        """Build a log from a string already in memory.

        `driver` pins the entry class instead of detecting one. `strict`
        restores the old behaviour of raising when the driver meets a line
        it cannot parse, rather than falling back to RawEntry. `framer`
        names how to cut the text into records; "auto" lets each framer
        claim it in turn.
        """
        log = cls()
        log._build(TextSource(text, source_name), driver=driver, strict=strict, framer=framer)
        return log

    def _build(
        self,
        source: Source,
        driver: type[LogEntry] | None = None,
        strict: bool = False,
        framer: str = "auto",
    ) -> None:
        stream = LogStream(source, driver=driver, strict=strict, framer=framer)
        self.data = stream.build(list)
        self.Entry = stream.Entry
        self.degraded = stream.degraded
        self.framer = stream.framer
        self.lines_in = stream.lines_in
        self.payload_type = stream.payload_type
        self.file_name = stream.source_name
        self.build_date = datetime.datetime.now()

    def select(self, records: list[Record]) -> type[LogEntry]:
        """The drivers' vote on `records`."""
        return vote(len(records), {i: _words(records[i]) for i in sample_plan(len(records))})

    def contains(self, obj: type[LogEntry]) -> bool:
        """Determine what kind of objects are contained in this Log"""
        if len(self) >= 1:
            return isinstance(self[len(self) - 1], obj)
        return False

    def display(self) -> None:
        """Simple display function to show entire log"""
        for entry in self:
            entry.display()

    def subset(self, string: str) -> CrunchLog:
        """Return Log object with subset of entries based on a filter"""

        newlog = CrunchLog()
        for entry in self:
            if re.search(string, entry.log_entry):
                newlog.append(entry)

        return newlog


class LogEntry:
    """Interface class which specifies generic log format for consumption
    by other classes"""
    year = ""
    month = ""
    day = ""
    hour = ""
    minute = ""
    second = ""
    host = ""
    daemon = ""
    log_entry = ""
    # The line exactly as it arrived, set by CrunchLog._parse. Parsing is
    # lossy in every driver, so this is the only faithful copy.
    raw = ""
    # 0-based position in the source buffer, set by CrunchLog._parse.
    # Grouping reorders by definition; this is how a caller gets back to
    # where a line actually was.
    line_number = -1
    # Source lines the entry's record covered: [start, end).
    span = (-1, -1)

    def __init__(self, line: str) -> None:
        """Every concrete driver parses `line` in its own __init__."""

    @staticmethod
    def is_type(line: list[str]) -> bool:
        """Every concrete driver decides whether it claims `line`."""
        raise NotImplementedError

    def display(self) -> None:
        print("Year: ", self.year,
              "Month:", self.month,
              "Day:", self.day,
              "Hour:", self.hour,
              "Minute:", self.minute,
              "Second:", self.second,
              "Host:", self.host,
              "Payload", self.log_entry)

    @staticmethod
    def tally_logic(tally: int, tally_threshold: float, _max_sample_lines: int) -> bool:
        return tally > tally_threshold

    def set_abnormal(self, value: list[str]) -> None:
        (self.year, self.month, self.day, self.hour, self.minute, self.second,
         self.host, self.daemon) = ["1900", "01", "01", "01", "01", "01", "#", "#"]
        self.log_entry = ' '.join(value)

    def set_blank(self) -> None:
        (self.year, self.month, self.day, self.hour, self.minute, self.second,
         self.host, self.daemon) = ["1900", "01", "01", "01", "01", "01", "#", "#"]
        self.log_entry = "#"


class SyslogEntry(LogEntry):
    """Driver for Syslog. Conforms to LogEntry interface class."""

    def __init__(self, line: str) -> None:

        # Split the line up
        value = line.split()

        # Should be normal log entry
        if len(value) >= 5:

            # Syslog does not store year information so, set to current year
            self.year = str(datetime.date.today().year)
            self.month, self.day, clocktime, self.host, self.daemon = value[:5]
            self.log_entry = ' '.join(value[5:])
            self.hour, self.minute, self.second = _clock_fields(clocktime)

            # Convert month to integer
            self.month = str(time.strptime(self.month, "%b")[1])

            # Normalize integers to standard widths and convert to strings
            self.year = f"{int(self.year):04d}"
            self.month = f"{int(self.month):02d}"
            self.day = f"{int(self.day):02d}"
            self.hour = f"{int(self.hour):02d}"
            self.minute = f"{int(self.minute):02d}"
            self.second = f"{int(self.second):02d}"

        # Abnormal log entry
        elif len(value) >= 1:
            self.set_abnormal(value)

        # Blank line, will be sorted out by scrub
        else:
            self.set_blank()

    @staticmethod
    def is_type(line: list[str]) -> bool:
        """Standard function from interface class to determine type"""

        if len(line) < 6:
            return False

        # Look for something similar to: "Feb 29 11:53:08" in first
        # three columns
        return bool(
            re.search("[A-Z][a-z]{2}", line[0])
            and re.search("[0-9][0-9]?", line[1])
            and re.fullmatch(CLOCK, line[2])
            and not (re.search("^pam_", line[5]) or re.search(r"^sshd\[", line[4]))
        )


class RSyslogEntry(LogEntry):
    """Driver for RSyslog. Conforms to LogEntry interface class."""

    def __init__(self, line: str) -> None:

        # Split the line up
        value = line.split()

        # Should be normal log entry
        if len(value) >= 5:

            # 2010-06-24T17:56:32.197716-04:00. This used to split on "-" to
            # find the offset, which only works west of UTC: "+05:30" and "Z"
            # raised, and so did any fraction but six digits (#11).
            stamp = RFC3339.fullmatch(value[0])
            if stamp is None:
                raise ValueError(f"not an RFC 3339 timestamp: {value[0]!r}")
            self.year, self.month, self.day, self.hour, self.minute, self.second = \
                stamp.groups()
            self.host = value[1]
            self.daemon = value[2]
            self.log_entry = ' '.join(value[3:])

            # Normalize integers to standard widths and convert to strings
            self.year = f"{int(self.year):04d}"
            self.month = f"{int(self.month):02d}"
            self.day = f"{int(self.day):02d}"
            self.hour = f"{int(self.hour):02d}"
            self.minute = f"{int(self.minute):02d}"
            self.second = f"{int(self.second):02d}"

        # Abnormal log entry
        elif len(value) >= 1:
            self.set_abnormal(value)

        # Blank line, will be sorted out by scrub
        else:
            self.set_blank()

    @staticmethod
    def is_type(line: list[str]) -> bool:
        """Standard function from interface class to determine type"""

        if len(line) < 1:
            return False

        # A whole RFC 3339 timestamp: "2011-04-04T10:00:00.123+02:00"
        return RFC3339.fullmatch(line[0]) is not None


class ApacheAccessEntry(LogEntry):
    """Driver for Apache Access formatted log files"""

    # Whitespace-separated fields in the Apache combined log format.
    FIELD_COUNT = 12

    def __init__(self, line: str) -> None:

        # Split the line up
        value = line.split()

        # Should be normal log entry
        if len(value) >= self.FIELD_COUNT:
            # Grab major chunks from the line
            (_rhost, _ident, _ruser, apachedate, _junk, _junk2, uri, _protocol,
             _status, _size, _referer, _agent) = value[:self.FIELD_COUNT]
            self.log_entry = uri

            # Split up something that looks like this: [03/Aug/2009:11:53:08
            entry_datetime = apachedate.split(':')
            date = entry_datetime[0]
            self.hour = entry_datetime[1]
            self.minute = entry_datetime[2]
            self.second = entry_datetime[3]
            dmy = date.split('/')
            self.day = re.sub(r"\[", "", dmy[0])
            self.month = dmy[1]
            self.year = dmy[2]
            self.host = uri

            # Convert month to integer
            self.month = str(time.strptime(self.month, "%b")[1])

            # Normalize integers to standard widths and convert to strings
            self.year = f"{int(self.year):04d}"
            self.month = f"{int(self.month):02d}"
            self.day = f"{int(self.day):02d}"
            self.hour = f"{int(self.hour):02d}"
            self.minute = f"{int(self.minute):02d}"
            self.second = f"{int(self.second):02d}"

        # Abnormal log entry
        elif len(value) >= 1:
            self.set_abnormal(value)

        # Blank line, will be sorted out by scrub
        else:
            self.set_blank()

    @staticmethod
    def is_type(line: list[str]) -> bool:
        """Standard function from interface class to determine type"""

        if len(line) < 4:
            return False

        # Look for: "03/Aug/2009:11:53:08" in forth column
        r = "[0-9]{2}/[a-zA-Z]{3}/[0-9]{4}:[0-9{2}:[0-9]{2}:[0-9]{2}"
        return bool(re.search(r, line[3]))


class ApacheErrorEntry(LogEntry):
    """Driver for Apache Error formatted log files"""

    def __init__(self, line: str) -> None:

        # Split the line up
        value = line.split()

        # Should be normal log entry
        if len(value) >= 5:
            # Grab major chunks from the line
            # Split up something that looks like this:
            # [Sat Feb 27 12:16:10 2010]
            _junk, self.month, self.day, clocktime, self.year = value[:5]
            self.log_entry = ' '.join(value[5:])
            self.hour, self.minute, self.second = clocktime.split(":")

            # Convert month to integer
            self.month = str(time.strptime(self.month, "%b")[1])

            # Clean up the year field
            self.year = re.sub(r"\]", "", self.year)

            # Normalize integers to standard widths and convert to strings
            self.year = f"{int(self.year):04d}"
            self.month = f"{int(self.month):02d}"
            self.day = f"{int(self.day):02d}"
            self.hour = f"{int(self.hour):02d}"
            self.minute = f"{int(self.minute):02d}"
            self.second = f"{int(self.second):02d}"

        # Abnormal log entry
        elif len(value) >= 1:
            self.set_abnormal(value)

        # Blank line, will be sorted out by scrub
        else:
            self.set_blank()

    @staticmethod
    def is_type(line: list[str]) -> bool:
        """Standard function from interface class to determine type"""

        if len(line) < 5:
            return False

        # Look for : [Sat Feb 27 12:16:10 2010]
        return bool(
            re.search(r"[\[a-zA-Z]{3}", line[0])
            and re.search("[0-9]{2}:[0-9]{2}:[0-9]{2}", line[3])
            and re.search("[0-9]{4}", line[4])
        )


class SecureLogEntry(LogEntry):
    """Driver for Syslog. Conforms to LogEntry interface class."""

    def __init__(self, line: str) -> None:

        # Split the line up
        value = line.split()

        # Should be normal log entry
        if len(value) >= 5:
            # Syslog does not store year information so, set to current year
            self.year = str(datetime.date.today().year)
            self.month, self.day, clocktime, self.host, self.daemon = value[:5]
            self.log_entry = ' '.join(value[5:])
            self.hour, self.minute, self.second = _clock_fields(clocktime)

            # Convert month to integer
            self.month = str(time.strptime(self.month, "%b")[1])

            # Normalize integers to standard widths
            self.year = f"{int(self.year):04d}"
            self.month = f"{int(self.month):02d}"
            self.day = f"{int(self.day):02d}"
            self.hour = f"{int(self.hour):02d}"
            self.minute = f"{int(self.minute):02d}"
            self.second = f"{int(self.second):02d}"

        # Abnormal log entry
        elif len(value) >= 1:
            self.set_abnormal(value)

        # Blank line, will be sorted out by scrub
        else:
            self.set_blank()

    @staticmethod
    def is_type(line: list[str]) -> bool:
        """Standard function from interface class to determine type"""

        if len(line) < 6:
            return False

        # Look for something similar to: "29 11:53:08" in third column
        return bool(
            re.search("[0-9][0-9]?", line[1])
            and re.fullmatch(CLOCK, line[2])
            and (re.search("^pam_", line[5]) or re.search(r"^sshd\[", line[4]))
        )

    @staticmethod
    def tally_logic(tally: int, _tally_threshold: float, max_sample_lines: int) -> bool:
        """Override tally logic for secure logs"""

        return tally >= max_sample_lines


class RawEntry(LogEntry):
    """
    Driver for Raw log files. Conforms to LogEntry interface class.
    This also allows raw logs to contain all of the correct fields
    to be worked with just like other entries that actually have time
    values
    """

    def __init__(self, line: str) -> None:

        # Split the line up
        value = line.split()

        # Fake the time/date values, put the entire line in the key
        if len(value) >= 1:
            self.set_abnormal(value)

        # Blank line, will be sorted out by scrub
        else:
            self.set_blank()

    @staticmethod
    def is_type(line: list[str]) -> bool:
        """
        Do minimum checking to ensure there is some data
        """

        if len(line) < 1:
            return False

        # Look for any length of text in the line
        return bool(re.search(".+", str(line)))


class StructuredEntry(LogEntry):
    """One JSON object, as cut out by JsonFramer.

    Never claims a record by vote: JsonFramer names it for the records it
    produces, and a caller can pin it. `document` is the parsed object.
    """

    document: dict[str, Any]

    def __init__(self, line: str) -> None:
        self.document = parse_json_object(line)
        self.set_abnormal(line.split())

    @staticmethod
    def is_type(_line: list[str]) -> bool:
        return False


class EmailEntry(LogEntry):
    """One RFC 822 message, as cut out by MessageFramer.

    Never claims a record by vote: MessageFramer names it for the records it
    produces. `header_names` are the field names in the header block, lower
    case, in order; `body_lines` are everything after it.
    """

    header_names: list[str]
    body_lines: list[str]

    def __init__(self, line: str) -> None:
        lines = line.splitlines()
        # An mbox separator line precedes the headers
        i = 1 if lines and lines[0].startswith("From ") else 0
        names = []
        while i < len(lines) and lines[i].strip():
            match = HEADER_FIELD.match(lines[i])
            if match:
                names.append(match.group(1).lower())
            elif lines[i][:1] not in (" ", "\t"):
                break
            i += 1
        self.header_names = names
        self.body_lines = lines[i:]
        value = line.split()
        if value:
            self.set_abnormal(value)
        else:
            self.set_blank()

    @staticmethod
    def is_type(_line: list[str]) -> bool:
        return False


class SnortEntry(LogEntry):
    """
    Driver for Snort formatted log files. Conforms to LogEntry interface class.
    """

    def __init__(self, line: str) -> None:

        # Split the line up
        value = line.split()

        # Should be normal log entry
        if len(value) >= 2:

            # Snort does not store year information so, set to current year
            self.year = str(datetime.date.today().year)

            # Initial break down
            snortdate_parts = value[:1]
            self.log_entry = ' '.join(value[1:])

            # Looks like "09/29-10:18:46.026172"
            snortdate, _junk = snortdate_parts[0].split('.')

            # Looks like "09/29-10:18:46"
            self.month, snortdate = snortdate.split('/')

            # Looks like "29-10:18:46"
            self.day, snortdate = snortdate.split('-')

            # Looks like "10:18:46"
            self.hour, self.minute, self.second = snortdate.split(':')

            # Normalize integers to standard widths and convert to strings
            self.year = f"{int(self.year):04d}"
            self.month = f"{int(self.month):02d}"
            self.day = f"{int(self.day):02d}"
            self.hour = f"{int(self.hour):02d}"
            self.minute = f"{int(self.minute):02d}"
            self.second = f"{int(self.second):02d}"

        # Abnormal value
        elif len(value) >= 1:
            self.set_abnormal(value)

        # Blank line, will be sorted out by scrub
        else:
            self.set_blank()

    @staticmethod
    def is_type(line: list[str]) -> bool:

        if len(line) < 4:
            return False

        # Look for : "09/29-10:18:46.026172" in first column
        r = r"[0-9]{2}\/[0-9]{2}\-[0-9]{2}\:[0-9]{2}\:[0-9]{2}\.[0-9]{6}"
        return bool(re.search(r, line[0]))


# Automatically load a list of drivers for each file type this will be used
# to determine what kind of log it is. Do NOT append the parent LogEntry and
# append RawEntry to the end to preserve last resort logic
_module_attrs: dict[str, object] = sys.modules[__name__].__dict__
entry_types: list[type[LogEntry]] = []

for _name in list(_module_attrs.keys()):
    _candidate = _module_attrs[_name]
    if isinstance(_candidate, type) and issubclass(_candidate, LogEntry) \
            and _candidate is not LogEntry and _candidate is not RawEntry:
        entry_types.append(_candidate)

entry_types.append(RawEntry)
