# Hashing

`petit --hash` groups the lines of a log by what's left after the parts that
vary have been taken out, then prints each group once with its count, most
frequent first. A 1500-line sshd log becomes eight lines.

## Why it matters

Most of any log is routine: logins, cron runs, health checks, repeated a
thousand times with a different PID or timestamp each time. The lines worth
reading are the ones that show up once. Hashing does the counting so that a
person only has to read the patterns, and the rare ones stand out at the
bottom of the list. See [Philosophy](philosophy.md) for where the idea
comes from.

## How it works

Each record is parsed by the entry driver for its format (syslog, Apache,
Snort, JSON, and so on; see [Reading logs](reading-logs.md)). The hash
driver for that format then applies its stopword filter: numbers, IPs,
timestamps and other variable tokens become `#` or a named placeholder
(`<N>`, `<TS>`, `<IP>`). Records with the same result are one group.

Options:

| Option | Effect |
|--------|--------|
| `--hash` | Group and count. Groups seen three times or fewer print a real sample line instead of the pattern, since a pattern with a count of one hides nothing. |
| `--nosample` | Always print the pattern. |
| `--allsample` | Always print a real sample line. |
| `--nofilter` | Skip the stopword filter: only identical lines group. Useful for de-duplicating lists such as source IPs. |
| `--fingerprint` | Collapse known routine event sequences (reboots of RHEL, Fedora, Debian, Ubuntu, openSUSE, Alpine, Arch) into one group each, named after the corpus that matched. Off by default because it removes lines. |
| `--identifiers N` | For JSON records, group records that differ only in an identifier (`PROJ-1234`, a numeric ID string, a UUID or SHA) and list up to N of the identifiers under each group. |

The stopword files live in `src/petit/data/filters/` and the reboot corpora
in `src/petit/data/fingerprints/`. How they are chosen and how to add one is
in [Writing and tuning drivers](internal/drivers.md).

## Example

An sshd log from 2010, 1500 lines:

```
$ petit --hash secure
537:	sshd[#]: Accepted publickey for #
347:	sshd[#]: Postponed publickey for #
273:	sshd[#]: pam_unix(sshd:session): session opened for #
270:	sshd[#]: pam_unix(sshd:session): session closed for #
33:	sshd[#]: reverse mapping checking getaddrinfo for #
32:	sshd[#]: Connection closed by #
6:	sshd[#]: Accepted password for #
2:	subsystem request for sftp
```

The six password logins on a system that otherwise uses keys are the thing
to go look at.

An Apache access log hashes by request:

```
$ petit --hash access_log
21:	/cgi-bin/ads/display_test.pl?ad=mytopnew&ts=#
20:	/cgi-bin/ads/display_test.pl?ad=myfoot
11:	/cgi-bin/ads/display_test.pl?ad=mytopnew
8:	/cgi-bin/ads/display_test.pl?ad=wwwcctside
5:	/ads/#/Left_Nav.gif
```

A syslog that caught a RHEL 4 and a Fedora 11 reboot hashes to 745 groups.
With `--fingerprint`, each reboot is one line and it's 16:

```
$ petit --hash --fingerprint messages | tail -2
1:	fedora11-reboot.fp
1:	rhel4-reboot.fp
```

## Related

- [Reports](reports.md): the same counting by daemon, host or word
- [Reading logs](reading-logs.md): how records and drivers are chosen
- [Library](library.md): `hash_text()` and `analyze_text()` do this from Python
