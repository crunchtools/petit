"""Hash drivers: SuperHash and the per-format classes that fingerprint entries.

A hash driver turns each parsed entry into a fingerprint key. It declares
three things and inherits the rest:

- KEY_FIELDS: which LogEntry fields make up the key.
- GENERALIZATIONS: (pattern, replacement) rules for the format's phrases.
- DEFAULT_FILTER: the stopword file used unless the caller supplies one.

The rule for GENERALIZATIONS:

    A generalization is a claim that everything after this phrase is a
    parameter, not a message. Normalize what the FORMAT generated; keep
    what a HUMAN wrote.

Ask two questions of a rule. Does it collapse a token or a phrase?
Token-level rules — timestamps, addresses, hex, PIDs — are always safe; a
token cannot carry a sentence. Phrase-level rules are allowed only when the
tail they swallow is drawn from a bounded, machine-generated vocabulary.
Then: what is the widest thing this rule's `.*` can swallow? If the format
permits free text there, the rule is too wide. docs/internal/drivers.md has more.
"""

from __future__ import annotations

import json
import logging
import os
import re
from collections import UserDict
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, ClassVar

from .CrunchLog import (
    ApacheAccessEntry,
    ApacheErrorEntry,
    CrunchLog,
    EmailEntry,
    LogEntry,
    LogStream,
    RawEntry,
    RSyslogEntry,
    SecureLogEntry,
    SnortEntry,
    StructuredEntry,
    SyslogEntry,
)
from .errors import DataFileError, PetitError
from .Filter import Filter
from .records import MAX_JSON_DEPTH
from .resources import search_prefixes

# Longest text a fingerprint key is built from. Every stopword regex runs
# over the whole key, so an unbounded key is unbounded work; samples and raw
# text are never truncated.
MAX_KEY_CHARS = 4096

# Share of a fingerprint corpus's patterns that must appear before the
# corpus is considered present.
FINGERPRINT_THRESHOLD = 0.31

# Fewest matched patterns that count as evidence. A corpus must match at
# least this many to be present at all, and a winner must hold at least this
# many that a close runner-up cannot produce to be told apart from it. Below
# that, the two are reported together as `a|b` rather than guessed between.
# A corpus smaller than this needs every one of its patterns.
FINGERPRINT_MIN_EVIDENCE = 5

# How close, as a share of the winner's identity score, a runner-up must
# come before it can share the winner's label.
FINGERPRINT_MARGIN = 0.10

# (path, mtime) -> the corpus's fingerprint keys. Parsing the corpora is
# thousands of lines of work; an embedding service asks on every request.
_FINGERPRINT_CACHE: dict[tuple[str, float], frozenset[str]] = {}

# Every loaded corpus's (path, mtime) -> each key's weight. A key's weight
# depends on how many corpora hold it, so it belongs to the whole set, and
# adding or changing one corpus starts a new entry.
_FINGERPRINT_WEIGHTS: dict[tuple[tuple[str, float], ...], dict[str, float]] = {}


@dataclass(frozen=True)
class FingerprintScore:
    """How one corpus fared in the fingerprint vote.

    `detection` is the share of the corpus's patterns found in the input,
    the test for whether its event happened at all. `identity` is how well
    the corpus, and no other, accounts for what was found: a weighted F1 in
    which a pattern shared by many corpora counts for little. Both are taken
    from the last round the corpus stood in, after earlier winners' patterns
    were set aside.
    """

    name: str
    detection: float
    identity: float


