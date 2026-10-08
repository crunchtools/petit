# petit Constitution

> **Version:** 1.4.0
> **Ratified:** 2026-09-20
> **Amended:** 2026-10-02
> **Status:** Active
> **Inherits:** [crunchtools/constitution](https://github.com/crunchtools/constitution) v1.21.0
> **Profile:** CLI Tool

This file holds petit's own rules. Everything the fleet requires (license,
semantic versioning, the Gourmand and Gatehouse gates, Dependabot) comes from
the inherited constitution and the CLI Tool profile at the pinned version, and
is checked against this repo's files by `constitution.yml`. It is not restated
here.

## Purpose

Log analysis for systems administrators: detects the log format, then
collapses the repetitive into counts so the unusual is what you read.

## Versioning

Semantic Versioning 2.0.0. MAJOR for changes to the CLI flag set, exit code
contract, or library API (`petit.api` and the names exported from
`petit`); MINOR for new
flags, new library functions, or new supported log formats; PATCH for bug
fixes and internal refactors with no observable behavior change.

## Amendments

This file holds the rules in force. Gatehouse reviews every PR against the
base branch's copy, so a PR cannot write the rules it is judged by.

A PR that changes this file is an amendment, and lands on its own: it
changes this file and nothing else. Code that relies on an amendment follows
in a later PR, reviewed against the amended text. Review an amendment for:

1. a version bump (MAJOR removes or loosens a rule, MINOR adds or tightens
   one, PATCH rewords without changing what is required). `Amended` is
   the day it merges, so an amendment made on the same day as the last
   one leaves that line as it is;
2. a rationale in the PR description;
3. new text that is clear and agrees with itself and with the code on the
   base branch.

An amendment that changes or removes a rule is not a violation of that rule.
Changing the rules is what an amendment is for, and maintainer approval of
the PR is the check on it.

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
`--framer {auto,json,message,multiline,line}`, `--identifiers N`, `--span`,
`-V/--version`, and one mode flag per report: `--hash`, `--wordcount`,
`--daemon`, `--host`, `--sgraph`, `--mgraph`, `--hgraph`, `--dgraph`,
`--mograph`, `--ygraph`, `--graph`. One optional positional `file`; reads
stdin when omitted. Running `petit` with no flags at all prints the version.

Exit codes: `0` on success, `1` on a `PetitError` (bad input — unreadable
file, unparseable log, unknown driver name), `2` on a usage error (argparse
itself: unknown flag, more than one positional file).

## External APIs / Credentials

None. petit reads a local file or stdin and writes to stdout/stderr; it
makes no network calls and needs no credentials, so the
`~/.config/mcp-env/petit.env` convention does not apply.

## Library API

`petit.api` and the names exported from `petit` (`analyze_text`,
`analyze_lines`, `hash_text`, `hash_lines`, `detect_format`,
`pull_identifiers`, `IDENTIFIER`, `Analysis`, `Group`, `FingerprintScore`,
and the `PetitError` hierarchy) are a supported embedding surface
independent of the CLI. See `petit/api.py`'s module docstring.

The CLI is a thin shell over `petit.api`. Every capability the CLI has is
reachable from the library with the same defaults, and the byte-for-byte
fixture suite is therefore a regression net for the library too. A new
driver, framer, or option is added to the library first and exposed by the
CLI second; never the reverse.

## Container

Built on `quay.io/hummingbird/python:latest-fips`/`-fips-builder`,
multi-stage venv pattern. No extra system packages — pure stdlib. Published
to `quay.io/crunchtools/petit` and `ghcr.io/crunchtools/petit`.

## Test Suite

`test/test_api.py` covers the library surface with mocked-nothing-needed
unit tests (no external API, nothing to mock). `test/test_cli.py` covers the
CLI: the exit code contract, `--help`, and a byte-for-byte regression suite
against `test/data/` + `test/output/` fixtures that have been part of this
repo since 2009. `test/test_drivers.py` holds MERGE/NO_MERGE example pairs
for every hash driver; a change to how aggressively a driver groups lands as
a change to that table. Run via `uv run pytest -v`.

## Hostile Input Invariants

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
   refuse by declining (a framer's `claims()` returns False,
   `pull_identifiers` returns its input unchanged), never by raising;
3. every regex that reads input, whether in a filter file, generalization
   table, framer or driver, is linear-time: character classes and bounded
   repetition, no nested quantifiers, each probed with input shaped to make it backtrack;
4. normalization touches tokens, never prose. A token (a timestamp,
   number, address, hash or identifier) is bounded and holds no spaces,
   so it cannot carry a sentence, and it may leave the fingerprint.
   Short strings and anything else a human wrote stay in it, so two
   records that say different things cannot merge and hide one of them.
   A merge keeps samples and a count, and drops the other token values.
   Identifiers can be listed instead when the caller asks
   (`max_identifiers`), and a record whose identifiers cannot all be
   listed keeps them in its fingerprint.
