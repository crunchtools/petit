#!/usr/bin/env python3
"""Log & text analysis tool for systems administrators


Logtool provides trimming and analysis of ascii based log files
such as syslog.  Different options allow different types of analyis such as
line hashing, hash counting, and word usage counting. These options can be used
to determine WHAT is normal and WHAT to look for, which programs such
as logwatch or swatch cannot do.
"""
###############################################################################
#
# Writen By: Scott McCarty
# Date: 8/2009
# Email: scott.mccarty@gmail.com
#
# Copyright (C) 2009 Scott McCarty
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import signal
import sys
from collections.abc import Callable
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from types import FrameType

from petit.api import Analysis, HashMode, analyze_lines
from petit.CrunchLog import LogStream
from petit.errors import PetitError
from petit.LogGraph import (
    GRAPH_FOR_UNIT,
    MIN_SPAN,
    DaysGraph,
    GraphHash,
    HoursGraph,
    MinutesGraph,
    MonthsGraph,
    SecondsGraph,
    YearsGraph,
    fit_graph,
)
from petit.records import FRAMER_NAMES
from petit.sources import open_source

GRAPH_MODES = frozenset({
    "mode_graph", "mode_sgraph", "mode_mgraph", "mode_hgraph",
    "mode_dgraph", "mode_mograph", "mode_ygraph",
})

# --span suffixes. "mo" is listed before "m" so the regex tries it first.
SPAN_UNITS = {"mo": "month", "s": "second", "m": "minute", "h": "hour", "d": "day", "y": "year"}
# GraphHash.display() prints the axis labels two characters wider than the graph.
AXIS_OVERHANG = 2
SPAN_RE = re.compile(r"^(\d+)(" + "|".join(SPAN_UNITS) + r")$")


def parse_span(value: str) -> tuple[str, int]:
    """argparse type for --span: `90m` -> ("minute", 90)."""
    match = SPAN_RE.match(value)
    if match is None:
        raise argparse.ArgumentTypeError(
            f"invalid span {value!r}: expected a count and one of "
            + ", ".join(SPAN_UNITS) + " (e.g. 90m, 36h, 18mo)"
        )
    return SPAN_UNITS[match.group(2)], int(match.group(1))

# Process Signals


def sigint_handler(_signum: int, _frame: FrameType | None) -> None:
    sys.exit(0)


## Exit when control-C is pressed
signal.signal(signal.SIGINT, sigint_handler)