def _load_corpora() -> tuple[list[tuple[str, frozenset[str]]], dict[str, float]]:
    """Every fingerprint corpus as (name, keys) by name, and the key weights.

    Every search prefix contributes: the packaged corpora plus any
    site-local .fp files. Where two share a name, the earlier prefix wins.
    Each corpus is hashed by whatever driver claims it, with that driver's
    own default filter.

    A key's weight is 1 / the number of corpora holding it, so a line every
    distribution logs on reboot carries little of the vote and a line only
    one produces carries all of its own.
    """
    prefixes = search_prefixes("fingerprints")
    by_name: dict[str, str] = {}
    for prefix in prefixes:
        if not os.path.isdir(prefix):
            continue
        for name in sorted(os.listdir(prefix)):
            if name.endswith(".fp"):
                by_name.setdefault(name, os.path.join(prefix, name))
    if not by_name:
        raise DataFileError(
            "could not locate fingerprint files in any of: " + ", ".join(prefixes)
        )

    corpora = []
    stamps = []
    for name in sorted(by_name):
        path = by_name[name]
        cache_key = (path, os.path.getmtime(path))
        keys = _FINGERPRINT_CACHE.get(cache_key)
        if keys is None:
            keys = frozenset(SuperHash.manufacture(CrunchLog(path)).keys())
            _FINGERPRINT_CACHE[cache_key] = keys
        corpora.append((name, keys))
        stamps.append(cache_key)

    weights = _FINGERPRINT_WEIGHTS.get(tuple(stamps))
    if weights is None:
        held: dict[str, int] = {}
        for _, keys in corpora:
            for key in keys:
                held[key] = held.get(key, 0) + 1
        weights = {key: 1 / count for key, count in held.items()}
        _FINGERPRINT_WEIGHTS[tuple(stamps)] = weights
    return corpora, weights


def load_fingerprints() -> list[tuple[str, frozenset[str]]]:
    """Every fingerprint corpus as (name, keys), sorted by name.

    Which corpus wins no longer depends on the order they are tried, so the
    order is only for determinism. It used to be largest file first, and
    the first to pass the threshold took the input.
    """
    return _load_corpora()[0]


