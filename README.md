<p align="center">
  <img src="https://raw.githubusercontent.com/crunchtools/petit/master/docs/images/petit-logo.png" alt="petit: a brass log press turning a long column of log text into a short slip" width="320">
</p>

# petit

petit is a command-line log analyzer for systems administrators. It takes
out of a log everything that repeats (the routine logins, the cron runs,
the health checks) and counts it, so what's left to read is short and the
unusual lines stand out. It works out the format on its own (syslog,
journalctl, Apache, Snort, application logs with stack traces, JSON, mail),
draws activity graphs in the terminal, and does the same from Python. It
has been doing this since 2009.

<p align="center">
  <img src="https://raw.githubusercontent.com/crunchtools/petit/master/docs/demo/petit.gif" alt="Terminal demo: a 1500-line sshd log hashed to 8 lines, then graphed, then reported by daemon and by word" width="800">
</p>

## Capabilities

1. **Hashing.** `petit --hash` groups lines by what's left after numbers,
   IPs and timestamps are taken out, and prints each pattern once with its
   count. A 1500-line sshd log becomes eight lines. `--fingerprint` goes
   further and collapses whole reboots into one line. [Hashing](https://github.com/crunchtools/petit/blob/master/docs/hashing.md)

2. **Reports.** `--daemon`, `--host` and `--wordcount` count a log by
   program, by machine, or by word, which shows its shape before you read a
   single line. [Reports](https://github.com/crunchtools/petit/blob/master/docs/reports.md)

3. **Graphs.** `--graph` draws the whole log over time in the terminal,
   choosing a column size that fits; `--hgraph`, `--mgraph`, `--span 90m`
   and friends pick a fixed window. [Graphs](https://github.com/crunchtools/petit/blob/master/docs/graphs.md)

4. **Format detection.** petit frames the input into records (JSON objects,
   mail messages, multi-line messages with their stack traces, or lines)
   and votes on a driver to read them. It streams: memory follows the number
   of distinct patterns, not the size of the log. [Reading logs](https://github.com/crunchtools/petit/blob/master/docs/reading-logs.md)

5. **Python library.** `hash_lines()`, `analyze_text()` and friends return
   the same groups as data, with no files, stdout or exits involved.
   [Library](https://github.com/crunchtools/petit/blob/master/docs/library.md)

## Quick Start

```bash
# Fedora, RHEL and rebuilds (Debian, Ubuntu and SUSE are in docs/install.md)
sudo curl -fsSLo /etc/yum.repos.d/crunchtools.repo \
    https://crunchtools.github.io/packages/rpm/crunchtools.repo
sudo dnf install petit

# Anywhere with Python 3.11+
uv tool install petit-log-crunchtools

# Or in a container
podman run --rm -v $(pwd):/data:ro,Z quay.io/crunchtools/petit --hash /data/some.log
```

Then:

```bash
petit --hash --fingerprint /var/log/messages    # what happened, minus reboots
petit --daemon /var/log/messages                 # who's talking
petit --graph /var/log/httpd/error_log           # when
grep error /var/log/messages | petit --mgraph    # when, for just the errors
```

## History

petit started as `lt`, a Perl script inspired by Marcus Ranum's
[artificial ignorance](https://www.ranum.com/security/computer_security/papers/ai/),
and became petit in August 2009. Since then:

- **2009**: first shown at the Akron Linux Users Group; hosted in Subversion at eyemg
- **2010**: packaged in Fedora and EPEL, then Debian; moved to crunchtools.com and
  presented at PyOhio
- **2010–2015**: hosted on Google Code as `petit-log`, in Mercurial
- **2011–2019**: shipped in every Ubuntu release from 11.04 to 19.10
- **2015**: moved to GitHub by the Google Code exporter
- **2018–2020**: dropped from Fedora, Debian and Ubuntu along with Python 2
- **2022**: ported to Python 3
- **2026**: moved to the crunchtools org, relicensed AGPL, back in native packages

The full timeline, with sources, is in [History](https://github.com/crunchtools/petit/blob/master/docs/history.md).

**Further reading:**
[Introduction: Petit Log Analysis Tool for Systems Administrators](https://www.youtube.com/watch?v=5hI5sUPuzGc) (video, 2009),
[Centralized Logging System, Analysis, and Troubleshooting](https://crunchtools.com/centralizing-log-files/) (2010),
[Snort Alert Log: Simple Analysis and Daily Reporting with Arnold and Petit](https://crunchtools.com/log-analysis-simple-breakdown-of-snort-alert-log-with-arnold/) (2010),
[Log Analysis with Python, PyOhio 2010](https://archive.org/details/pyvideo_514___pyohio-2010-log-analysis-with-python),
[Petit for Log Analysis](https://blog.jasonantman.com/2012/02/petit-for-log-analysis/) by Jason Antman (2012),
[Petiti – An Open Source Log Analysis Tool for Linux SysAdmins](https://www.tecmint.com/petiti-log-analysis-tool-for-linux-sysadmins/) by Aaron Kili at Tecmint (2017).

## Documentation

| Page | What it covers |
|------|----------------|
| [Install](https://github.com/crunchtools/petit/blob/master/docs/install.md) | Native packages for Fedora, RHEL, SUSE, Debian and Ubuntu; PyPI; container |
| [Hashing](https://github.com/crunchtools/petit/blob/master/docs/hashing.md) | `--hash`, samples, filters, `--fingerprint`, `--identifiers` |
| [Reports](https://github.com/crunchtools/petit/blob/master/docs/reports.md) | `--daemon`, `--host`, `--wordcount` |
| [Graphs](https://github.com/crunchtools/petit/blob/master/docs/graphs.md) | Every graph, its units, window and width |
| [Reading logs](https://github.com/crunchtools/petit/blob/master/docs/reading-logs.md) | Framers, drivers, big inputs, multi-line messages, JSON |
| [Library](https://github.com/crunchtools/petit/blob/master/docs/library.md) | The Python API and what SemVer covers |
| [Philosophy](https://github.com/crunchtools/petit/blob/master/docs/philosophy.md) | Why petit removes certainty and leaves uncertainty |
| [History](https://github.com/crunchtools/petit/blob/master/docs/history.md) | Where petit has lived since 2009, and what's been written about it |
| [Writing and tuning drivers](https://github.com/crunchtools/petit/blob/master/docs/internal/drivers.md) | For contributors: framers, entry and hash drivers, stopwords, reboot corpora |

## Development

```bash
uv sync --all-extras          # dev tools: pytest, ruff, mypy
uv run pytest                 # tests
uv run ruff check src test    # lint
uv run mypy src               # types
podman build -t petit .       # container
```

Packages, the container image and PyPI releases are built by GitHub Actions
on every GitHub release. The README demo is rendered from
[docs/demo/petit.tape](https://github.com/crunchtools/petit/blob/master/docs/demo/petit.tape).

## License

AGPL-3.0-or-later. See [COPYING](https://github.com/crunchtools/petit/blob/master/COPYING).
