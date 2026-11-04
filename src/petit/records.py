"""Framing: turning lines into records before any driver sees them.

petit used to assume one line is one entry. A JSON array element, an email
in a thread, or a log message with a stack trace under it is not a line, so
framing is its own stage, run before driver selection. A framer surveys
the whole input a line at a time, says whether it claims it, and then cuts
it into Records as the lines stream past a second time.
Every entry driver still receives a string — `record.text` — so a one-line
record is byte-identical to the line every driver has always been given.

Framers are tried in the order of `framers`; LineFramer is last and always
claims, mirroring how RawEntry closes the entry-driver registry.

Everything here reads attacker-controlled text. Claims decline rather than
raise, sizes are capped before parsing, and every regex is linear: character
classes and bounded repetition, no nested quantifiers.
"""

from __future__ import annotations

import json
import re
from bisect import bisect_right
from collections import deque
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from functools import partial
from typing import Any, ClassVar

# JsonFramer declines a buffer larger than this rather than parse it.
MAX_JSON_CHARS = 4_000_000

# JsonFramer declines JSON nested deeper than this. json.loads recurses, and
# so does anything that walks the result.
MAX_JSON_DEPTH = 64

# A JSON string literal, escapes included. The alternatives are disjoint on
# their first character, so matching is linear.
_JSON_STRING = re.compile(r'"(?:[^"\\]|\\.)*"')
_JSON_BRACKET = re.compile(r"[\[\]{}]")


def _skip_whitespace(text: str, idx: int) -> int:
    while idx < len(text) and text[idx].isspace():
        idx += 1
    return idx


@dataclass(frozen=True)
class Record:
    """One unit of input: a line, a JSON object, a message.

    `start` and `end` are 0-based source line numbers, `end` exclusive.
    `lines` hold the record's own text, which for a JSON element on a line
    shared with others is just that element.
    """

    lines: list[str]
    start: int
    end: int

    @property
    def text(self) -> str:
        return "".join(self.lines)


def json_depth_ok(text: str, limit: int = MAX_JSON_DEPTH) -> bool:
    """False when brackets in `text` nest deeper than `limit`.

    Brackets inside string literals don't count. Linear in `text`.
    """
    depth = 0
    for bracket in _JSON_BRACKET.findall(_JSON_STRING.sub("", text)):
        if bracket in "[{":
            depth += 1
            if depth > limit:
                return False
        else:
            depth -= 1
    return True


def parse_json_object(text: str) -> dict[str, Any]:
    """Parse `text` as one JSON object, or raise ValueError.

    Oversized or over-deep input is refused before json.loads sees it, so
    the only exception a caller has to expect is ValueError.
    """
    if len(text) > MAX_JSON_CHARS or not json_depth_ok(text):
        raise ValueError("JSON too large or too deeply nested")
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("not a JSON object")
    return value


def _loads_or_none(text: str) -> Any:
    try:
        return json.loads(text)
    except ValueError:
        return None


@dataclass(frozen=True)
class Claim:
    """A framer's verdict on a whole input: how to cut it into records, and
    how many records that makes."""

    frame: Callable[[Iterable[str]], Iterator[Record]]
    records: int


class Survey:
    """Reads an input one line at a time and decides whether a framer claims it.

    A survey never holds the input, only counters and at most one record's
    lines. That is what lets petit decide how to frame a file of any size in
    one pass and frame it in the next.
    """

    def feed(self, line: str) -> None:
        raise NotImplementedError

    def result(self) -> Claim | None:
        raise NotImplementedError


class Framer:
    """Interface: survey an input, then cut it into records.

    `survey()` makes a fresh Survey, whose Claim cuts the lines it surveyed
    into Records. `records(lines)` cuts lines the way the framer does when
    nothing was surveyed. Both take the input as a stream. `claims()` and
    `frame()` do the same over a list.
    """

    name: ClassVar[str] = ""
    # Entry driver every record from this framer is parsed with, by name,
    # instead of voting. None lets the drivers vote as they always have.
    entry_name: ClassVar[str | None] = None

    survey: ClassVar[type[Survey]] = Survey

    @classmethod
    def records(cls, lines: Iterable[str]) -> Iterator[Record]:
        raise NotImplementedError

    @classmethod
    def claim(cls, buf: Iterable[str]) -> Claim | None:
        survey = cls.survey()
        for line in buf:
            survey.feed(line)
        return survey.result()

    @classmethod
    def claims(cls, buf: list[str]) -> bool:
        return cls.claim(buf) is not None

    @classmethod
    def frame(cls, buf: list[str]) -> list[Record]:
        claim = cls.claim(buf)
        return list(cls.records(buf) if claim is None else claim.frame(buf))