class SuperHash(UserDict[str, list[Any]]):
    """Interface and parent class for all hash/dict based objects.

    Each key maps to [count, members]. `max_samples` bounds how many member
    entries a key keeps — the first ones seen, so output stays deterministic
    — which is what keeps memory tied to the number of distinct keys rather
    than the size of the input. None keeps them all.

    Alongside, each key tallies the input records it grouped and the source
    lines they covered, so `records_grouped` and `lines_grouped` stay exact
    when the members are not all kept.

    `max_identifiers` above 0 lets a driver that knows where identifiers sit
    (StructuredHash) take them out of the key and list them instead: records
    that differ only in an identifier group together, and every identifier
    is kept, up to that many rows per key. A record that would go past that
    keeps its identifiers in its key instead, so none is ever dropped.
    0 leaves them in the key.
    """

    filter = Filter()
    sample = "none"
    file_name = ""

    # The stopword file this driver normalises with unless the caller says
    # otherwise. The driver knows what noise looks like in its format; the
    # caller does not, so the default belongs here and not in analyze_text.
    DEFAULT_FILTER: ClassVar[str] = "hash.stopwords"

    # Which LogEntry fields, joined by a space, make up the fingerprint.
    KEY_FIELDS: ClassVar[tuple[str, ...]] = ("log_entry",)

    # (pattern, replacement) rules applied to the key before the filter.
    # See the module docstring for what a rule here is allowed to swallow.
    GENERALIZATIONS: ClassVar[list[tuple[re.Pattern[str], str]]] = []

    def __init__(
        self,
        log: Iterable[LogEntry],
        filter_filename: str | Filter | None = None,
        max_key_chars: int = MAX_KEY_CHARS,
        max_samples: int | None = None,
        max_identifiers: int = 0,
    ) -> None:

        # Call parent init
        UserDict.__init__(self)
        self.max_key_chars = max_key_chars
        self.max_samples = max_samples
        self.max_identifiers = max_identifiers
        # key -> (identifier fields, one row of their values per record).
        self.identifiers: dict[str, tuple[tuple[str, ...], list[tuple[str, ...]]]] = {}
        # key -> [records, lines] grouped under it; see account().
        self.grouped: dict[str, list[int]] = {}
        # How each corpus fared the last time fingerprint() ran.
        self.fingerprint_scores: list[FingerprintScore] = []
        # The furthest source line any grouped record has reached.
        self._reach = -1

        # None asks the driver. A caller that supplies its own normalisation
        # policy passes a built Filter instead of the name of one to find.
        if filter_filename is None:
            filter_filename = self.DEFAULT_FILTER
        if isinstance(filter_filename, Filter):
            self.filter = filter_filename
        elif filter_filename != "__none__":
            self.filter = Filter(filter_filename)

        self.fill(log)

    def generalize(self, text: str) -> str:
        """Return `text` with this format's variable phrases collapsed."""
        for pattern, replacement in self.GENERALIZATIONS:
            text = pattern.sub(replacement, text)
        return text

    def key_for(self, entry: LogEntry) -> str:
        """The fingerprint of one entry: its key fields, generalised, then scrubbed.

        Built into a local, never written back. SecureLogHash used to assign
        its generalised payload onto the entry, which destroyed the user
        name and source address for every later reader of the log.
        """
        text = " ".join(getattr(entry, name) for name in self.KEY_FIELDS)
        return self.filter.scrub(self.generalize(text[:self.max_key_chars]))

    def identify(self, entry: LogEntry) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
        """An entry's key, and the identifier fields and values taken out of it.

        Nothing is taken out here: only a driver that can tell an identifier
        from a message overrides this.
        """
        return self.key_for(entry), (), ()

    def fill(self, log: Iterable[LogEntry]) -> None:
        """Group every entry under its fingerprint."""
        for entry in log:
            key, fields, values = self.identify(entry)
            self.increment(key, entry)
            self.account(key, entry)
            if fields:
                self.identifiers.setdefault(key, (fields, []))[1].append(values)

        # An entry that scrubs away to nothing carries no information
        self.pop("#", None)

    def increment(self, key: str, entry: object) -> None:
        """Adds a new entry to superhash data structures.
        Similar to append for a list"""

        # Check to make sure it exists
        if key not in self:
            self[key] = [0, []]

        self[key][0] += 1
        if self.max_samples is None or len(self[key][1]) < self.max_samples:
            self[key][1].append(entry)

    def account(self, key: str, entry: LogEntry) -> None:
        """Count `entry`'s record as grouped under `key`.

        Records arrive in input order, so the lines a record adds are the
        ones past the furthest line reached so far; JSON elements that
        share a line count it once. A record under "#" is dropped, and a
        stand-in for a collapsed fingerprint came from no input.
        """
        start, end = entry.span
        if key == "#" or start < 0:
            return
        tally = self.grouped.setdefault(key, [0, 0])
        tally[0] += 1
        tally[1] += max(0, end - max(start, self._reach))
        self._reach = max(self._reach, end)

    def __delitem__(self, key: str) -> None:
        super().__delitem__(key)
        self.grouped.pop(key, None)
        self.identifiers.pop(key, None)

    @property
    def records_grouped(self) -> int:
        """Input records that ended up in a group."""
        return sum(tally[0] for tally in self.grouped.values())

    @property
    def lines_grouped(self) -> int:
        """Source lines covered by records that ended up in a group."""
        return sum(tally[1] for tally in self.grouped.values())

    def display(self) -> None:
        """Displays all entries held in the SuperHash structure"""

        # Set static sample threshold
        sample_threshold = 3

        # Debugging
        logging.info("Sample Type: " + self.sample)

        # Print out the dictionary first sorted by the word with
        # the most entries with an alphabetical subsort
        for key in sorted(sorted(self.keys()),
                key=lambda k: self[k][0],
                reverse=True):

            # Print all lines as sample
            if self.sample == "all":
                print(str(self[key][0]) + ":\t" + self[key][1][0].log_entry)

            elif self.sample == "none":
                print(str(self[key][0]) + ":\t" + str(key))

            elif self.sample == "threshold":
                # Print sample for small values below/equal to threshold
                if self[key][0] <= sample_threshold:
                    print(str(self[key][0]) + ":\t" +
                    self[key][1][0].log_entry)
                else:
                    print(str(self[key][0]) + ":\t" + str(key))
            else:
                raise PetitError(
                    "unsupported sampling mode: " + str(self.sample)
                )

    def fingerprint(self) -> list[str]:
        """Collapse every known event sequence found in this hash.

        A fingerprint is a corpus of the lines one routine event produces — a
        reboot, say. When a corpus is present, every one of its patterns is
        removed and replaced by a single group named after it, so 600 lines
        of boot noise read as one line and whatever was unusual stands out.

        Corpora of related systems share most of their lines, so presence
        and identity are decided apart. A corpus is present when more than
        FINGERPRINT_THRESHOLD of its patterns, and at least
        FINGERPRINT_MIN_EVIDENCE, are found. Among those present, the one
        that best accounts for the input on its distinctive lines wins (see
        FingerprintScore). A runner-up the winner cannot be told from — it
        scores within FINGERPRINT_MARGIN, the winner holds too few lines it
        lacks, and it is gone once the winner's lines are — shares the
        label, as `a|b`.
        Then the winner's patterns are set aside and the rest vote again,
        so two reboots in one log both collapse, each under its own name.

        Largest corpus first, first past the threshold wins, used to decide
        this: a big corpus claimed its neighbours' reboots and, by removing
        the lines they share, left the right one below the threshold.

        Returns the labels collapsed, in the order they were, so a caller
        can tell "nothing matched" from "not asked". The scores behind them
        are left in `fingerprint_scores`.
        """
        corpora, weights = _load_corpora()
        known = frozenset().union(*(keys for _, keys in corpora))
        consumed: set[str] = set()
        scores: dict[str, FingerprintScore] = {}
        matched: list[str] = []

        def evidence(keys: frozenset[str]) -> int:
            return min(FINGERPRINT_MIN_EVIDENCE, len(keys))

        def present(keys: frozenset[str], gone: set[str]) -> bool:
            live = keys - gone
            hits = sum(1 for key in live if key in self)
            return hits >= evidence(keys) and hits > len(live) * FINGERPRINT_THRESHOLD

        while True:
            found = sum(weights[key] for key in known - consumed if key in self)
            candidates = []
            for name, keys in corpora:
                if not present(keys, consumed):
                    continue
                live = keys - consumed
                hits = frozenset(key for key in live if key in self)
                recall = sum(weights[key] for key in hits) / sum(weights[key] for key in live)
                precision = sum(weights[key] for key in hits) / found
                identity = 2 * precision * recall / (precision + recall)
                scores[name] = FingerprintScore(name, len(hits) / len(live), identity)
                candidates.append((identity, name, keys, hits))
                logging.info("Fingerprint %s: %d of %d patterns, identity %.3f",
                             name, len(hits), len(live), identity)
            if not candidates:
                break

            candidates.sort(key=lambda c: (-c[0], c[1]))
            best, name, keys, hits = candidates[0]
            label = [name]
            gone = set(keys)
            for identity, other, other_keys, _ in candidates[1:]:
                if (identity >= best * (1 - FINGERPRINT_MARGIN)
                        and len(hits - other_keys) < evidence(keys)
                        and not present(other_keys, consumed | keys)):
                    label.append(other)
                    gone |= other_keys
            name = "|".join(sorted(label))

            for key in gone:
                self.pop(key, None)
            consumed |= gone

            # The collapsed group stands for lines that are gone, so its one
            # member is made up here and named after the corpus. It used to
            # be the corpus's own parsed entry with its payload overwritten,
            # which mutated the loaded fingerprint — harmless only while
            # nothing kept the corpus around between calls.
            stand_in = RawEntry(name)
            stand_in.raw = name
            self.increment(name, stand_in)
            matched.append(name)

        self.fingerprint_scores = [scores[name] for name in sorted(scores)]
        return matched

    @staticmethod
    def manufacture(
        log: CrunchLog | LogStream,
        filter: str | Filter | None = None,
        max_key_chars: int = MAX_KEY_CHARS,
        max_samples: int | None = None,
        max_identifiers: int = 0,
    ) -> SuperHash:
        """The hash driver for whatever entry driver parsed `log`."""
        entry_type = getattr(log, "Entry", None)
        if entry_type is None:
            if not isinstance(log, CrunchLog) or len(log) < 1:
                raise PetitError("could not determine what type of objects the log contains")
            entry_type = type(log[-1])
        return hash_for(entry_type)(log, filter, max_key_chars, max_samples, max_identifiers)


