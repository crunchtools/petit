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
from petit import hash_lines, detect_format

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

`analyze_text()` returns the same groups plus how they were produced, and
takes the options the CLI has: `hash_mode` (`"daemon"`, `"host"`,
`"wordcount"`), `collapse_fingerprints`, and `framer`. A JSON array, JSON
Lines, a mail thread, or a log whose messages run over several lines is
grouped per object or per message rather than per line, and the Analysis
accounts for both records and source lines (see
[Reading logs](reading-logs.md)). Normalization is chosen by the driver for
the format unless you pass `filter_name` or `stopwords`.

JSON records that differ only in an identifier are each their own group
unless you pass `max_identifiers=N`: then they group with the identifiers
listed. `Group.identifier_fields` names where they were, as JSON Pointers,
and `Group.identifiers` holds one row of values per record, up to N. A record
past N keeps its identifiers in its fingerprint, so none is dropped.
`pull_identifiers()` does the same to one JSON value, for a caller that
fingerprints JSON its own way.

Text goes in, data comes out. Nothing here reads a file, writes to stdout, or
exits the process. Failures raise `PetitError` subclasses (`EmptyLogError`,
`ParseError`, `DataFileError`) for the caller to handle.

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
from petit import analyze_text

with open("secure") as log:
    analysis = analyze_text(log.read())
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