## Ignore problems when piping to head
signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def build_parser() -> argparse.ArgumentParser:
    """Adds all options in one concise function"""

    parser = argparse.ArgumentParser(usage="%(prog)s [options] [file]")

    # Handle flags
    parser.add_argument("-v", "--verbose",
                         dest="verbose",
                         action="count",
                         help="Show verbose output")

    parser.add_argument("--sample", dest="sample",
                         action="store_const",
                         const="threshold",
                         default="threshold",
                         help="Show sample output for small numbered entries")

    parser.add_argument("--nosample",
                         dest="sample",
                         action="store_const",
                         const="none",
                         help="Do not sample output for low count entries")

    parser.add_argument("--allsample", dest="sample",
                         action="store_const",
                         const="all",
                         help="Show samples instead of munged text for all entries")

    parser.add_argument("--filter",
                         dest="filter",
                         action="store_true",
                         default=None, help="Use filter files during processing")

    parser.add_argument("--nofilter",
                         dest="filter",
                         action="store_false",
                         help="Do not use filter files during processing")

    parser.add_argument("--wide",
                         dest="wide",
                         action="store_true",
                         default=False,
                         help="Use wider graph characters")

    parser.add_argument("--tick",
                         dest="tick",
                         default="#",
                         help="Change tick character from default")

    parser.add_argument("--framer",
                         dest="framer",
                         choices=FRAMER_NAMES,
                         default="auto",
                         help="How to cut input into records: per JSON object, per email "
                              "message, per multi-line log message (a stack trace joined "
                              "to the line it belongs to), or one per line. auto, the "
                              "default, tries them in that order")

    parser.add_argument("--identifiers",
                         dest="identifiers",
                         type=int,
                         default=0,
                         metavar="N",
                         help="For JSON records, group those that differ only in an "
                              "identifier (PROJ-1234, a numeric id string, a UUID or SHA) "
                              "and list up to N of the identifiers under each group")

    parser.add_argument("--fingerprint",
                         dest="fingerprint",
                         action="store_true",
                         default=False,
                         help="Use fingerprinting to remove certain patterns")

    # Handle modes
    parser.add_argument("-V", "--version",
                         dest="mode",
                         action="store_const",
                         const="mode_version",
                         help="Show verbose output")

    parser.add_argument("--hash",
                         dest="mode",
                         action="store_const",
                         const="mode_hash",
                         help="Show hashes of log files with numbers removed")

    parser.add_argument("--wordcount",
                         dest="mode",
                         action="store_const",
                         const="mode_wordcount",
                         help="Show word count for given word")

    parser.add_argument("--daemon",
                         dest="mode",
                         action="store_const",
                         const="mode_daemon",
                         help="show a report of entries from each daemon")

    parser.add_argument("--host",
                         dest="mode",
                         action="store_const",
                         const="mode_host",
                         help="show a report of entries from each host")

    parser.add_argument("--sgraph",
                         dest="mode",
                         action="store_const",
                         const="mode_sgraph",
                         help="graph 60 one-second columns from the first entry")

    parser.add_argument("--mgraph",
                         dest="mode",
                         action="store_const",
                         const="mode_mgraph",
                         help="graph 60 one-minute columns from the first entry")

    parser.add_argument("--hgraph",
                         dest="mode",
                         action="store_const",
                         const="mode_hgraph",
                         help="graph 24 one-hour columns from the first entry")

    parser.add_argument("--dgraph",
                         dest="mode",
                         action="store_const",
                         const="mode_dgraph",
                         help="graph 31 one-day columns from the first entry")

    parser.add_argument("--mograph",
                         dest="mode",
                         action="store_const",
                         const="mode_mograph",
                         help="graph 12 one-month columns from the first entry")

    parser.add_argument("--ygraph",
                         dest="mode",
                         action="store_const",
                         const="mode_ygraph",
                         help="graph 10 one-year columns from the first entry")

    parser.add_argument("--graph",
                         dest="mode",
                         action="store_const",
                         const="mode_graph",
                         help="graph the whole log, choosing the finest column size (1s up to 10y) "
                              "that fits the terminal width")

    parser.add_argument("--span",
                         dest="span",
                         type=parse_span,
                         default=None,
                         metavar="N{s,m,h,d,mo,y}",
                         help="graph N one-unit columns from the first entry: s(econds), "
                              "m(inutes), h(ours), d(ays), mo(nths), y(ears), e.g. 90m or 36h. "
                              "Implies --graph; at least 6, and must fit the terminal width")

    # -V/--version is the default when no mode flag is given at all, exactly
    # as running plain `petit` always has.
    parser.set_defaults(mode="mode_version")

    parser.add_argument("file", nargs="?", default=None)

    return parser