class SyslogHash(SuperHash):
    """Syslog and rsyslog: the daemon and its message."""

    KEY_FIELDS: ClassVar[tuple[str, ...]] = ("daemon", "log_entry")


class ApacheLogHash(SuperHash):
    """Apache access and error logs: the request or message."""


class SnortLogHash(SuperHash):
    """Snort alerts: the alert text."""


class SecureLogHash(SuperHash):
    """sshd and PAM entries from a secure/auth log."""

    KEY_FIELDS: ClassVar[tuple[str, ...]] = ("daemon", "log_entry")

    # Each rule collapses the machine-generated tail after a phrase sshd or
    # PAM emits: the host, port or session detail that differs line to line.
    # A user name is chosen by whoever is knocking, so it is kept verbatim:
    # the rule captures exactly one token for it and matches nothing at all
    # if the name has a space in it, rather than swallowing the rest.
    GENERALIZATIONS: ClassVar[list[tuple[re.Pattern[str], str]]] = [
        # Session entries
        (re.compile("session closed for.*"), "session closed for #"),
        (re.compile("session opened for.*"), "session opened for #"),
        # Auth entries
        (re.compile("Accepted publickey for.*"), "Accepted publickey for #"),
        (re.compile("Accepted password for.*"), "Accepted password for #"),
        (re.compile("Postponed publickey for.*"), "Postponed publickey for #"),
        (re.compile(r"Invalid user (\S+) from \S+"), r"Invalid user \1 from #"),
        (re.compile("reverse mapping checking getaddrinfo for.*"),
         "reverse mapping checking getaddrinfo for #"),
        (re.compile("Connection closed by.*"), "Connection closed by #"),
        (re.compile(r"Failed password for invalid user (\S+) from \S+"),
         r"Failed password for invalid user \1 from #"),
        (re.compile(r"Failed password for (\S+) from \S+"), r"Failed password for \1 from #"),
        (re.compile("authentication failure.*"), "authentication failure #"),
        # Misc
        (re.compile("Received disconnect from.*"), "Received disconnect from #"),
        (re.compile("Could not reverse map address.*"), "Could not reverse map address #"),
    ]


