# Writing and tuning petit drivers

petit works in three stages:

1. A **framer** (`petit/records.py`) cuts the text into records: one per
   JSON object, one per email message, one per multi-line log message, or
   one per line.
2. An **entry driver** (`petit/CrunchLog.py`) parses each record, picking
   out timestamp, host, daemon and payload.
3. A **hash driver** (`petit/LogHash.py`) turns each entry into a
   fingerprint. Entries that share a fingerprint are one group.

How aggressive a hash driver is decides what a reader ever gets to see, so
most of this page is about getting that right.

## Framers

Framers are tried in order and the first to claim the whole input wins.
Each framer surveys the input a line at a time and never holds it, so a
file of any size is claimed on all of it; a pipe longer than 4 MB is
claimed on its first 4 MB (see "Big inputs" in
[Reading logs](../reading-logs.md#big-inputs)).
`--framer` or `analyze_text(framer=...)` names one instead.

| Framer    | Claims                                                       | Entry driver      |
|-----------|--------------------------------------------------------------|-------------------|
| `json`    | a JSON array of objects, or every non-blank line an object   | `StructuredEntry` |
| `message` | 2+ RFC 822 header blocks, or 2+ mbox `From ` separators       | `EmailEntry`      |
| `multiline` | timestamped lines with indented continuation lines         | voted, as always  |
| `line`    | anything; always last                                        | voted, as always  |

A header block counts only if it has two or more fields and at least one is
a mail header (`From`, `To`, `Subject`, `Date`, `Message-ID`, …), and it
must start the buffer or follow a blank line. That keeps `key: value` prose
from reading as mail.

A framer that knows what its records are names their entry driver; line
records are still voted on by every registered driver. Detection looks at
only the first 2000 characters of a record (`DETECT_MAX_CHARS`).

### `multiline`

A record starts at a line that begins, in column 0, with a timestamp, and
every line after it that doesn't is part of that record, indented or not.
That covers journalctl's indented continuations, Java's `\tat ...` frames and
unindented `Caused by:` lines, and Python's `Traceback (most recent call
last):` block down to the final `ValueError: ...`.

It claims a buffer only when all of these hold:

1. The first line with content (blank lines and journald markers aside)
   starts with a timestamp from `HEAD_PATTERNS`.
2. At least one continuation line is indented. That is the evidence the
   input really has multi-line messages. Without it the framer declines and
   the buffer is framed line by line, so a log with a stray unparseable line
   (the `#` lines in test01) is never folded into its neighbour. The 2009
   corpus, test01-test13, has no indented lines and frames exactly as before.
3. No record runs past `MAX_RECORD_LINES` (1000). A longer one declines the
   buffer rather than build a record that size.

The timestamp format is fixed by the first record: a continuation line that
happens to start with a different kind of time (a `10:00:00.500` inside an
ISO-dated log) doesn't start a new record. journald's own notes, `-- Boot
... --` and `-- No entries --`, are dropped: they count in `lines_in` but are
in no record.

| Pattern         | Example head                                   | Written by |
|-----------------|------------------------------------------------|------------|
| `bsd`           | `Sep 23 10:00:00`, `<34>Sep 23 10:00:00`        | syslog, secure, journalctl `short`/`short-precise` |
| `iso`           | `2026-09-23T10:00:00`, `2026-09-23 10:00:00,123` | RFC 3339/5424, rsyslog, journalctl `short-iso`, Python logging, log4j/logback, Go, Postgres |
| `iso_bracket`   | `[2026-09-23 10:00:00`                          | Elasticsearch, many application logs |
| `level_iso`     | `ERROR 2026-09-23 10:00`, `[INFO] 2026-09-23 10:00` | level-first application logs |
| `slash`         | `2026/09/23 10:00:00`                           | nginx error log, Go's `log` |
| `ctime_bracket` | `[Sun Apr 10 04:04:00`                          | Apache error log |
| `clf`           | `1.2.3.4 - - [10/Apr/2011:04:04:00`             | Apache/nginx access log |
| `snort`         | `09/29-08:25:54`                                | Snort alerts |
| `klog`          | `I0923 10:00:00.123456`                         | Kubernetes, glog |
| `kernel`        | `[ 1234.567890]`                                | dmesg, journalctl `short-monotonic` |
| `epoch`         | `1789845105.816 `                               | squid, Unix-time logs |
| `jul`           | `Sep 23, 2026 10:00:00 AM`                      | java.util.logging, older Tomcat |
| `tomcat`        | `23-Sep-2026 10:00:00`                          | Tomcat 8+ |
| `us_date`       | `09/23/2026 10:00:00`                           | US-style dates |
| `redis`         | `12345:M 23 Sep 2026 10:00:00`                  | Redis |
| `time_ms`       | `10:00:00.123`, `10:00:00,123`                  | logback's default layout |

To add a format, add a pattern to `HEAD_PATTERNS` anchored at column 0,
using only character classes and bounded repeats (the module's rule for
hostile input), and add its two example heads to
`TestMultilineFramer.HEADS` in `test/test_records.py`; a test fails until
every pattern has them.

The framer only decides where records begin and end. Whether their text can
be read is still the entry drivers' vote: Python or Java
application logs have no driver of their own, so they are grouped as
`RawEntry` records, one per message.

## Timestamps the entry drivers read

| Driver | First columns | Accepts |
|---|---|---|
| `SyslogEntry`, `SecureLogEntry` | `Sep 23 16:55:34 host daemon:` | seconds with an optional 1-9 digit fraction (`16:55:34.125733`, journalctl `-o short-precise`); the year is the current one |
| `RSyslogEntry` | `2026-09-23T16:55:34.125733+02:00 host daemon:` | RFC 3339: any 1-9 digit fraction or none, and an offset of `+hh:mm`, `-hh:mm`, `+hhmm`, `Z` or none (rsyslog, journalctl `-o short-iso` / `short-iso-precise`) |

The whole column has to match (`CLOCK` and `RFC3339` in `CrunchLog.py`), so a
driver is never voted in for a line it can't unpack. Fractions are dropped:
petit counts whole seconds. RFC 3339 offsets are not applied; times are the
wall clock the host logged.

`JsonFramer` declines, rather than raises, above 4,000,000 characters
(`MAX_JSON_CHARS`) or 64 levels of nesting (`MAX_JSON_DEPTH`). Array elements
keep the exact source text as their sample, and `Group.sample_spans` gives the
source lines each covered.

## What a hash driver declares

```python
class SecureLogHash(SuperHash):
    KEY_FIELDS = ("daemon", "log_entry")        # fields joined into the key
    GENERALIZATIONS = [(re.compile(...), "...")]  # format phrases, applied first
    DEFAULT_FILTER = "hash.stopwords"           # stopword file, applied second
```

The key for an entry is its `KEY_FIELDS` joined by a space, with
`GENERALIZATIONS` applied, then scrubbed by the filter. Nothing is ever
written back to the entry.

`DEFAULT_FILTER` is the driver's decision, not the caller's. `analyze_text`
uses it unless the caller passes `filter_name=` or `stopwords=` explicitly;
those still win.

| Hash driver     | KEY_FIELDS               | DEFAULT_FILTER     |
|-----------------|--------------------------|--------------------|
| `SyslogHash`    | `daemon`, `log_entry`    | `hash.stopwords`   |
| `SecureLogHash` | `daemon`, `log_entry`    | `hash.stopwords`   |
| `ApacheLogHash` | `log_entry`              | `hash.stopwords`   |
| `SnortLogHash`  | `log_entry`              | `hash.stopwords`   |
| `RawLogHash`    | `log_entry`              | `strict.stopwords` |
| `StructuredHash`| the parsed JSON object   | none (`__none__`)  |
| `EmailHash`     | the message skeleton     | `strict.stopwords` |
| `DaemonHash`    | `daemon`                 | `daemon.stopwords` |
| `HostHash`      | `host`                   | `host.stopwords`   |

Which hash driver handles which entry driver is the `HASH_FOR` table in
`LogHash.py`, looked up along the entry class's MRO. A subclass of an entry
driver inherits its parent's hash driver. Anything unregistered gets
`RawLogHash`.

Every key is built from at most `max_record_chars` (default 4096) characters
of text, because each stopword rule runs over the whole key. Samples are
never truncated.

### StructuredHash

A JSON record's key is its canonical form: keys verbatim and sorted, values
by type: numbers `<N>`, booleans `<B>`, null `<NULL>`, ISO-8601-shaped
strings `<TS>`, UUID-shaped strings `<UUID>`, strings over 200 characters
`<STR:n>` (n is the length rounded up to a power of two). Arrays become runs
of identical element fingerprints with counts, `[<N>*3]`.

**Strings of 200 characters or fewer stay verbatim.** That is where prose
lives, and so where an injected instruction lives. A driver that normalized
short strings away would let two records that say different things merge,
and one of them would disappear into the other's count.

### EmailHash

An email's key is its skeleton plus what its author wrote:

- the header field names present, sorted, but never their values (addresses,
  dates, `Message-ID`, `Received`);
- the quote-depth profile: each run of lines at one depth, in order, with
  `> > >` and `>>>` both depth 3;
- whether there is a signature (`-- `), but not what it says;
- the unquoted body lines above the signature, normalized by
  `strict.stopwords` and otherwise verbatim.

A quoted block is format: it repeats something already said, so only its
depth counts. An unquoted body line is human, so it is never generalized. Two
replies that both say "Looking now." merge whoever sent them; a reply that
says something else never does.

## The rule for generalizations

> **A generalization is a claim that everything after this phrase is a
> parameter, not a message. Normalize what the FORMAT generated; keep what a
> HUMAN wrote.**

Ask a rule two questions, in order.

1. **Does it collapse a token or a phrase?** Token-level rules (timestamps,
   IP addresses, hex, PIDs) are always safe, because a token cannot carry a
   sentence. Phrase-level rules are allowed only when the tail they swallow is
   drawn from a bounded, machine-generated vocabulary.
2. **What is the widest thing this rule's `.*` can swallow?** If the format
   allows free text there, the rule is too wide.

Applied to sshd: `Invalid user.*` used to swallow the user name and
everything after it. The user name is chosen by whoever is connecting, so it
can hold anything, including text written to be read by whatever reads the
log. The rule is now `Invalid user (\S+) from \S+` → `Invalid user \1 from #`:
the name stays, only the source address goes, and a name with a space in it
doesn't match at all rather than being swallowed.

## Stopword files

Filter files live in `petit/data/filters/`, one rule per line, applied in
order. A line is either a bare regex, replaced with `#`, or
`regex<TAB>replacement`:

```
\b(?:\d{1,3}\.){3}\d{1,3}\b	<IP>
[0-9]+
```

Order matters: put specific shapes before general ones, or a timestamp
becomes six numbers.

- **`hash.stopwords`** is tuned for system logs and is deliberately
  aggressive: after `[0-9]+` → `#`, the rules `[a-f]+#` and `#[a-f]+` also
  collapse hex letters next to a number, so `bob0` and `boa0` share a
  fingerprint. That's right for spotting a flapping daemon, and wrong for
  identifiers. Before the number rule, it collapses values a machine
  generates and that differ per boot or per host: MACs and UUIDs in either
  case, vfat serials (`F96D-44AD`), `0x` hex, and Python-tempfile and snap
  mount names. After it, it collapses decimals and signs. The rules were
  tuned so two reboots of the same image hash alike (see
  `test/test_drivers.py`).
- **`strict.stopwords`** normalizes only unambiguous shapes: ISO-8601, syslog,
  date and time stamps → `<TS>`, UUIDs → `<UUID>`, dotted quads → `<IP>`, `0x`
  hex and hex runs of 8+ containing a letter → `<HEX>`, standalone numbers →
  `<N>`. A number attached to a word or a dash (`web01`, `PROJ-1234`) is part
  of an identifier and stays.
- **`words.stopwords`** is for `--wordcount`, which scrubs each
  whitespace-separated word on its own and drops any word that scrubs to
  `#`. Its English and systemd words are anchored: `(?i)^[^\w#]*the[^\w#]*$`
  drops "The" and "(the)", but not "there" or "the1". An unanchored word
  cuts itself out of longer words ("target" → `tar#`). Unknown words and
  acronyms are never dropped.
- **`daemon.stopwords`** and **`host.stopwords`** scrub a single field. The
  daemon rules drop classic syslog pseudo-daemons (`last` in "last message
  repeated", `--` in "-- MARK --") only as the whole field.

Filter files have no comment syntax, because every line is compiled as a
regex. Document a rule here and pin it with a test.

Every regex in a filter or generalization table must be linear-time: use
character classes and bounded repetition, and no nested quantifiers. petit
runs these over text it didn't write.

## Settling an argument about a driver

`test/test_drivers.py` has one class per hash driver with `MERGE` and
`NO_MERGE` lists of `(line_a, line_b, reason)`. If a driver collapses too
much or too little, add the pair that shows it and change the driver until
the table passes.

## Fingerprint corpora (`--fingerprint`, `collapse_fingerprints=True`)

A fingerprint corpus is a log of one routine event, such as a reboot, stored as
`<name>.fp`. When a corpus is present in the input, every matching group is
removed and replaced by one group named after the corpus.
`Analysis.fingerprints_matched` lists what matched.

Related systems log much of the same reboot, so whether an event happened and
which system logged it are decided separately:

1. **Present.** More than 31% of the corpus's fingerprints appear, and at
   least five of them (or all of them, for a corpus smaller than that).
2. **Identity.** Each fingerprint is weighted 1 / the number of corpora that
   hold it. A present corpus scores a weighted F1: how much of the corpus
   was found, and how much of what was found the corpus accounts for. The
   highest score wins, and ties go to the first name.
3. **Ambiguity.** A runner-up shares the winner's label, as `a|b`, when it
   scores within 10% of the winner, the winner has fewer than five
   fingerprints the runner-up lacks, and the runner-up is no longer present
   once the winner's fingerprints are set aside. That's the case where
   nothing in the input tells them apart.
4. **Repeat.** The winner's fingerprints are removed, and the remaining
   corpora vote again on what is left. A log holding two different reboots
   collapses both.

`Analysis.fingerprint_scores` has each present corpus's detection share and
identity score. `petit -v --fingerprint` logs them.

Corpora are read from every one of these directories: the packaged
`petit/data/fingerprints/`, then `/var/lib/petit/fingerprints/`,
`/usr/local/petit/var/lib/fingerprints/` and `/opt/petit/var/lib/fingerprints/`.
Where two files share a name, the earlier directory wins. Corpora are parsed
once per process and cached by path and modification time.

To add your own:

1. Capture the event as a log in a format petit already parses. For a
   reboot on a systemd host, the shutdown is the tail of
   `journalctl -o short -b -1` and the startup is the head of
   `journalctl -o short -b 0`.
2. Trim it to the event itself, from the shutdown request through the end of
   startup, and concatenate the two.
3. Replace host names and user names you don't want to publish. The
   fingerprint normalizes numbers already.
4. Save it as `<name>.fp` in your fingerprint directory.

On a host without a journal, such as Alpine with busybox syslogd, take
`/var/log/messages` from the reboot request through the end of the next
boot instead.

### Keeping the corpora current

The packaged corpora for current releases are not captured by hand.
`tools/fingerprints/refresh.py` boots each distribution's own cloud image
under QEMU/KVM, reboots it once cleanly, and cuts that reboot out of the
journal. Every corpus comes from the same procedure on a clean guest.

- `platforms.toml` lists the families to track: how to find a release's
  image, which corpus it feeds, and whether it is a corpus or only verifies
  one. Rocky and CentOS Stream only verify the `elN` corpora captured on
  AlmaLinux, which also match RHEL itself. endoflife.date decides which
  releases are supported.
- `captured.json` is the lock file. It records the image, digest, kernel and
  date behind each committed capture.
- `.github/workflows/fingerprints.yml` runs weekly and on demand. It
  captures every supported release and opens a PR only when something
  changed:
  - a new release, which gets a corpus plus a second, independent reboot
    in `test/data/verify/<corpus>.fp/`;
  - a release whose fresh reboot no longer names its own corpus first, or
    scores below an identity of 0.5, which gets a new corpus;
  - a release past its end of life, which is retired.

  Every run also pushes each capture to
  [crunchtools/petit-captures](https://github.com/crunchtools/petit-captures),
  under `<date>/<run>/<release>/`. That includes the whole journal of both boots
  (`raw/<a|b>/*.log.xz`), scrubbed like the corpora. It lives in its own
  repo, so it is never part of a petit clone or package.

To capture by hand from a local qcow2 guest image:

    tools/fingerprints/refresh.py capture myhost --image guest.qcow2 \
        --seed --as verify:el9 --out captures/myhost

The image must run cloud-init with the NoCloud datasource, which `--seed`
feeds the capture script through. It also needs `logger`, `tar` and
either a systemd journal or, with `--log messages`, a syslog daemon writing
`/var/log/messages`. Stock distribution cloud images have all of these.

Every capture is scrubbed before it is written. Addresses become RFC 5737 or
RFC 3849 ones, MACs RFC 7042 ones, and machine and filesystem IDs zeros.
`refresh.py` refuses to write a capture that still names the host it ran on.
The captured guest calls itself `host01`.