def check_span(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """--span stands alone or goes with --graph, and has to fit on screen.

    Exits 2 through parser.error() like any other usage mistake.
    """
    if args.span is None:
        return
    if args.mode == "mode_version":
        # No mode flag given: --span on its own means --graph.
        args.mode = "mode_graph"
    elif args.mode != "mode_graph":
        parser.error("--span only applies to --graph")

    _unit, count = args.span
    if count < MIN_SPAN:
        parser.error(f"--span needs at least {MIN_SPAN} units to label the axis")
    if count > graph_columns(args):
        columns = count * (2 if args.wide else 1) + AXIS_OVERHANG
        available = shutil.get_terminal_size().columns
        parser.error(f"--span needs {columns} columns; the terminal has {available}")


def graph_columns(args: argparse.Namespace) -> int:
    """How many graph columns fit the terminal; --wide draws each one twice as wide.

    The axis labels run two characters past the last column, so they get
    that room too.
    """
    return (shutil.get_terminal_size().columns - AXIS_OVERHANG) // (2 if args.wide else 1)


def mode_version(_args: argparse.Namespace, _filename: str) -> None:
    """Version information"""
    try:
        current_version = pkg_version("petit-log-crunchtools")
    except PackageNotFoundError:
        current_version = "unknown"
    print("Version: " + current_version)


# Groups at or below this count print a real sample instead of the pattern.
SAMPLE_THRESHOLD = 3


def print_groups(analysis: Analysis, sample: str) -> None:
    """Print each group as `count:<TAB>text`, most frequent first.

    `sample` picks the text: "none" always prints the pattern, "all" always
    prints a member's payload, "threshold" prints the payload only for
    groups small enough that the pattern hides something worth seeing.
    """
    for group in analysis.groups:
        show_sample = sample == "all" or (
            sample == "threshold" and group.count <= SAMPLE_THRESHOLD
        )
        text = group.sample_payloads[0] if show_sample else group.pattern
        print(str(group.count) + ":\t" + text)
        if group.identifiers:
            listed = ", ".join(" ".join(row) for row in group.identifiers)
            # A field name is an object key from the input: escape it, as
            # the pattern already is, so it cannot reach the terminal raw.
            fields = " ".join(json.dumps(name)[1:-1] for name in group.identifier_fields)
            print("\t" + fields + ": " + listed)


def mode_hash(args: argparse.Namespace, filename: str) -> None:
    """Runs in hashing mode"""
    analysis = analyze_lines(
        open_source(filename),
        source_name=filename,
        filter_name="__none__" if args.filter is False else None,
        max_samples=1,
        collapse_fingerprints=args.fingerprint,
        framer=args.framer,
        max_identifiers=args.identifiers,
    )
    print_groups(analysis, args.sample)


def _run_report_mode(hash_mode: HashMode, args: argparse.Namespace, filename: str) -> None:
    """--wordcount, --daemon and --host: counts per word, daemon or host."""
    analysis = analyze_lines(
        open_source(filename), source_name=filename, max_samples=1, hash_mode=hash_mode,
        framer=args.framer,
    )
    print_groups(analysis, "none")


def mode_wordcount(args: argparse.Namespace, filename: str) -> None:
    """Runs wordcount mode"""
    _run_report_mode("wordcount", args, filename)


def mode_daemon(args: argparse.Namespace, filename: str) -> None:
    """Runs daemon report mode"""
    _run_report_mode("daemon", args, filename)


def mode_host(args: argparse.Namespace, filename: str) -> None:
    """Runs host report mode"""
    _run_report_mode("host", args, filename)


def _run_graph_mode(
    graph_cls: type[GraphHash] | None,
    args: argparse.Namespace,
    filename: str,
) -> None:
    """Build, configure and display one of the time-window graphs.

    Every --?graph mode differs only in which GraphHash subclass it builds;
    tick/wide/display are identical, so they share this one implementation.
    `graph_cls` None is --graph: --span's unit and count if given, otherwise
    whichever fixed graph fits the log.
    """
    def draw(log: LogStream) -> GraphHash:
        if args.span is not None:
            unit, count = args.span
            return GRAPH_FOR_UNIT[unit](log, count)
        if graph_cls is None:
            return fit_graph(log, graph_columns(args))
        return graph_cls(log)

    x = LogStream(open_source(filename), framer=args.framer).build(draw)
    x.tick = args.tick
    x.wide = args.wide
    x.display()


MODE_HANDLERS: dict[str, Callable[[argparse.Namespace, str], None]] = {
    "mode_version": mode_version,
    "mode_hash": mode_hash,
    "mode_wordcount": mode_wordcount,
    "mode_daemon": mode_daemon,
    "mode_host": mode_host,
    "mode_sgraph": lambda args, filename: _run_graph_mode(SecondsGraph, args, filename),
    "mode_mgraph": lambda args, filename: _run_graph_mode(MinutesGraph, args, filename),
    "mode_hgraph": lambda args, filename: _run_graph_mode(HoursGraph, args, filename),
    "mode_dgraph": lambda args, filename: _run_graph_mode(DaysGraph, args, filename),
    "mode_mograph": lambda args, filename: _run_graph_mode(MonthsGraph, args, filename),
    "mode_ygraph": lambda args, filename: _run_graph_mode(YearsGraph, args, filename),
    "mode_graph": lambda args, filename: _run_graph_mode(None, args, filename),
}


def main() -> int:
    """Console-script entry point.

    This is the boundary where a PetitError becomes an exit status. The
    library itself never exits — see petit.errors.
    """
    parser = build_parser()
    args = parser.parse_args()
    check_span(parser, args)

    filename = args.file if args.file is not None else "__none__"

    # Set Verbosity
    log_level = logging.WARNING
    if args.verbose == 1:
        log_level = logging.INFO
    elif args.verbose == 2:
        log_level = logging.DEBUG

    # Set up basic configuration
    logging.basicConfig(level=log_level)

    try:
        MODE_HANDLERS[args.mode](args, filename)
    except PetitError as exc:
        print("petit: " + str(exc), file=sys.stderr)
        return 1
    except BrokenPipeError:
        # `petit ... | head` is normal usage, not an error.
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
