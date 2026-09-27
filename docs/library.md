# Library

Everything the `petit` command does is available from Python as the `petit`
package, which is installed alongside the command.

## Why it matters

petit's grouping is useful anywhere text needs to be made shorter without
losing what's unusual in it: a CI job summarising its own logs, a monitoring
check, or an agent that has to read a 50,000-line log and can't afford to.
The library gives that to a program without shelling out.

## How it works

```python
from petit import hash_lines

with open("/var/log/messages") as log:
    for group in hash_lines(log):
        print(group.count, group.pattern)
```

`hash_lines()` groups lines by fingerprint, most frequent first, reading them
one at a time: memory follows the number of groups, not the size of the
input. `hash_text()` and `analyze_text()` do the same for a string already in
memory, and `analyze_lines()` is `analyze_text()` for lines. `detect_format()`
reports which driver claims the text; `"RawEntry"` means no driver
recognised it.

### Functions

| Function | Takes | Returns |
|----------|-------|---------|
| `analyze_text(text, **options)` | a `str` | `Analysis` |
| `analyze_lines(lines, **options)` | any iterable of lines, such as an open file; streams | `Analysis` |
| `hash_text(text, **options)` | a `str` | `list[Group]`, most frequent first |
| `hash_lines(lines, **options)` | any iterable of lines; streams | `list[Group]`, most frequent first |
| `detect_format(text, source_name="<text>", framer="auto")` | a `str` | the name of the driver that claims it; `"RawEntry"` if none does |
| `pull_identifiers(value, max_fields=4)` | one parsed JSON value | `(value with identifiers replaced by IDENTIFIER, their JSON Pointers, their values)` |

The four analysis functions take the same keyword-only options:

| Option | Default | Meaning |
|--------|---------|---------|
| `hash_mode` | `"auto"` | What to group by: `"auto"` fingerprints each record with the hash driver for its format; `"daemon"`, `"host"` and `"wordcount"` are the [reports](reports.md). |
| `collapse_fingerprints` | `False` | Replace each known reboot sequence with one group named after it (`--fingerprint`). |
| `framer` | `"auto"` | `"json"`, `"message"`, `"multiline"` or `"line"`; see [Reading logs](reading-logs.md). |
| `filter_name` | `None` | Packaged stopword file to use. `None` lets the hash driver choose; `"__none__"` turns filtering off. |
| `stopwords` | `None` | Your own list of regexes, or `(regex, replacement)` pairs, used instead of any packaged file. |
| `driver` | `None` | Pin an entry driver by name (e.g. `"RawEntry"`) instead of detecting one. |
| `strict` | `False` | Raise `ParseError` on a record the driver can't read, instead of falling back to RawEntry. |
| `max_samples` | `3` | Real lines kept per group. |
| `max_identifiers` | `0` | For JSON, group records that differ only in an identifier, listing up to this many per group. |
| `max_record_chars` | `4096` | Longest text a fingerprint is built from; bounds the work on hostile input. Samples are never truncated. |
| `source_name` | `"<text>"` / `"<lines>"` | Label used in errors and logging. |

An `Analysis` has `groups`, `driver` (the entry driver used), `degraded`
(True if the driver met a record it couldn't read and RawEntry was used
instead), `framer`, `lines_in`/`lines_grouped`, `records_in`/`records_grouped`,
and `fingerprints_matched`. A `Group` has `pattern`, `count`, `samples`
(real lines, as they appeared), `sample_lines` (their line numbers), and for
JSON with identifiers, `identifier_fields` (JSON Pointers) and `identifiers`
(one row of values per record). A record past `max_identifiers` keeps its
identifiers in its fingerprint, so none is dropped.

Text goes in, data comes out. Nothing here reads a file, writes to stdout, or
exits the process. Failures raise `PetitError` subclasses: `EmptyLogError`
(no data), `ParseError` (only with `strict` or a pinned `driver`), and
`DataFileError` (a `filter_name` that can't be read). An unknown `driver`,
`hash_mode` or `framer` raises `PetitError` itself. Every function's
docstring has the full detail.

### Public API and versioning

petit follows [Semantic Versioning](https://semver.org). Two things are
public and covered by it:

- the `petit` command line, its options and its output
- the names exported from the `petit` package: `analyze_text`,
  `analyze_lines`, `hash_text`, `hash_lines`, `detect_format`,
  `pull_identifiers`, `IDENTIFIER`, `Analysis`, `Group`, and the
  `PetitError` hierarchy

Everything else is internal. The driver classes in `petit.CrunchLog` and the
hash classes in `petit.LogHash` may change in any release; they are where
new log formats get added, and pinning them would freeze that. If you need
something from them, ask for it to be exported rather than importing it
directly.

## Example

```python
from petit import analyze_lines

with open("secure") as log:
    analysis = analyze_lines(log)
print(analysis.driver, analysis.lines_in, "lines ->", len(analysis.groups), "groups")
for group in analysis.groups[:3]:
    print(group.count, group.pattern)
```

```
SecureLogEntry 1500 lines -> 8 groups
537 sshd[#]: Accepted publickey for #
347 sshd[#]: Postponed publickey for #
273 sshd[#]: pam_unix(sshd:session): session opened for #
```

## Related

- [Hashing](hashing.md)
- [Reading logs](reading-logs.md)
- [Install](install.md): the PyPI distribution is `petit-log-crunchtools`
