# Graphs

A graph counts log entries per slice of time and draws one column per slice
in the terminal, tallest where the log was busiest.

## Why it matters

Counts tell you what happened; a graph tells you when. A spike at 03:00
every night is a cron job. A spike at 14:22 on one Tuesday is the incident.
Graphs pair well with `grep`: graph only the errors and see whether they
cluster.

```
cat /var/log/messages | grep error | petit --mgraph
```

## How it works

Every graph is built from one unit. The axis under the graph labels the
first, middle and last column with that column's starting value in its unit,
so an hour graph reads 00-23, not a date; Start Time and End Time give the
full dates.

| Unit   | Fixed graph | Columns | `--span` example | `--graph` column sizes | Axis label           |
|--------|-------------|---------|------------------|------------------------|----------------------|
| second | `--sgraph`  | 60      | `30s`            | 1, 5, 15, 30 s         | second of the minute |
| minute | `--mgraph`  | 60      | `45m`            | 1, 5, 15, 30 m         | minute of the hour   |
| hour   | `--hgraph`  | 24      | `36h`            | 1, 2, 3, 6, 12 h       | hour of the day, 00-23 |
| day    | `--dgraph`  | 31      | `45d`            | 1, 2, 7 d              | day of the month     |
| month  | `--mograph` | 12      | `18mo`           | 1, 3, 6 mo             | month, 01-12         |
| year   | `--ygraph`  | 10      | `12y`            | 1, 5, 10 y             | year, last two digits |

Three ways to choose the window:

- **`--sgraph` … `--ygraph`**: a fixed number of one-unit columns starting
  at the first line of the log.
- **`--span N<unit>`**: N one-unit columns starting at the first line, e.g.
  `--span 90m`. Units: s, m, h, d, mo, y. N is at least 6, and the graph
  must fit the terminal or petit exits 2.
- **`--graph`**: the whole log, earliest entry to latest. petit picks the
  finest column size from the table that fits the terminal and draws only
  the columns the log covers. Three and a half days is 84 one-hour columns
  on a 120-column terminal, or 42 two-hour columns on 80. Logs out of time
  order are fine: the window runs from the earliest entry, wherever it is.

**Where a column starts.** The window starts at the entry's time floored to
the unit: 10:07:12 becomes 10:07 for minutes, 10:00 for hours, the 1st of
the month for months. When a column spans several units it also starts on a
round value: 15-minute columns at :00/:15/:30/:45, 2-hour columns on even
hours, 3-month columns in Jan/Apr/Jul/Oct, 5-year columns on years ending in
0 or 5. Days are the exception: multi-day columns start on the entry's own
day, because months don't divide into 2 or 7 days. Months and years are
counted on the calendar, so every month column is exactly one calendar month.

**The summary lines.** Start Time and End Time are the starts of the first
and last columns. Duration is the whole window, with the column size when a
column spans several units. Minimum and Maximum Value are the fewest and
most entries in any one column, and Scale is how many entries one row of the
graph stands for.

**Width.** The terminal width comes from `$COLUMNS` or the terminal itself,
and is 80 when petit's output is piped. Two characters are kept for the axis
labels, which run past the last column. `--wide` draws each column two
characters wide, so it fits half as many. `--tick` changes the character
used to draw.

**Lines without a time.** Lines petit can't read a time from are stamped
with the year 1900, so they fall outside any window that starts at a real
time. `--graph` ignores them unless no line in the log has a time.

## Example

Five days of an Apache error log on an 80-column terminal: 60 two-hour
columns, labelled 04:00 on the 10th, 16:00 on the 12th and 02:00 on the
15th.

```
$ petit --graph /var/log/httpd/error_log
    #                       #                #
    #                       ##               #    #
#   #             #         ##  # #        # #    #  #
#  ###            #         ##  # #####    # ##   #  ####  #
# ####  # ## #### # #   #  ###### ######  #####   # ##### ##
############################################################
04                            16                           02

Start Time:	 2011-04-10 04:00:00 		Minimum Value: 0
End Time:	 2011-04-15 02:00:00 		Maximum Value: 7
Duration:	 120 hours (2-hour columns) 			Scale: 1.1666666666666667
```

A log petit has no driver for can still be graphed if the time is moved to
where a driver expects it. Here awk blanks the fields of an Apache error log
that get in the way:

```
cat /var/log/httpd/error_log | awk '{$1="";$5="";print}' | petit --sgraph
```

## Related

- [Reports](reports.md): counts by daemon, host and word
- [Reading logs](reading-logs.md): which timestamps petit recognises
