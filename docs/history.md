# History

petit is older than most of the tools it now reads logs from. It started as
a Perl script in the 2000s, shipped in Fedora, EPEL, Debian and Ubuntu for a
decade, fell out of them with Python 2, and came back in 2026 as a Python 3
command and library. This page is the full record; the README has the short
version.

## Why it matters

Some of the best writing about how to use petit is fifteen years old, and
some of it lives on sites that no longer exist. Knowing where the code has
been makes old links, package names and bug reports make sense.

## How it got here

**Origins.** petit grew out of `lt`, a Perl script Scott McCarty wrote to
hash log files, which was itself inspired by Marcus Ranum's
[artificial ignorance](https://www.ranum.com/security/computer_security/papers/ai/):
throw away what you know is boring, and read what's left.

| Date | Event | Source |
|------|-------|--------|
| 2009-07-31 | First commit in this repository; the tool is still called `lt`. | `002657d` |
| 2009-08-05 | "lt2": a new object model, built from the ground up. | `8dacd32` |
| 2009-08-07 | Renamed petit. First RPM spec the same day, first .deb the next. | `bc9993f`, `afdb037`, `81411fa` |
| 2009-08-17 | Shared code split into its own `crunchtools` library. | `1daa3be` |
| 2009 | Hosted in Subversion at eyemg, with releases on opensource.eyemg.com. | `e91271f` |
| 2009-09 | First public talk: "Science in Systems Administration" at the Akron Linux Users Group. | [crunchtools.com](https://crunchtools.com/science-in-systems-administration/) |
| 2009-11-16 | Relicensed GPLv3. | `21cf230` |
| 2010-03-07 | Fedora package review filed by Sandro Mathys, approved May 2010. | [RHBZ #571225](https://bugzilla.redhat.com/show_bug.cgi?id=571225) |
| 2010-04 | Imported to Fedora; in EPEL 5 by the end of the month. | [src.fedoraproject.org](https://src.fedoraproject.org/rpms/petit) |
| 2010-05-03 | opensource.eyemg.com becomes crunchtools.com; petit gets its project page. | [crunchtools.com/software/petit](https://crunchtools.com/software/petit/) |
| 2010-06-11 | "Petit is Available in Fedora 13". | [crunchtools.com](https://crunchtools.com/petit-is-available-in-fedora-13/) |
| 2010-07-06 | Accepted into Debian by Carl Chenet for the Python Applications Packaging Team; in Squeeze testing by 2010-07-17. | [tracker.debian.org](https://tracker.debian.org/pkg/petit) |
| 2010-07-31 | "Log Analysis with Python" tutorial at PyOhio 2010. | [recording](https://archive.org/details/pyvideo_514___pyohio-2010-log-analysis-with-python), [slides post](https://crunchtools.com/log-analysis-with-python/) |
| 2010-11 | Moved from Subversion to Mercurial on Google Code, as `petit-log` (not `petit`, which is someone else's project). | `760f38f` |
| 2010-11-02 | In Ubuntu from 11.04 Natty, and in every release through 19.10 Eoan, including the 12.04, 14.04, 16.04 and 18.04 LTS releases. | [launchpad.net](https://launchpad.net/ubuntu/+source/petit) |
| 2011-04-15 | 1.1.1, the last Python 2 release. Into EPEL 6 that July. | tag `1.1.1` |
| 2015-07-02 | Google Code shuts down; the exporter moves petit to github.com/fatherlinux/petit. | `8e9978a` |
| 2018-12-24 | Retired from Fedora after 18 releases (f12 through f29), orphaned. | [src.fedoraproject.org](https://src.fedoraproject.org/rpms/petit) |
| 2019–2020 | Removed from Debian and Ubuntu in the Python 2 purge. | [Debian #937274](https://bugs.debian.org/937274) |
| 2022-10-13 | Ported to Python 3 as 2.0.0. | `c18d9a7` |
| 2022-10-17 | Pablo Iranzo Gómez publishes it to PyPI as `petitlog`. | [pypi.org](https://pypi.org/project/petitlog/) |
| 2026-09-19 | Moves to github.com/crunchtools/petit. | `e74f8e2` |
| 2026-09-20 | Relicensed AGPL-3.0-or-later; on PyPI as `petit-log-crunchtools`. | [pypi.org](https://pypi.org/project/petit-log-crunchtools/) |
| 2026-09-24 | Native .rpm and .deb packages again, from a signed repository. | [Install](install.md) |

## Example

How petit was used in 2010, from Scott's "Centralized Logging" post: a
syslog-ng server collected every machine's logs, and a nightly script ran
`petit --hgraph --wide`, `--hash --fingerprint`, `--daemon` and `--host`
over them, then sorted the hashed lines into Errors, Kernel, Cluster and
Everything Else. Reading the report took three to five minutes each morning,
and the approach held at 1500 Linux servers, because the number of unique
patterns doesn't grow linearly with the number of servers.

## Further reading

Written with or about petit, oldest first:

- [Science in Systems Administration](https://crunchtools.com/science-in-systems-administration/),
  Scott McCarty, ALUG, September 2009
- [Centralized Logging System, Analysis, and Troubleshooting](https://crunchtools.com/centralizing-log-files/),
  Scott McCarty, 2010: the daily report, scripts included
- [Snort Alert Log: Simple Analysis and Daily Reporting with Arnold and Petit](https://crunchtools.com/log-analysis-simple-breakdown-of-snort-alert-log-with-arnold/),
  Scott McCarty, 2010
- [Log Analysis with Python](https://archive.org/details/pyvideo_514___pyohio-2010-log-analysis-with-python),
  PyOhio 2010 talk recording
- [System's Administrator's Lab: Testing](https://crunchtools.com/systems-administrators-lab-testing/),
  Scott McCarty, 2010: the functional test suite that caught three bugs
  in the Mercurial move
- [Designing a Robust Monitoring System](https://crunchtools.com/designing-a-robust-monitoring-system/),
  Scott McCarty, 2011
- [Petit for Log Analysis](https://blog.jasonantman.com/2012/02/petit-for-log-analysis/),
  Jason Antman, 2012
- [Petiti – An Open Source Log Analysis Tool for Linux SysAdmins](https://www.tecmint.com/petiti-log-analysis-tool-for-linux-sysadmins/),
  Aaron Kili, Tecmint, 2017 (title as published)

## Related

- [Philosophy](philosophy.md): the 2009 reasoning, in the original words
- [CHANGELOG.md](../CHANGELOG.md): every release since the Python 3 port
