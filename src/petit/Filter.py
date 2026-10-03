"""Defines filter class for use with SuperHash"""

from __future__ import annotations

import logging
import os
import re

from .errors import DataFileError
from .resources import search_prefixes

logger = logging.getLogger(__name__)


def parse_rule(line: str) -> tuple[re.Pattern[str], str]:
    """One filter-file line: `regex<TAB>replacement`, or a bare regex.

    A bare regex is replaced with "#", the scrub character petit has always
    used. The tab form lets a file say what it normalised away — "<TS>",
    "<IP>" — the way a caller's (regex, replacement) pairs can.
    """
    pattern, tab, replacement = line.partition("\t")
    return re.compile(pattern), replacement if tab else "#"


class Filter:
    """Filter object used to load filters into memory once, to save on file operations"""

    file = ""
    # Packaged data first, legacy system paths after — see resources.py
    prefixes = search_prefixes("filters")

    # Not a ClassVar: every instance gets its own list, reassigned in
    # __init__/from_patterns before use. This is only the pre-assignment
    # type declaration.
    stopwords: list[tuple[re.Pattern[str], str]]

    @classmethod
    def from_patterns(cls, patterns: list[str | tuple[str, str]]) -> Filter:
        """Build a filter from regexes supplied by the caller.

        Normalisation policy belongs to whoever is reading the output. The
        packaged hash.stopwords is tuned for system logs and is deliberately
        aggressive — `[a-f]+#` collapses the letters next to a scrubbed
        number, so "bob0" and "boa0" land in the same group. That is the
        right trade for spotting a flapping daemon and the wrong one for a
        caller who needs two distinct names to stay distinct.

        Rather than have such a caller ship a file into a package data
        directory to be found by name, let it hand over the patterns.

        Each entry is either a regex, which is replaced with "#" as a file
        would be, or a (regex, replacement) pair. Distinct replacements keep
        a fingerprint legible: "<TS> host sshd[<N>]: login from <IP>" says
        what was normalised away, where "# host sshd[#]: login from #" only
        says that something was.
        """
        instance = cls.__new__(cls)
        instance.file = "<patterns>"
        instance.stopwords = [
            (re.compile(p), "#") if isinstance(p, str)
            else (re.compile(p[0]), p[1])
            for p in patterns
        ]
        return instance

    def __init__(self, file: str = "__none__") -> None:
        self.stopwords = []
        if file == "__none__":
            self.file = file
            return

        for prefix in self.prefixes:
            self.file = prefix + file
            if not os.path.exists(self.file):
                continue
            try:
                with open(self.file) as f:
                    self.stopwords = [parse_rule(line) for line in f.read().splitlines()]
            except OSError as exc:
                raise DataFileError(
                    "could not open filter file " + str(self.file)
                ) from exc
            logger.info("Filter File: %s", self.file)
            return

        # A misspelt filter name used to filter nothing, silently.
        raise DataFileError(
            "could not locate filter file " + file + " in any of: " + ", ".join(self.prefixes)
        )

    def scrub(self, string: str) -> str:
        """Used to remove entries and replace them with the scrub character"""

        # Asked once per call, not once per stopword: scrub runs for every
        # key, and the logging call alone used to cost as much as the regex.
        debug = logger.isEnabledFor(logging.DEBUG)

        # Check each stopword against each key
        for stopword, replacement in self.stopwords:

            # Replace matches with this pattern's replacement
            old_string = string
            string = stopword.sub(replacement, string)
            if debug:
                logger.debug(
                    " SCRUBBING %s OF %s BECOMES %s", old_string, stopword.pattern, string
                )

        return string

    def bleach(self, string: str) -> bool:
        """Determine if a scrub has or should happen"""

        return self.scrub(string) == "#"