def _json_claims(buf: list[str]) -> bool:
    stripped = "".join(buf).strip()
    if not stripped or stripped[0] not in "[{" or not json_depth_ok(stripped):
        return False
    if stripped[0] == "[":
        value = _loads_or_none(stripped)
        return (
            isinstance(value, list)
            and bool(value)
            and all(isinstance(item, dict) for item in value)
        )
    return all(isinstance(_loads_or_none(line), dict) for line in buf if line.strip())


class _JsonSurvey(Survey):
    """Keeps the input until it passes MAX_JSON_CHARS, then gives up on it."""

    def __init__(self) -> None:
        self.buf: list[str] = []
        self.size = 0
        self.overflow = False

    def feed(self, line: str) -> None:
        if self.overflow:
            return
        self.size += len(line)
        if self.size > MAX_JSON_CHARS:
            self.overflow = True
            self.buf = []
        else:
            self.buf.append(line)

    def result(self) -> Claim | None:
        if self.overflow or not _json_claims(self.buf):
            return None
        return Claim(JsonFramer.records, sum(1 for _ in JsonFramer.records(self.buf)))


class JsonFramer(Framer):
    """A JSON array of objects, or JSON Lines: one object per record.

    Never claims more than MAX_JSON_CHARS, so whatever it frames fits in
    memory and may be joined back into one string.
    """

    name = "json"
    entry_name = "StructuredEntry"

    survey = _JsonSurvey

    @classmethod
    def records(cls, lines: Iterable[str]) -> Iterator[Record]:
        buf = list(lines)
        text = "".join(buf)
        if text.lstrip()[:1] == "[":
            yield from JsonFramer._frame_array(text)
            return
        for i, line in enumerate(buf):
            if line.strip():
                yield Record([line], i, i + 1)

    @staticmethod
    def _frame_array(text: str) -> list[Record]:
        """One record per array element, spanning the lines it sits on."""
        line_starts = [0]
        for match in re.finditer("\n", text):
            line_starts.append(match.end())

        decoder = json.JSONDecoder()
        records = []
        idx = _skip_whitespace(text, 0) + 1
        while True:
            idx = _skip_whitespace(text, idx)
            if text[idx] == "]":
                break
            _value, end = decoder.raw_decode(text, idx)
            first = bisect_right(line_starts, idx) - 1
            last = bisect_right(line_starts, end - 1) - 1
            records.append(Record(text[idx:end].splitlines(keepends=True), first, last + 1))
            idx = _skip_whitespace(text, end)
            if text[idx] != ",":
                break
            idx += 1
        return records


# A header field: a name of printable characters other than colon, then a
# colon. RFC 5322 section 2.2.
HEADER_FIELD = re.compile(r"([!-9;-~]{1,76}):")

