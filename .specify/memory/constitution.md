# petit Constitution

> **Version:** 1.2.0
> **Ratified:** 2026-09-20
> **Amended:** 2026-09-26
> **Status:** Active
> **Inherits:** [crunchtools/constitution](https://github.com/crunchtools/constitution) v1.17.0
> **Profile:** CLI Tool

## Purpose

Log analysis for systems administrators: detects the log format, then
collapses the repetitive into counts so the unusual is what you read.

## License

AGPL-3.0-or-later.

## Versioning

Semantic Versioning 2.0.0. MAJOR for changes to the CLI flag set, exit code
contract, or library API (`petit.api`); MINOR for new flags, new library
functions, or new supported log formats; PATCH for bug fixes and internal
refactors with no observable behavior change.

## PyPI Naming Exception

The tool and command are `petit`; the PyPI distribution is
`petit-log-crunchtools`, not `petit`, because `petit` was already taken on
PyPI by an unrelated protein engineering toolkit at the time petit was
first packaged for PyPI (see `CHANGELOG.md` 3.0.0 and 2.0.0 entries —
`petitlog` was also taken by a fork of this same project). The
distribution briefly used `petit-log` before settling on
`petit-log-crunchtools` (3.1.1), matching the naming convention already in
use across the crunchtools fleet (`gatehouse-crunchtools`,
`mcp-gemini-crunchtools`). This is a documented exception to profile
Section VIII's PyPI-name-matches-tool-name convention, not an oversight.

## CLI Interface

Built with `argparse`. Flags: `-v/--verbose`, `--sample`/`--nosample`/
`--allsample`, `--filter`/`--nofilter`, `--wide`, `--tick`, `--fingerprint`,
`--framer {auto,line,json,message}`,
`-V/--version`, and one mode flag per report: `--hash`, `--wordcount`,
`--daemon`, `--host`, `--sgraph`, `--mgraph`, `--hgraph`, `--dgraph`,
`--mograph`, `--ygraph`. One optional positional `file`; reads stdin when
omitted. Running `petit` with no flags at all prints the version.

Exit codes: `0` on success, `1` on a `PetitError` (bad input — unreadable
file, unparseable log, unknown driver name), `2` on a usage error (argparse
itself: unknown flag, more than one positional file).

## External APIs / Credentials

None. petit reads a local file or stdin and writes to stdout/stderr; it
makes no network calls and needs no credentials, so the
`~/.config/mcp-env/petit.env` convention does not apply.

## Library API

`petit.api` (`hash_text`, `analyze_text`, `detect_format`, `Group`,
`Analysis`, and the `PetitError` hierarchy) is a supported embedding surface
independent of the CLI — see `petit/api.py`'s module docstring.

The CLI is a thin shell over `petit.api`. Every capability the CLI has is
reachable from the library with the same defaults, and the byte-for-byte
fixture suite is therefore a regression net for the library too. A new
driver, framer, or option is added to the library first and exposed by the
CLI second; never the reverse.

## Container

Built on `quay.io/hummingbird/python:latest-fips`/`-fips-builder`,
multi-stage venv pattern. No extra system packages — pure stdlib. Published
to `quay.io/crunchtools/petit` and `ghcr.io/crunchtools/petit`.

## Testing

`test/test_api.py` covers the library surface with mocked-nothing-needed
unit tests (no external API, nothing to mock). `test/test_cli.py` covers the
CLI: the exit code contract, `--help`, and a byte-for-byte regression suite
against `test/data/` + `test/output/` fixtures that have been part of this
repo since 2009. `test/test_drivers.py` holds MERGE/NO_MERGE example pairs
for every hash driver; a change to how aggressively a driver groups lands as
a change to that table. Run via `uv run pytest -v`.

### Hostile input

petit parses attacker-controlled text: its main library consumer sits on a
prompt-injection perimeter. Every parser, framer, and driver MUST have
adversarial tests in `test/test_hostile.py` alongside its functional ones,
and a change that adds one without them is incomplete. Those tests MUST
show that:

1. hostile input produces a result or a `PetitError` — never
   `RecursionError`, `SystemExit`, or any other exception escaping the
   library;
2. work is bounded: deep nesting, oversized records, and pathological
   strings complete within a fixed time budget, and size and depth limits
   refuse by declining (a framer's `claims()` returns False), never by
   raising;
3. every regex added to a filter file, generalization table, or framer is
   linear-time: character classes and bounded repetition, no nested
   quantifiers, each probed with input shaped to make it backtrack;
4. normalization never removes what a human wrote: short strings and
   client-supplied values stay in the fingerprint, so two records that
   say different things cannot merge and hide one of them. The one
   exception is an identifier (a bounded, space-free token that
   `pull_identifiers` recognises), and only when the caller asks for it:
   it may leave the fingerprint when its value is listed for every
   record in the group. A record whose identifiers cannot all be listed
   keeps them in its fingerprint.

## Gourmand

Zero violations required. Config in `gourmand.toml`, exceptions in
`gourmand-exceptions.toml`.

## Quality Gates

1. Lint — `uv run ruff check src test`
2. Type Check — `uv run mypy src`
3. Tests — `uv run pytest -v`
4. Gourmand — `gourmand check --full .`, run from `quay.io/crunchtools/gourmand:latest` (see `.pre-commit-config.yaml`)
5. Container Build — `podman build -f Containerfile .`
