# Reports

`--daemon`, `--host` and `--wordcount` count a log by one field instead of
by the whole line: which programs are talking, which machines are talking,
and which words they use most.

## Why it matters

Before reading any lines, it helps to know the shape of a log. A daemon
report shows that the kernel wrote most of it; a host report shows that one
machine out of forty wrote half of it. A word count surfaces the vocabulary:
if `error`, `warning` or `fatal` is near the top, start there. It's also the
quickest way to pick words to alert on in a tool like swatch.

## How it works

The entry driver picks out the daemon and host of each record (see
[Reading logs](reading-logs.md)). `--daemon` and `--host` group on those
fields, with numbers such as PIDs taken out so `sshd[4478]` and `sshd[4502]`
count together. `--wordcount` splits each message into words, scrubs
them with `src/petit/data/filters/words.stopwords` so that numbers, dates
and IDs don't count as vocabulary, and counts what's left.
A log whose driver finds no daemon or host (RawEntry) has nothing to report
on for those two.

## Example

```
$ petit --daemon messages | head -8
760:	kernel:
36:	NetworkManager:
29:	sshd[#]:
18:	clurgmgrd:
16:	crond(pam_unix)[#]:
15:	avahi-daemon[#]:
13:	rc.sysinit:
10:	sshd(pam_unix)[#]:

$ petit --host messages | head -3
651:	blackdaemon
313:	seth
19:	tate.eyemg.com

$ petit --wordcount messages | head -5
75:	ACPI:
65:	succeeded
60:	root
52:	usb
51:	<info>
```

Reports compose with the shell. To see what one daemon said:

```
grep clurgmgrd /var/log/messages | petit --hash
```

## Related

- [Hashing](hashing.md): group by the whole line
- [Graphs](graphs.md): the same log counted by time
