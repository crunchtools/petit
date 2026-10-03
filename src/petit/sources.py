"""Where lines come from: a string, a file, a pipe.

petit reads its input as a stream of lines and never holds all of it. Some
inputs can be read again from the start — a file, a string, a list — and
petit reads those in several passes: one to decide how to frame them, one
to pick a driver, one to parse. A pipe can be read once. See LogStream for
what petit does with each.

Lines keep their newline, as iterating a file in text mode gives them, and
every source applies universal newlines: `\\r\\n` and `\\r` end a line.
"""

from __future__ import annotations

import io
import logging
import sys
from collections.abc import Iterable, Iterator, Sequence

from .errors import DataFileError, PetitError

logger = logging.getLogger(__name__)


def _guarded(lines: Iterable[str], name: str) -> Iterator[str]:
    """`lines`, with read errors turned into DataFileError.

    A missing or unreadable file is an ordinary operator mistake, not a
    bug, and it should read like one. Left bare it escapes as a
    PermissionError traceback (reported as issue #16), and bytes that are
    not text escape as a UnicodeDecodeError — which, now that input is
    decoded as it streams, can happen on any line, not just at open.
    """
    # Through a generator of its own: closing this one early — voting stops
    # reading once it has its sample — must not close the caller's file, and
    # `yield from` passes close() on to whatever it iterates.
    try:
        yield from (line for line in lines)
    except OSError as exc:
        raise DataFileError(f"cannot read {name}: {exc.strerror or exc}") from exc
    except UnicodeDecodeError as exc:
        raise DataFileError(f"cannot read {name}: not valid text ({exc.reason})") from exc


class Source:
    """Lines of input. `lines()` starts a pass from the beginning.

    A source that is not `rewindable` gives one pass only.
    """

    name = "<input>"
    rewindable = True

    def lines(self) -> Iterator[str]:
        raise NotImplementedError


class TextSource(Source):
    """A string already in memory."""

    def __init__(self, text: str, name: str = "<text>") -> None:
        self.text = text
        self.name = name

    def lines(self) -> Iterator[str]:
        return iter(io.StringIO(self.text, newline=None))


class ListSource(Source):
    """Lines already in memory, one string each."""

    def __init__(self, lines: Sequence[str], name: str = "<lines>") -> None:
        self.buf = lines
        self.name = name

    def lines(self) -> Iterator[str]:
        return iter(self.buf)


class PathSource(Source):
    """A file, opened afresh for each pass."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.name = path

    def _read(self) -> Iterator[str]:
        logger.debug("Opening File: %s", self.path)
        with open(self.path) as handle:
            yield from handle

    def lines(self) -> Iterator[str]:
        return _guarded(self._read(), self.name)


class HandleSource(Source):
    """An open text stream: rewindable when it can seek, one pass when not."""

    def __init__(self, handle: Iterable[str], name: str = "<stream>") -> None:
        self.handle = handle
        self.name = name
        self.start = -1
        try:
            if isinstance(handle, io.IOBase) and handle.seekable():
                self.start = handle.tell()
        except (OSError, ValueError):
            self.start = -1
        self.rewindable = self.start >= 0
        self.used = False

    def lines(self) -> Iterator[str]:
        if isinstance(self.handle, io.IOBase) and self.rewindable:
            self.handle.seek(self.start)
        elif self.used:
            raise PetitError(f"{self.name} can only be read once")
        self.used = True
        return _guarded(self.handle, self.name)


def source_for(lines: Iterable[str] | Source, name: str = "<lines>") -> Source:
    """The Source for whatever a caller handed over.

    A seekable file, a list or a tuple can be read more than once; any other
    iterable — a pipe, a generator — is read once.
    """
    if isinstance(lines, Source):
        return lines
    if isinstance(lines, str):
        return TextSource(lines, name)
    if isinstance(lines, Sequence):
        return ListSource(lines, name)
    return HandleSource(lines, name)


def open_source(filename: str) -> Source:
    """The CLI's input: `filename`, or stdin when it is "__none__".

    stdin is re-wrapped for universal newlines, which Python's own stdin
    does not apply on POSIX; petit always has. Redirected from a file,
    stdin can seek and is read like one.
    """
    if filename != "__none__":
        return PathSource(filename)
    stdin = io.TextIOWrapper(
        sys.stdin.buffer, encoding=sys.stdin.encoding, errors=sys.stdin.errors, newline=None,
    )
    return HandleSource(stdin, "<stdin>")