class RawLogHash(SuperHash):
    """Text no driver recognised: the whole line, structurally normalised.

    Nothing is known about the format, so nothing format-specific is
    collapsed. strict.stopwords normalises shapes that are unambiguous —
    timestamps, UUIDs, addresses, standalone numbers — and leaves
    identifiers like web01 or PROJ-1234 distinct.
    """

    DEFAULT_FILTER: ClassVar[str] = "strict.stopwords"


class DaemonHash(SyslogHash):
    """Counts entries per daemon."""

    DEFAULT_FILTER: ClassVar[str] = "daemon.stopwords"
    KEY_FIELDS: ClassVar[tuple[str, ...]] = ("daemon",)


class HostHash(SyslogHash):
    """Counts entries per host."""

    DEFAULT_FILTER: ClassVar[str] = "host.stopwords"
    KEY_FIELDS: ClassVar[tuple[str, ...]] = ("host",)


class WordHash(SuperHash):
    """
    Subclass which creates a dictionary of words which may hold value in a given log file
    Date, time, and other common words are excluded from the count.
    """

    DEFAULT_FILTER: ClassVar[str] = "words.stopwords"

    # Distinct words whose scrubbed form is remembered before starting over.
    SCRUB_MEMO = 100_000

    def fill(self, log: Iterable[LogEntry]) -> None:

        # Words are scrubbed as they arrive, so words that scrub to the same
        # key count as one word from the start. Scrubbing runs every
        # stopword regex, so each distinct word is scrubbed once.
        memo: dict[str, str] = {}
        for entry in log:

            # Base the wordcount on the log_entry payload. Keep the entry,
            # not the word, so a group's members are the lines the word
            # appeared in; the record counts as grouped under its first
            # word that survives scrubbing.
            grouped = False
            for whole in entry.log_entry.split():
                word = whole[:self.max_key_chars]
                key = memo.get(word)
                if key is None:
                    if len(memo) >= self.SCRUB_MEMO:
                        memo.clear()
                    key = memo[word] = self.filter.scrub(word)
                self.increment(key, entry)
                if not grouped and key != "#":
                    self.account(key, entry)
                    grouped = True

        # Finally, remove valueless lines
        if "#" in self:
            del self["#"]


