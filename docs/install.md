# Install

petit ships as native packages for the major Linux distributions, as a
Python package on PyPI, and as a container image.

## Why it matters

A log tool is most useful on the machine with the logs, which is usually a
server with no development tools on it. The native packages install from a
signed repository and update with the rest of the system.

## How it works

### Native packages

From the signed repositories at https://crunchtools.github.io/packages:

```bash
# Fedora, RHEL 8/9/10 and rebuilds, Amazon Linux 2023
sudo curl -fsSLo /etc/yum.repos.d/crunchtools.repo \
    https://crunchtools.github.io/packages/rpm/crunchtools.repo
sudo dnf install petit

# SUSE Linux Enterprise 15 SP7 and 16
sudo zypper addrepo https://crunchtools.github.io/packages/rpm/crunchtools.repo
sudo zypper install petit

# Debian 12 and 13, Ubuntu 24.04 and 26.04
sudo install -d /etc/apt/keyrings
sudo curl -fsSLo /etc/apt/keyrings/crunchtools.asc \
    https://crunchtools.github.io/packages/crunchtools.asc
sudo curl -fsSLo /etc/apt/sources.list.d/crunchtools.sources \
    https://crunchtools.github.io/packages/deb/crunchtools.sources
sudo apt update && sudo apt install petit
```

The signing key's fingerprint is
`588C E8BF 2F36 D77E 1B1E  545C C04F 530D 3931 F683`. Each GitHub release
also carries the .rpm and .deb for a one-off install
(`dnf install ./petit-*.rpm`, `apt install ./petit_*.deb`).

The packages install petit in `/usr/lib/petit` and run it on the newest
Python 3.11 or later the system has; on RHEL 8 and 9 that pulls in the
python3.12 package. Ubuntu 22.04 and Debian 11 have no supported Python
3.11, so use pipx there.

### PyPI

```bash
pip install petit-log-crunchtools
# or: uv tool install petit-log-crunchtools
# or: pipx install petit-log-crunchtools
```

Installs the `petit` command and the `petit` library. The PyPI distribution
is named `petit-log-crunchtools`, not `petit`, because `petit` on PyPI
belongs to an unrelated project. It follows the same naming convention as
the rest of the crunchtools fleet (`gatehouse-crunchtools`,
`mcp-gemini-crunchtools`); see the 3.0.0 and 3.1.1 entries in
[CHANGELOG.md](../CHANGELOG.md).

### Container

For CI or isolated execution:

```bash
podman run --rm -v $(pwd):/data:ro,Z quay.io/crunchtools/petit --hash /data/some.log
```

## Example

The same package, installed from the repository into a Debian 13 image, is
what records the demo in the README; see
[docs/demo/Containerfile](demo/Containerfile).

## Related

- [Hashing](hashing.md): what to run first
- [Library](library.md): using petit from Python
