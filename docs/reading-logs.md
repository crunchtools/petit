# Reading logs

petit works out what it has been given (syslog, journalctl, Apache, Snort,
application logs with stack traces, JSON, a mail thread) without being told,
and cuts it into records before counting anything.

## Why it matters

A hash is only as good as the records it's built from. If a Java stack
trace is read as forty separate lines, it counts as forty patterns. If a
JSON array is read line by line, it's a pile of braces. Getting the record
boundaries and the fields right is what makes the counts mean something.

## How it works

Every input goes through the same stages:

```
text -> lines -> framer -> records -> entry driver -> hash driver
                                                   -> graphs
```

1. The text is split into lines.

2. A **framer** cuts the lines into records. A record is one log message:
   usually one line, but not always. petit tries each framer in turn and
   the first that recognises the whole input wins:

   | Framer      | Record |
   |-------------|--------|
   | `json`      | a JSON array of objects, or JSON Lines: one record per object |
   | `message`   | a mail thread or mbox: one record per message |
   | `multiline` | log messages that run over several lines: one record per message, continuation lines included |
   | `line`      | anything else: one record per line |

   `--framer json|message|multiline|line` forces one.

3. An **entry driver** reads each record and picks out the time, host,
   daemon and message. petit votes on which driver fits (syslog, rsyslog,
   Apache access and error, secure, Snort, ...). If one record in the input
   can't be read by the chosen driver, the whole input falls back to
   RawEntry, which reads anything but finds no times, hosts or daemons in it.

4. A **hash driver** turns each entry into a pattern, and entries with the
   same pattern are one group in `--hash`. The graphs count entries per
   slice of time instead.

Counts are kept for both: an Analysis reports `lines_in` (source lines) and
`records_in` (records), which are the same unless a framer joined lines.

### Big inputs

petit streams: it never holds the whole input, only each group's count and a
few sample lines, so a 96 MB log runs in about 30 MB of memory, and so does
one four times its size. A file is read more than once (once to choose the
framer, once to sample records for the drivers' vote, once to parse) so
every choice is made on the whole file. A pipe can only be read once. petit
holds its first 4 MB; a pipe that ends there is read exactly like a file,
and one that runs longer is framed and parsed by whatever its first 4 MB
chose, with any later record that driver can't read falling back to
RawEntry on its own.

### Multi-line messages

Stack traces, Python tracebacks and journalctl's indented continuation lines
put one message over several lines, and only the first carries a timestamp:

```
Sep 19 15:41:27 host01 ModemManager[1151]: <msg> couldn't check support...
Sep 19 15:41:27 host01 gnome-shell[2856]: Object .GProxyVolume ... disposed
                                          == Stack trace for context 0x5566 ==
                                          #0   556694310aa8 i   resource:///...
                                          #1   5566943109f8 i   resource:///...
Sep 19 15:41:28 host01 gnome-shell[2856]: Object .GProxyVolume ... disposed
                                          == Stack trace for context 0x5566 ==
```

Read line by line, that is seven records, four of which have no time, so the
syslog driver can't read them and the whole log falls back to RawEntry. The
multiline framer makes it three: a record starts at every line that begins
with a timestamp, and every other line belongs to the record above it. Each
crash is then one entry at 15:41:27, grouped with the other crashes like it,
and counted once in a graph.

It recognises the timestamps of syslog and journalctl, RFC 3339/5424, Python
logging, log4j/logback, Go, nginx, Apache, Snort, Kubernetes, the kernel,
Tomcat, java.util.logging, Redis and Unix time. It only switches on when some
continuation line is indented, which is what a real multi-line log looks
like; a log without one is framed line by line, exactly as before.
journalctl's `-- Boot ... --` lines are skipped.

### JSON identifiers

JSON records that differ only in an identifier (a `PROJ-1234` key, a numeric
id string, a SHA) are each their own group, because an identifier is kept
verbatim; UUIDs group as `<UUID>`. With `--identifiers N` (or
`max_identifiers=N` in the [library](library.md)) they group together, with
up to N of the identifiers listed under each group. 200 Jira issues that
differ only in their keys go from 200 groups to one.

## Example

The multi-line journal above, hashed:

```
$ petit --hash journal.log | head -3
3:	Started session-4.scope - Session 4 of User alice.
2:	<info> [1789845681.1001] device (wlan0): state change: config -> ip-config
2:	Object .GProxyVolume (0x55669dd5ac50), has been already disposed — impossible to access it. == Stack trace for context 0x55669424a1f0 == ...
```

Each gnome-shell crash is one record with its stack trace attached.

## Related

- [Writing and tuning drivers](internal/drivers.md): every framer rule and
  timestamp format, and how to add a driver (for contributors)
- [Hashing](hashing.md)
- [Library](library.md)