# Structured values that are shaped like a parameter whatever their content.
_ISO_TIMESTAMP = re.compile(
    r"\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:[.,]\d{1,9})?)?"
    r"(?:Z|[+-]\d{2}:?\d{2})?)?"
)
_UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")

# Strings up to this length are kept verbatim in a structured fingerprint.
MAX_VERBATIM_STRING = 200

# What an identifier looks like: a numeric string ("10234"), a key
# ("PROJ-1234"), a reference ("#42"), a UUID, or a lowercase hex digest with
# both digits and letters in it (a git SHA). No alternative admits a space,
# so no sentence fits in one. Every repetition is bounded.
_IDENTIFIER = re.compile(
    r"\d{1,20}"
    r"|[A-Za-z][A-Za-z0-9_]{0,31}-\d{1,12}"
    r"|#\d{1,12}"
    r"|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    r"|(?=[0-9a-f]{0,63}[0-9])(?=[0-9a-f]{0,63}[a-f])[0-9a-f]{7,64}"
)
MAX_IDENTIFIER_CHARS = 64

# A record with more identifier fields than this keeps them all in its
# fingerprint. Listing them would make the list the bulk of the record.
MAX_IDENTIFIER_FIELDS = 4

# pull_identifiers visits at most this many values in one record, keys and
# array members counted. A record bigger than that is not a list entry
# worth masking, and walking it would be work an attacker chose.
MAX_IDENTIFIER_NODES = 10_000


class Identifier(str):
    """Stands where an identifier was pulled out of a structured value.

    A str, so a masked value still serializes as JSON (as "<ID>"). canonical()
    knows it by its exact type and writes a bare <ID>, which no JSON string
    can produce, so a record that really says "<ID>" never shares its key.
    """


IDENTIFIER = Identifier("<ID>")


class _DeclinedError(Exception):
    """A value that pull_identifiers leaves as it is."""


def _pointer_token(key: str) -> str:
    return key.replace("~", "~0").replace("/", "~1")


def pull_identifiers(
    value: Any, max_fields: int = MAX_IDENTIFIER_FIELDS,
) -> tuple[Any, tuple[str, ...], tuple[str, ...]]:
    """Take the identifier-shaped strings out of a JSON value.

    Returns (masked, fields, values). `masked` is a copy of `value` with each
    identifier-shaped string replaced by IDENTIFIER; `fields` are where they
    were, as RFC 6901 JSON Pointers, and `values` what they were. Objects are
    walked in sorted key order, and their copies come out in that order, so
    two records with the same shape list their fields in the same order
    whatever order their keys came in.

    Fingerprint `masked` and records that differ only in an identifier share
    a fingerprint; keep `values` and none of those identifiers is lost.
    Group by the fields as well as the fingerprint when the fingerprint is
    not canonical()'s, which marks the masked slots itself.

    Only strings qualify: numbers are the caller's to normalise or not. A
    value with no identifier, more than `max_fields` of them, more than
    MAX_IDENTIFIER_NODES values, or nesting past MAX_JSON_DEPTH comes back
    as it is, with no fields.

    Args:
        value: A value as json.loads returns it. It is not modified.
        max_fields: Most identifiers a value may have and still be masked.

    Returns:
        (masked, fields, values): the masked copy, or `value` itself when
        nothing was taken out; a JSON Pointer per identifier; and the
        identifiers, parallel to `fields`.
    """
    fields: list[str] = []
    values: list[str] = []
    visited = 0

    def walk(node: Any, pointer: str, depth: int) -> Any:
        nonlocal visited
        visited += 1
        if depth > MAX_JSON_DEPTH or visited > MAX_IDENTIFIER_NODES:
            raise _DeclinedError
        # Checked before a list or object is sorted or copied, so a huge one
        # costs nothing to decline.
        if isinstance(node, (dict, list)) and visited + len(node) > MAX_IDENTIFIER_NODES:
            raise _DeclinedError
        if isinstance(node, dict):
            return {key: walk(node[key], pointer + "/" + _pointer_token(str(key)), depth + 1)
                    for key in sorted(node)}
        if isinstance(node, list):
            return [walk(item, f"{pointer}/{idx}", depth + 1) for idx, item in enumerate(node)]
        if type(node) is str and len(node) <= MAX_IDENTIFIER_CHARS \
                and _IDENTIFIER.fullmatch(node):
            if len(fields) >= max_fields:
                raise _DeclinedError
            fields.append(pointer)
            values.append(node)
            return IDENTIFIER
        return node

    try:
        masked = walk(value, "", 0)
    except _DeclinedError:
        return value, (), ()
    if not fields:
        return value, (), ()
    return masked, tuple(fields), tuple(values)