# A header block must name at least one of these to count as a message.
_MESSAGE_HEADERS = frozenset(
    {
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
)


class _HeaderStarts:
    """Lines that open a message's header block, found as the lines go by.

    A candidate is the first line or any line after a blank one. It opens a
    message when the header fields from it on — an indented line continues
    a field — number two or more and one of them is a mail header. That is
    only known when the block ends, so starts are confirmed late, but always
    in order.

    Open candidates are grouped by state: fields so far, capped at 2, and
    whether a mail header was seen. Two candidates in the same state see the
    same lines from then on and end the same way, so the work per line stays
    constant however many of them overlap.
    """

    def __init__(self) -> None:
        self.line = 0
        self.after_blank = True
        self.open: dict[tuple[int, bool], list[int]] = {}
        self.pending: deque[int] = deque()
        self.verdict: dict[int, bool] = {}

    def feed(self, line: str) -> list[int]:
        """Take the next line; return the starts it confirmed, in order."""
        if self.after_blank:
            self.open.setdefault((0, False), []).append(self.line)
            self.pending.append(self.line)
        self.line += 1
        self.after_blank = not line.strip()

        match = HEADER_FIELD.match(line)
        continues = line[:1] in (" ", "\t")
        still: dict[tuple[int, bool], list[int]] = {}
        for (seen, named), starts in self.open.items():
            fields, known = seen, named
            if match:
                fields = min(fields + 1, 2)
                known = known or match.group(1).lower() in _MESSAGE_HEADERS
            elif not (fields and continues):
                self._decide(starts, fields >= 2 and known)
                continue
            if fields >= 2 and known:
                # More fields cannot undo it.
                self._decide(starts, True)
                continue
            # Hand the list over rather than copy it: in the worst case one
            # state holds nearly every candidate, line after line.
            merged = still.get((fields, known))
            if merged is None:
                still[(fields, known)] = starts
            else:
                merged.extend(starts)
        self.open = still
        return self._confirmed()

    def finish(self) -> list[int]:
        """End of input: every open block ends here."""
        for (fields, known), starts in self.open.items():
            self._decide(starts, fields >= 2 and known)
        self.open = {}
        return self._confirmed()

    def _decide(self, starts: list[int], verdict: bool) -> None:
        for start in starts:
            self.verdict[start] = verdict

    def _confirmed(self) -> list[int]:
        out = []
        while self.pending and self.pending[0] in self.verdict:
            start = self.pending.popleft()
            if self.verdict.pop(start):
                out.append(start)
        return out


class _MboxStarts:
    """Lines that open an mbox message: `From ` at the start or after a blank line."""

    def __init__(self) -> None:
        self.line = 0
        self.after_blank = True

    def feed(self, line: str) -> list[int]:
        start = self.after_blank and line.startswith("From ")
        self.after_blank = not line.strip()
        self.line += 1
        return [self.line - 1] if start else []

    @staticmethod
    def finish() -> list[int]:
        return []


class _StartCount:
    """How many starts a scanner found, and whether the first was line 0."""

    def __init__(self, scanner: _HeaderStarts | _MboxStarts) -> None:
        self.scanner = scanner
        self.count = 0
        self.first = -1

    def add(self, starts: list[int]) -> None:
        if starts and self.count == 0:
            self.first = starts[0]
        self.count += len(starts)

    def records(self) -> int:
        """Records the starts cut the input into: text before the first
        start is a record of its own."""
        return self.count + (0 if self.first == 0 else 1)


class _MessageSurvey(Survey):
    def __init__(self) -> None:
        self.mbox = _StartCount(_MboxStarts())
        self.headers = _StartCount(_HeaderStarts())

    def feed(self, line: str) -> None:
        for count in (self.mbox, self.headers):
            count.add(count.scanner.feed(line))

    def result(self) -> Claim | None:
        self.headers.add(self.headers.scanner.finish())
        # mbox separators win when there are two; header blocks otherwise.
        for mode, count in (("mbox", self.mbox), ("header", self.headers)):
            if count.count >= 2:
                return Claim(partial(MessageFramer.records, mode=mode), count.records())
        return None


class MessageFramer(Framer):
    """RFC 822 messages: a mail thread or an mbox."""

    name = "message"
    entry_name = "EmailEntry"

    survey = _MessageSurvey

    @classmethod
    def records(cls, lines: Iterable[str], mode: str = "header") -> Iterator[Record]:
        """One record per message; text before the first is a record too.

        A start is confirmed after its header block ends, so the lines since
        the last confirmed start are held until the next one is.
        """
        scanner = _MboxStarts() if mode == "mbox" else _HeaderStarts()
        buf: list[str] = []
        begin = 0
        line_count = 0
        for line in lines:
            buf.append(line)
            line_count += 1
            for start in scanner.feed(line):
                if start > begin:
                    yield Record(buf[: start - begin], begin, start)
                    buf = buf[start - begin :]
                    begin = start
        for start in scanner.finish():
            if start > begin:
                yield Record(buf[: start - begin], begin, start)
                buf = buf[start - begin :]
                begin = start
        yield Record(buf, begin, line_count)


# A multi-line message may run to this many lines. MultilineFramer declines a
# buffer with a longer one rather than build it.
MAX_RECORD_LINES = 1000

# An optional syslog priority, `<34>`, and RFC 5424 version, `<34>1 `.
_PRI = r"(?:<[0-9]{1,3}>(?:[0-9]{1,2} )?)?"
_YMD = r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
_HMS = r"[0-9]{2}:[0-9]{2}:[0-9]{2}"
_LEVEL = r"(?:TRACE|DEBUG|INFO|NOTICE|WARN|WARNING|ERROR|FATAL|CRITICAL|SEVERE)"

# Timestamps a log message can start with, matched at column 0. A record
# starts on a line that begins with one; see MultilineFramer. Every pattern
# is character classes and bounded repeats, so matching is linear.
HEAD_PATTERNS: dict[str, re.Pattern[str]] = {
    name: re.compile(pattern)
    for name, pattern in {
        # Sep 23 10:00:00 — syslog, secure, journalctl -o short / short-precise
        "bsd": _PRI + r"[A-Z][a-z]{2} [ 0-9][0-9] [0-9]{2}:[0-9]{2}:[0-9]{2}",
        # YYYY-MM-DDThh:mm:ss or YYYY-MM-DD hh:mm:ss — RFC 3339/5424, rsyslog,
        # journalctl -o short-iso, Python logging, log4j, Go, Postgres
        "iso": _PRI + _YMD + "[T ]" + _HMS,
        # [YYYY-MM-DD hh:mm:ss — Elasticsearch and many application logs
        "iso_bracket": r"\[" + _YMD + "[T ]" + _HMS,
        # ERROR YYYY-MM-DD hh:mm or [INFO] YYYY-MM-DD hh:mm — level first
        "level_iso": r"\[?" + _LEVEL + r"\]?:? {1,8}\[?" + _YMD + r"[T ][0-9]{2}:[0-9]{2}",
        # YYYY/MM/DD hh:mm:ss — nginx error log, Go's log package
        "slash": r"[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}",
        # [Sun Apr 10 04:04:00 — Apache error log
        "ctime_bracket": r"\[[A-Z][a-z]{2} [A-Z][a-z]{2} [ 0-9][0-9] [0-9]{2}:[0-9]{2}:[0-9]{2}",
        # host ident user [10/Apr/2011:04:04:00 — Apache/nginx access log
        "clf": r"[^ ]{1,255} [^ ]{1,255} [^ ]{1,255} \[[0-9]{2}/[A-Z][a-z]{2}/[0-9]{4}:" + _HMS,
        # 09/29-08:25:54 — Snort alerts
        "snort": r"[0-9]{2}/[0-9]{2}(?:/[0-9]{2})?-[0-9]{2}:[0-9]{2}:[0-9]{2}",
        # I0923 10:00:00.123456 — Kubernetes / glog
        "klog": r"[IWEF][0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{1,9}",
        # [ 1234.567890] — dmesg, journalctl -o short-monotonic
        "kernel": r"\[ {0,12}[0-9]{1,12}\.[0-9]{6}\]",
        # 1789845105.816 — Unix time: squid and some applications
        "epoch": r"[0-9]{10}(?:\.[0-9]{1,9})? ",
        # Mon DD, YYYY h:mm:ss AM — java.util.logging, older Tomcat
        "jul": r"[A-Z][a-z]{2} [0-9]{1,2}, [0-9]{4} [0-9]{1,2}:[0-9]{2}:[0-9]{2} [AP]M",
        # DD-Mon-YYYY hh:mm:ss — Tomcat 8 and later
        "tomcat": r"[0-9]{2}-[A-Z][a-z]{2}-[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}",
        # MM/DD/YYYY hh:mm:ss — US-style dates
        "us_date": r"[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{1,2}:[0-9]{2}:[0-9]{2}",
        # pid:role DD Mon YYYY hh:mm:ss — Redis
        "redis": r"[0-9]{1,10}:[XCSM] [0-9]{2} [A-Z][a-z]{2} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}",
        # 10:00:00.123 or 10:00:00,123 — logback's default layout
        "time_ms": r"[0-9]{2}:[0-9]{2}:[0-9]{2}[.,][0-9]{3}",
    }.items()
}


def _is_journald_marker(line: str) -> bool:
    """`-- Boot 3f2a... --`, `-- No entries --`: journalctl's own notes."""
    text = line.rstrip("\r\n")
    return text.startswith("-- ") and text.endswith(" --")


def _head_pattern(line: str) -> re.Pattern[str] | None:
    for pattern in HEAD_PATTERNS.values():
        if pattern.match(line):
            return pattern
    return None


class _MultilineCutter:
    """Cuts lines into multi-line records, one line at a time.

    A record starts at a line that begins, in column 0, with the timestamp
    format of the first line with content; journald markers end a record
    and belong to none. `cut` caps a record at MAX_RECORD_LINES by starting
    a new one. Without it, a longer record marks the input declined.
    """

    def __init__(self, cut: bool) -> None:
        self.cut = cut
        self.head: re.Pattern[str] | None = None
        self.declined = False
        self.indented = False
        self.line = 0
        self.begin = 0
        self.buf: list[str] = []

    def feed(self, line: str) -> Record | None:
        i = self.line
        self.line += 1
        if self.declined:
            return None
        if self.head is None:
            if line.strip() and not _is_journald_marker(line):
                self.head = _head_pattern(line)
                self.declined = self.head is None
                self.begin, self.buf = i, [line]
            return None

        done = None
        marker = _is_journald_marker(line)
        if marker or self.head.match(line):
            if self.buf:
                done = Record(self.buf, self.begin, i)
            self.begin, self.buf = (i + 1, []) if marker else (i, [line])
        else:
            if line[:1] in (" ", "\t") and line.strip():
                self.indented = True
            self.buf.append(line)
        if i - self.begin >= MAX_RECORD_LINES:
            if not self.cut:
                self.declined = True
                return None
            done = Record(self.buf, self.begin, i + 1)
            self.begin, self.buf = i + 1, []
        return done

    def finish(self) -> Record | None:
        if self.declined or not self.buf:
            return None
        return Record(self.buf, self.begin, self.line)


class _MultilineSurvey(Survey):
    def __init__(self) -> None:
        self.cutter = _MultilineCutter(cut=False)
        self.count = 0

    def feed(self, line: str) -> None:
        if self.cutter.feed(line) is not None:
            self.count += 1

    def result(self) -> Claim | None:
        last = self.cutter.finish()
        cutter = self.cutter
        if cutter.declined or cutter.head is None or not cutter.indented:
            return None
        return Claim(MultilineFramer.records, self.count + (last is not None))


class MultilineFramer(Framer):
    """Log messages that run over several lines: stack traces, tracebacks,
    journalctl's indented continuations.

    A record starts at a line that begins, in column 0, with a timestamp
    from HEAD_PATTERNS, and every line after it that doesn't is part of the
    same record. The timestamp format is fixed by the first record, so a
    continuation line that happens to start with a different kind of time
    stays a continuation.

    Claims only input whose first line with content starts with a
    timestamp, with at least one indented continuation line and no record
    longer than MAX_RECORD_LINES. A log without an indented line frames
    line by line exactly as it always has.
    """

    name = "multiline"

    survey = _MultilineSurvey

    @classmethod
    def records(cls, lines: Iterable[str]) -> Iterator[Record]:
        # Input claimed on its whole length never has an over-long record;
        # the cap only bites when the claim was made on a prefix.
        cutter = _MultilineCutter(cut=True)
        for line in lines:
            record = cutter.feed(line)
            if record is not None:
                yield record
        last = cutter.finish()
        if last is not None:
            yield last

    @classmethod
    def frame(cls, buf: list[str]) -> list[Record]:
        return super().frame(buf) if cls.claims(buf) else []


class _LineSurvey(Survey):
    def __init__(self) -> None:
        self.count = 0

    def feed(self, _line: str) -> None:
        self.count += 1

    def result(self) -> Claim | None:
        return Claim(LineFramer.records, self.count) if self.count else None


class LineFramer(Framer):
    """One record per line. Claims any input with a line in it; the last resort."""

    name = "line"

    survey = _LineSurvey

    @classmethod
    def records(cls, lines: Iterable[str]) -> Iterator[Record]:
        for i, line in enumerate(lines):
            yield Record([line], i, i + 1)


# Tried in order. LineFramer must stay last.
framers: list[type[Framer]] = [JsonFramer, MessageFramer, MultilineFramer, LineFramer]
FRAMER_NAMES = ("auto", *(framer.name for framer in framers))
