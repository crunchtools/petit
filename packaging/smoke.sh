#!/bin/sh
# Installs the package from /pkg and checks petit against test/output/.
# Run by packaging/Containerfile's smoke stage, once per target distro.
# Needs PKG_KIND (rpm or deb) and VERSION; fixtures are under /t.
set -eu

if [ "$PKG_KIND" = deb ]; then
    apt-get update
    apt-get install -y /pkg/petit_*.deb
elif command -v zypper >/dev/null; then
    zypper --non-interactive install --allow-unsigned-rpm /pkg/petit-*.rpm
else
    dnf install -y /pkg/petit-*.rpm
fi

petit --version
test "$(petit --version)" = "Version: $VERSION"
# cksum, not diff: minimal images ship coreutils but not diffutils.
for mode in hash wordcount; do
    petit "--$mode" /t/data/test01.log > "/tmp/$mode.out"
    if [ "$(cksum < "/tmp/$mode.out")" != "$(cksum < "/t/output/test01-$mode.output")" ]; then
        echo "petit --$mode differs from test/output/test01-$mode.output" >&2
        cat "/tmp/$mode.out" >&2
        exit 1
    fi
done