def canonical(value: Any) -> str:
    """A structured value's fingerprint: keys verbatim, values by type.

    Numbers, booleans and nulls become <N>, <B> and <NULL>, and an
    Identifier left by pull_identifiers becomes <ID>; timestamp- and
    UUID-shaped strings become <TS> and <UUID>; a string over 200 characters
    becomes <STR:n>, n its length rounded up to a power of two. Every other
    string is kept exactly. That is where prose lives, and so where an
    injected instruction lives: normalising short strings away would let two
    records that say different things merge, and one of them vanish.

    Object keys are sorted. Arrays become runs of identical element
    fingerprints with their counts, `[<N>*3]`.
    """
    if isinstance(value, dict):
        return "{" + ",".join(
            json.dumps(key) + ":" + canonical(value[key]) for key in sorted(value)
        ) + "}"
    if isinstance(value, list):
        runs: list[list[Any]] = []
        for item in value:
            fingerprint = canonical(item)
            if runs and runs[-1][0] == fingerprint:
                runs[-1][1] += 1
            else:
                runs.append([fingerprint, 1])
        return "[" + ",".join(f"{fp}*{count}" for fp, count in runs) + "]"
    return _canonical_scalar(value)


# Scalars fingerprinted by type alone. Looked up by exact type, so a bool
# is never taken for the int it subclasses.
_SCALAR_TOKENS: dict[type, str] = {
    bool: "<B>", type(None): "<NULL>", int: "<N>", float: "<N>", Identifier: "<ID>",
}

# Strings shaped like a parameter, whatever they say.
_STRING_SHAPES = [(_ISO_TIMESTAMP, "<TS>"), (_UUID, "<UUID>")]


def _canonical_scalar(value: Any) -> str:
    token = _SCALAR_TOKENS.get(type(value))
    return token if token is not None else _canonical_string(str(value))


def _canonical_string(text: str) -> str:
    for shape, token in _STRING_SHAPES:
        if shape.fullmatch(text):
            return token
    if len(text) > MAX_VERBATIM_STRING:
        return f"<STR:{1 << (len(text) - 1).bit_length()}>"
    return json.dumps(text)


class StructuredHash(SuperHash):
    """JSON records: the object's shape, with short strings kept verbatim.

    The type-based rules are complete on their own. hash.stopwords on top
    would mangle key names, so the default filter is none at all.

    With `max_identifiers` set, identifier-shaped strings (see
    pull_identifiers) become <ID> in the key and are listed per group, so
    records that differ only in their keys or IDs group without losing one.
    """

    DEFAULT_FILTER: ClassVar[str] = "__none__"

    # Marks a record kept whole whose key a caller's filter folded into a
    # key that lists identifiers, which must then list every record it holds.
    UNLISTED: ClassVar[str] = " <UNLISTED>"

    def identify(self, entry: LogEntry) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
        document = getattr(entry, "document", None)
        if document is None or self.max_identifiers <= 0:
            return super().identify(entry)
        masked, fields, values = pull_identifiers(document)
        if not fields:
            return self._whole(entry)
        text = canonical(masked)
        key = self.filter.scrub(self.generalize(text))
        listed = self.identifiers.get(key)
        # Keep the record whole, identifiers in its key, when:
        # - its key was cut short and no longer says where its <ID>s are;
        # - a caller's filter folded two shapes into one key, whose rows
        #   must all name the same fields to be read;
        # - the key is full, and masking without listing would delete them.
        if (len(text) > self.max_key_chars
                or (key in self and (listed is None or listed[0] != fields))
                or (listed is not None and len(listed[1]) >= self.max_identifiers)):
            return self._whole(entry)
        return key, fields, values

    def _whole(self, entry: LogEntry) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
        """A record kept whole, out of any key that lists identifiers."""
        whole = self.key_for(entry)
        return (whole + self.UNLISTED if whole in self.identifiers else whole), (), ()

    def key_for(self, entry: LogEntry) -> str:
        document = getattr(entry, "document", None)
        if document is None:
            return super().key_for(entry)
        return self.filter.scrub(self.generalize(canonical(document)[:self.max_key_chars]))


