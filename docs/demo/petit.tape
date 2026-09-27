# The petit demo in the README and on crunchtools.com.
#
# Render from the repository root:
#
#   podman build -t petit-vhs docs/demo
#   podman run --rm -v .:/vhs:Z petit-vhs docs/demo/petit.tape
#
# The logs are test fixtures from 2010: an sshd log and a syslog from the
# eyemg servers petit was written for.

Output docs/demo/petit.gif
Output docs/demo/petit.mp4

Set Shell bash
Set FontSize 18
Set Width 1200
Set Height 720
Set Padding 24
Set Theme "GruvboxDark"
Set TypingSpeed 45ms

Hide
Type "cd $(mktemp -d) && cp /vhs/test/data/test08.log secure && cp /vhs/test/data/test06.log messages && PS1='$ ' && clear"
Enter
Show

Type "wc -l secure"
Sleep 400ms
Enter
Sleep 1.5s

Type "petit --hash secure"
Sleep 400ms
Enter
Sleep 4s

Type "petit --graph secure"
Sleep 400ms
Enter
Sleep 4s

Type "clear"
Enter
Type "petit --daemon messages | head -8"
Sleep 400ms
Enter
Sleep 3s

Type "petit --wordcount messages | head -8"
Sleep 400ms
Enter
Sleep 4s