# Leading quote markers on a line, however they are spaced: "> > >", ">>>".
_QUOTE_RUN = re.compile(r"(?:>[ \t]?)+")

# A signature delimiter line (RFC 3676 "-- ", or a bare "--").
_SIGNATURE = re.compile(r"--[ \t]?")


class EmailHash(SuperHash):
    """Email messages: the message's skeleton plus what its author wrote.

    The key is:
    - the header field names present, sorted — never their values, which
      are addresses, dates and IDs;
    - the quote-depth profile: each run of lines at one quote depth, in
      order, so "wrote, then quoted, then quoted deeper" is a shape;
    - whether a signature is present, but not what it says;
    - the unquoted body lines above the signature, token-normalized by
      strict.stopwords and otherwise verbatim.

    A quoted block is format: it repeats what an earlier message already
    said, so only its depth counts. An unquoted body line is human: it is
    never generalized, only its timestamps and numbers normalized, so two
    messages that say different things never share a key.
    """

    DEFAULT_FILTER: ClassVar[str] = "strict.stopwords"

    # No GENERALIZATIONS table: both email rules are structural here. Header
    # values (Message-ID, Date, Received and the rest) never enter the key
    # at all, and a run of ">" markers collapses to its depth, so neither
    # needs a regex that could reach into what the author wrote.

    def key_for(self, entry: LogEntry) -> str:
        names = getattr(entry, "header_names", None)
        if names is None:
            return super().key_for(entry)
        body: list[str] = getattr(entry, "body_lines", [])

        depths: list[int] = []
        written: list[str] = []
        signed = False
        for line in body:
            if _SIGNATURE.fullmatch(line):
                signed = True
                break
            if not line.strip():
                continue
            run = _QUOTE_RUN.match(line)
            depth = run.group(0).count(">") if run else 0
            if not depths or depths[-1] != depth:
                depths.append(depth)
            if depth == 0:
                written.append(" ".join(line.split()))

        skeleton = (
            "headers=" + ",".join(sorted(set(names)))
            + " quotes=" + "-".join(str(d) for d in depths)
            + " signature=" + ("yes" if signed else "no")
        )
        text = " / ".join(written)[:self.max_key_chars]
        return skeleton + " body=" + self.filter.scrub(text)


# Which hash driver fingerprints which entry driver. Looked up along the
# entry class's MRO, so a subclass of a registered entry inherits its hash
# driver instead of silently falling through to the wrong one. Declared here
# rather than on the entry classes to keep CrunchLog free of LogHash imports.
HASH_FOR: dict[type[LogEntry], type[SuperHash]] = {
    SyslogEntry: SyslogHash,
    RSyslogEntry: SyslogHash,
    ApacheAccessEntry: ApacheLogHash,
    ApacheErrorEntry: ApacheLogHash,
    SnortEntry: SnortLogHash,
    SecureLogEntry: SecureLogHash,
    RawEntry: RawLogHash,
    StructuredEntry: StructuredHash,
    EmailEntry: EmailHash,
}


def hash_for(entry_type: type[LogEntry]) -> type[SuperHash]:
    """The hash driver for `entry_type`, falling back to RawLogHash."""
    for klass in entry_type.__mro__:
        if klass in HASH_FOR:
            return HASH_FOR[klass]
    return RawLogHash
