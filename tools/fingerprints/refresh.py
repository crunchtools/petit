#!/usr/bin/env python3
"""Keep petit's reboot fingerprint corpora current (#37).

The corpora are logs of one clean reboot of each supported Linux release.
This captures them the same way every time, from each distribution's own
cloud image booted under QEMU/KVM, so that a scheduled workflow can notice a
new release, or drift in an old one, and propose the change as a PR.

    refresh.py check [--only IDS]          what is supported, and what to do
    refresh.py capture ID --out DIR        boot ID and capture its reboot
    refresh.py propose DIR                 turn captures into corpora and verify logs
    refresh.py verify                      every verify log matches its corpus first
    refresh.py report                      how the corpora overlap, as markdown

`captured.json` records what each committed capture came from. It is the
lock file: a release leaves it only when endoflife.date says it is over.
"""

from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import ipaddress
import json
import lzma
import os
import re
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, TypeVar

from petit import LogHash
from petit.api import analyze_text

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST = HERE / "platforms.toml"
LOCK = HERE / "captured.json"
GUEST = HERE / "guest"
CORPORA = ROOT / "src" / "petit" / "data" / "fingerprints"
VERIFY = ROOT / "test" / "data" / "verify"


EOL_API = "https://endoflife.date/api/v1/products/{}"
FEDORA_RELEASES = "https://fedoraproject.org/releases.json"
ALPINE_CLOUD = "https://dl-cdn.alpinelinux.org/alpine/v{version}/releases/cloud/"
USER_AGENT = "petit-fingerprint-refresh (+https://github.com/crunchtools/petit)"

# A recaptured reboot that still names its corpus first, but scores below
# this, has drifted far enough that the corpus is replaced.
IDENTITY_FLOOR = 0.5
BOOT_TIMEOUT = 1800
DOWNLOAD_TIMEOUT = 600
DISK_SIZE = "20G"
OUTPUT_DISK_BYTES = 64 << 20
CHUNK_BYTES = 1 << 20
MARKER = "petit-capture"
RETRY_DELAYS = (10, 30, 90)

T = TypeVar("T")


@dataclass(frozen=True)
class Platform:
    """One release of one family: what to boot and what it fingerprints."""

    id: str
    family: str
    version: str
    role: str
    corpus: str
    log: str
    source: str
    image: str
    checksum: str

    @property
    def corpus_file(self) -> str:
        return f"{self.corpus}-reboot.fp"

    @property
    def verify_log(self) -> Path:
        return VERIFY / self.corpus_file / f"{self.id}.log"

    @property
    def captures(self) -> int:
        """A corpus needs a second, independent reboot to verify it."""
        return 2 if self.role == "corpus" else 1


# --- what is supported -------------------------------------------------------


def retrying(what: str, attempt: Callable[[], T]) -> T:
    """Mirrors reset connections and time out handshakes; try again before
    failing a capture over it."""
    for delay in RETRY_DELAYS:
        try:
            return attempt()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            print(f"{what}: {error}; retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)
    return attempt()


def fetch(url: str) -> bytes:
    def once() -> bytes:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            return bytes(response.read())

    return retrying(url, once)


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", version))


def supported(family: dict[str, Any]) -> list[dict[str, Any]]:
    """endoflife.date's supported releases of `family`, newest first."""
    if "eol_product" not in family:
        return [{"name": "", "codename": ""}]
    releases = json.loads(fetch(EOL_API.format(family["eol_product"])))["result"]["releases"]
    keep = [
        r
        for r in releases
        if not r.get("isEol")
        and (r.get("isLts") or not family.get("lts_only"))
        and version_key(r["name"])[0] >= family.get("min_major", 0)
    ]
    return sorted(keep, key=lambda r: version_key(r["name"]), reverse=True)


def platforms(only: set[str] | None = None) -> list[Platform]:
    manifest = tomllib.loads(MANIFEST.read_text())
    found = []
    for family in manifest["family"]:
        releases = supported(family)
        if family["releases"] == "latest":
            releases = releases[: 1 + family.get("previous", 0)]
        for index, release in enumerate(releases):
            if family["releases"] == "all":
                found.append(make_platform(family, release, family["role"]))
            else:
                # The releases before the newest verify the newest's corpus.
                found.append(
                    make_platform(
                        family,
                        release,
                        family["role"] if index == 0 else "verify",
                        corpus_from=releases[0],
                    )
                )
    return [p for p in found if only is None or p.id in only]


def template_fields(release: dict[str, Any]) -> dict[str, str]:
    version = release["name"]
    return {
        "version": version,
        "major": version.split(".")[0],
        "codename": (release.get("codename") or "").split(" ")[0].lower(),
    }


def make_platform(
    family: dict[str, Any],
    release: dict[str, Any],
    role: str,
    corpus_from: dict[str, Any] | None = None,
) -> Platform:
    version = release["name"]
    fields = template_fields(release)
    return Platform(
        id=f"{family['name']}{version}",
        family=family["name"],
        version=version,
        role=role,
        corpus=family["corpus"].format(**template_fields(corpus_from or release)),
        log=family.get("log", "journal"),
        source=family.get("source", "cloud"),
        image=family.get("image", "").format(**fields),
        checksum=family.get("checksum", "").format(**fields),
    )


def load_lock() -> dict[str, dict[str, str]]:
    return json.loads(LOCK.read_text()) if LOCK.exists() else {}


def cmd_check(args: argparse.Namespace) -> int:
    only = set(args.only.split(",")) if args.only else None
    current = platforms()
    lock = load_lock()
    wanted = [p for p in current if only is None or p.id in only]
    plan = {
        "capture": [{"id": p.id, "action": "recheck" if p.id in lock else "new"} for p in wanted],
        "retire": sorted(set(lock) - {p.id for p in current}),
    }
    text = json.dumps(plan, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n")
    print(text)
    return 0


# --- getting an image --------------------------------------------------------


def resolve(platform: Platform) -> tuple[str, str]:
    """The image URL and its expected digest, `algorithm:hex`."""
    if platform.family == "fedora":
        for entry in json.loads(fetch(FEDORA_RELEASES)):
            if (
                entry["version"] == platform.version
                and entry["arch"] == "x86_64"
                and entry["subvariant"] == "Cloud_Base"
                and entry["link"].endswith(".qcow2")
            ):
                return entry["link"], "sha256:" + entry["sha256"]
        raise SystemExit(f"{platform.id}: no Cloud_Base qcow2 in {FEDORA_RELEASES}")
    image, checksum = platform.image, platform.checksum
    if platform.family == "alpine":
        image = alpine_image(platform.version)
        checksum = image + ".sha512"
    return image, digest_from(fetch(checksum).decode(), image.rsplit("/", 1)[1])


def alpine_image(version: str) -> str:
    listing = fetch(ALPINE_CLOUD.format(version=version)).decode()
    pattern = re.compile(
        rf"alpine-{re.escape(version)}\.(\d+)-x86_64-(?:bios-)?cloudinit-r(\d+)\.qcow2"
    )
    names = {m.group(0): (int(m.group(1)), int(m.group(2))) for m in pattern.finditer(listing)}
    if not names:
        raise SystemExit(f"alpine{version}: no x86_64 cloud-init image listed")
    return ALPINE_CLOUD.format(version=version) + max(names, key=names.__getitem__)


def digest_from(text: str, filename: str) -> str:
    """Find `filename`'s digest in a checksum file, whichever style it uses."""
    lines = [line for line in text.splitlines() if line.strip() and not line.startswith("#")]
    candidates = [line for line in lines if filename in line] or (lines if len(lines) == 1 else [])
    for line in candidates:
        match = re.search(r"\b([0-9a-f]{128}|[0-9a-f]{64})\b", line)
        if match:
            algorithm = "sha512" if len(match.group(1)) == 128 else "sha256"
            return f"{algorithm}:{match.group(1)}"
    raise SystemExit(f"no checksum for {filename}")


def download(url: str, digest: str, cache: Path) -> Path:
    algorithm, expected = digest.split(":")
    target = cache / f"{expected[:16]}-{url.rsplit('/', 1)[1]}"
    if target.exists():
        return target
    cache.mkdir(parents=True, exist_ok=True)
    retrying(url, lambda: download_once(url, algorithm, expected, target))
    return target


def download_once(url: str, algorithm: str, expected: str, target: Path) -> None:
    hasher = hashlib.new(algorithm)
    partial = target.with_suffix(".part")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with (
        urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT) as response,
        partial.open("wb") as out,
    ):
        while chunk := response.read(CHUNK_BYTES):
            hasher.update(chunk)
            out.write(chunk)
    if hasher.hexdigest() != expected:
        partial.unlink()
        raise SystemExit(f"{url}: {algorithm} mismatch")
    partial.rename(target)


# --- booting it --------------------------------------------------------------


def user_data(platform: Platform) -> str:
    def encoded(name: str) -> str:
        return base64.b64encode((GUEST / name).read_bytes()).decode()

    template = (GUEST / f"user-data-{platform.log}.yaml").read_text()
    return template.format(
        script=encoded("petit-capture.sh"), unit=encoded("petit-capture.service")
    )


def make_seed(platform: Platform, work: Path) -> Path:
    (work / "user-data").write_text(user_data(platform))
    (work / "meta-data").write_text(f"instance-id: {platform.id}\nlocal-hostname: host01\n")
    seed = work / "seed.iso"
    files = [str(work / "user-data"), str(work / "meta-data")]
    if shutil.which("cloud-localds"):
        subprocess.run(["cloud-localds", str(seed), *files], check=True)
        return seed
    for tool in (["xorriso", "-as", "mkisofs"], ["genisoimage"], ["mkisofs"]):
        if shutil.which(tool[0]):
            subprocess.run(
                [
                    *tool,
                    "-quiet",
                    "-output",
                    str(seed),
                    "-volid",
                    "cidata",
                    "-joliet",
                    "-rock",
                    *files,
                ],
                check=True,
            )
            return seed
    raise SystemExit("need cloud-localds, xorriso, genisoimage or mkisofs for the seed")


def qemu() -> str:
    for candidate in ("qemu-system-x86_64", "/usr/libexec/qemu-kvm"):
        if shutil.which(candidate):
            return candidate
    raise SystemExit("need qemu-system-x86_64")


def boot(base: Path, seed: Path | None, work: Path) -> dict[str, str]:
    """Boot a throwaway overlay of `base` until the guest powers off."""
    disk, out = work / "disk.qcow2", work / "out.img"
    subprocess.run(
        [
            "qemu-img",
            "create",
            "-q",
            "-f",
            "qcow2",
            "-F",
            "qcow2",
            "-b",
            str(base),
            str(disk),
            DISK_SIZE,
        ],
        check=True,
    )
    with out.open("wb") as blank:
        blank.truncate(OUTPUT_DISK_BYTES)
    command = [
        qemu(),
        "-machine",
        "q35,accel=kvm",
        "-cpu",
        "host",
        "-m",
        "2048",
        "-smp",
        "2",
        "-display",
        "none",
        "-monitor",
        "none",
        "-serial",
        f"file:{work / 'console.log'}",
        "-drive",
        f"file={disk},if=none,id=root,format=qcow2",
        "-device",
        "virtio-blk-pci,drive=root,bootindex=0",
        "-drive",
        f"file={out},if=none,id=out,format=raw",
        "-device",
        "virtio-blk-pci,drive=out,serial=petitout",
        "-netdev",
        "user,id=net0",
        "-device",
        "virtio-net-pci,netdev=net0,mac=52:54:00:00:00:01",
    ]
    if seed:
        # A virtio disk, not a CD-ROM: Debian 12's cloud kernel has no SATA
        # CD driver, and NoCloud finds a `cidata` volume on any block device.
        command += ["-drive", f"file={seed},if=virtio,format=raw,readonly=on"]
    subprocess.run(command, check=True, timeout=BOOT_TIMEOUT)
    files: dict[str, str] = {}
    with tarfile.open(out) as archive:
        for member in archive.getmembers():
            handle = archive.extractfile(member) if member.isfile() else None
            if handle:
                files[member.name.removeprefix("./")] = handle.read().decode(errors="replace")
    if not files:
        raise SystemExit(f"guest wrote no capture; see {work / 'console.log'}")
    return files


# --- cutting out the event ---------------------------------------------------


def is_marker(line: str, word: str) -> bool:
    return MARKER in line and line.rstrip().endswith(word)


def last_index(lines: list[str], test: Any) -> int:
    for index in range(len(lines) - 1, -1, -1):
        if test(lines[index]):
            return index
    raise SystemExit("capture is missing its markers")


def extract_event(files: dict[str, str]) -> list[str]:
    """From the reboot request through the end of the next startup."""
    if "messages.log" in files:
        lines = files["messages.log"].splitlines()
        start = last_index(lines, lambda line: is_marker(line, "rebooting"))
        end = last_index(lines, lambda line: is_marker(line, "capturing"))
        event = lines[start + 1 : end]
    else:
        previous = files["previous.log"].splitlines()
        current = files["current.log"].splitlines()
        start = last_index(previous, lambda line: is_marker(line, "rebooting"))
        finished = [
            i
            for i, line in enumerate(current)
            if re.search(r"systemd\[1\]: Startup finished", line)
        ]
        end = (
            finished[0]
            if finished
            else last_index(current, lambda line: is_marker(line, "capturing"))
        )
        event = previous[start + 1 :] + current[: end + 1]
    return [line for line in event if MARKER not in line and not line.startswith("-- ")]


MAC = re.compile(r"(?<![\w:])(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}(?![\w:])")
IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
IPV6 = re.compile(r"(?<![\w:])(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}(?![\w:])")
UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
HEX_ID = re.compile(r"\b[0-9a-f]{32}\b")
KEEP_IPV4 = {"0.0.0.0", "127.0.0.1", "255.255.255.255"}


def scrub(lines: list[str]) -> list[str]:
    """Rewrite what identifies the machine to the constitution's roster (§XVII):
    RFC 5737 and RFC 3849 addresses, RFC 7042 MACs, zeroed IDs."""
    seen: dict[str, str] = {}

    def swap(value: str, fresh: str) -> str:
        return seen.setdefault(value, fresh.format(len(seen) + 1))

    def ipv4(match: re.Match[str]) -> str:
        text = match.group(0)
        try:
            ipaddress.IPv4Address(text)
        except ValueError:
            return text
        # Netmasks and the wildcard say nothing about the machine.
        return text if text in KEEP_IPV4 or text.startswith("255.") else swap(text, "192.0.2.{}")

    def ipv6(match: re.Match[str]) -> str:
        text = match.group(0)
        if ("::" not in text and text.count(":") < 4) or MAC.fullmatch(text):
            return text
        return text if text == "::1" else swap(text, "2001:db8::{}")

    out = []
    for line in lines:
        text = MAC.sub(lambda m: swap(m.group(0), "00:00:5e:00:53:{:02x}"), line)
        text = UUID.sub("00000000-0000-0000-0000-000000000000", text)
        text = HEX_ID.sub("0" * 32, text)
        out.append(IPV6.sub(ipv6, IPV4.sub(ipv4, text)))
    return out


def assert_clean(lines: list[str]) -> None:
    """Refuse to write a capture that still names the machine that made it."""
    text = "\n".join(lines)
    names = {socket.gethostname().split(".")[0], os.environ.get("USER", "")}
    leaks = [
        name for name in names if len(name) >= 4 and re.search(rf"\b{re.escape(name)}\b", text)
    ]
    for match in IPV4.finditer(text):
        try:
            address = ipaddress.IPv4Address(match.group(0))
        except ValueError:
            continue
        if (
            match.group(0) not in KEEP_IPV4
            and not match.group(0).startswith("255.")
            and address not in ipaddress.ip_network("192.0.2.0/24")
        ):
            leaks.append(match.group(0))
    if leaks:
        raise SystemExit(f"capture still carries {sorted(set(leaks))}; not writing it")


RAW_LOGS = ("previous.log", "current.log", "messages.log")


def archive_raw(files: dict[str, str], dest: Path) -> None:
    """Keep every log the guest wrote, whole, for crunchtools/petit-captures.

    The logs are scrubbed together, so one address maps to one stand-in
    across both boots, and xz-compressed; kernel and os-release are copied.
    """
    logs = {name: files[name].splitlines() for name in RAW_LOGS if name in files}
    clean = scrub([line for lines in logs.values() for line in lines])
    assert_clean(clean)
    dest.mkdir(parents=True, exist_ok=True)
    start = 0
    for name, lines in logs.items():
        end = start + len(lines)
        text = "".join(line + "\n" for line in clean[start:end])
        (dest / f"{name}.xz").write_bytes(lzma.compress(text.encode()))
        start = end
    for name in ("kernel", "os-release"):
        if name in files:
            (dest / name).write_text(files[name])


def cmd_capture(args: argparse.Namespace) -> int:
    matches = platforms({args.platform}) if not args.image else []
    if not args.image and not matches:
        raise SystemExit(f"{args.platform}: not a supported platform (see `check`)")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    platform = matches[0] if matches else manual_platform(args)
    image, digest = (args.image, "local") if args.image else ("", "")
    with tempfile.TemporaryDirectory(prefix="petit-capture-") as scratch:
        work = Path(args.work or scratch)
        work.mkdir(parents=True, exist_ok=True)
        if args.image:
            base = Path(args.image).resolve()
        else:
            image, digest = resolve(platform)
            base = download(image, digest, Path(args.cache))
        runs = args.captures or platform.captures
        for run in range(runs):
            attempt = work / f"boot{run}"
            attempt.mkdir()
            seed = make_seed(platform, attempt) if platform.source == "cloud" else None
            files = boot(base, seed, attempt)
            event = scrub(extract_event(files))
            assert_clean(event)
            (out / f"{'ab'[run]}.log").write_text("\n".join(event) + "\n")
            archive_raw(files, out / "raw" / "ab"[run])
            os_name = re.search(r'^PRETTY_NAME="?([^"\n]*)', files.get("os-release", ""), re.M)
    meta = {
        **asdict(platform),
        "image": image,
        "digest": digest,
        "kernel": files.get("kernel", "").strip(),
        "os": os_name.group(1) if os_name else "",
        "captured": datetime.date.today().isoformat(),
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"{platform.id}: {runs} capture(s) in {out}")
    return 0


def manual_platform(args: argparse.Namespace) -> Platform:
    """`--image guest.qcow2 --as verify:el9`: a capture by hand, outside the manifest."""
    role, _, corpus = args.as_.partition(":")
    if role not in {"corpus", "verify"} or not corpus:
        raise SystemExit("--image needs --as corpus:NAME or --as verify:NAME")
    return Platform(
        id=args.platform,
        family=args.platform,
        version="",
        role=role,
        corpus=corpus,
        log=args.log,
        source="cloud" if args.seed else "image",
        image="",
        checksum="",
    )


# --- judging captures --------------------------------------------------------


def first_match(text: str, corpus_file: str) -> tuple[bool, float, str]:
    """Whether `text` names `corpus_file` first, its identity score, and
    what came first."""
    result = analyze_text(text, collapse_fingerprints=True)
    first = result.fingerprints_matched[0] if result.fingerprints_matched else ""
    identity = next((s.identity for s in result.fingerprint_scores if s.name == corpus_file), 0.0)
    return corpus_file in first.split("|"), identity, first


def cmd_verify() -> int:
    failed = 0
    for log in sorted(VERIFY.glob("*.fp/*.log")):
        ok, identity, first = first_match(log.read_text(), log.parent.name)
        failed += not ok
        print(
            f"{'ok ' if ok else 'BAD'} {log.relative_to(VERIFY)}  identity={identity:.2f}"
            f"  first={first or '-'}"
        )
    return 1 if failed else 0


def managed_corpora() -> list[str]:
    return sorted(
        {
            f"{entry['corpus']}-reboot.fp"
            for entry in load_lock().values()
            if entry["role"] == "corpus"
        }
    )


def overlap_report() -> str:
    corpora, _weights = LogHash._load_corpora()
    keys = {name: set(found) for name, found in corpora}
    names = [name for name in managed_corpora() if name in keys]
    lines = [
        "### Corpus overlap (Jaccard of fingerprint keys)",
        "",
        "| | " + " | ".join(n.removesuffix("-reboot.fp") for n in names) + " |",
        "|---" * (len(names) + 1) + "|",
    ]
    for a in names:
        cells = [f"{len(keys[a] & keys[b]) / len(keys[a] | keys[b]):.2f}" for b in names]
        lines.append(f"| {a.removesuffix('-reboot.fp')} | " + " | ".join(cells) + " |")
    lines += ["", "### Verify logs", "", "| log | first match | identity |", "|---|---|---|"]
    for log in sorted(VERIFY.glob("*.fp/*.log")):
        ok, identity, first = first_match(log.read_text(), log.parent.name)
        mark = "" if ok else " ✗"
        lines.append(f"| {log.relative_to(VERIFY)} | {first or '-'}{mark} | {identity:.2f} |")
    return "\n".join(lines) + "\n"


def cmd_report() -> int:
    print(overlap_report(), end="")
    return 0


# --- proposing the change ----------------------------------------------------


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def adopt(meta: dict[str, Any], capture: Path, lock: dict[str, dict[str, str]]) -> str | None:
    """Commit one platform's captures if they change anything; say why."""
    platform = Platform(**{k: meta[k] for k in Platform.__dataclass_fields__})
    corpus = CORPORA / platform.corpus_file
    first = (capture / "a.log").read_text()
    if platform.id in lock and (platform.role == "verify" or corpus.exists()):
        ok, identity, named = first_match(first, platform.corpus_file)
        if ok and identity >= IDENTITY_FLOOR:
            return None
        reason = f"drifted: first match {named or '-'}, identity {identity:.2f}"
    else:
        reason = "new release"
    if platform.role == "corpus":
        write(corpus, first)
        write(platform.verify_log, (capture / "b.log").read_text())
    else:
        write(platform.verify_log, first)
        ok, identity, named = first_match(first, platform.corpus_file)
        if not ok:
            reason += f"; does NOT match {platform.corpus_file} first ({named or '-'})"
    lock[platform.id] = {
        k: str(meta[k])
        for k in (
            "family",
            "version",
            "role",
            "corpus",
            "image",
            "digest",
            "kernel",
            "os",
            "captured",
        )
    }
    return reason


def retire(ids: list[str], lock: dict[str, dict[str, str]]) -> list[str]:
    notes = []
    for platform_id in ids:
        entry = lock.pop(platform_id)
        corpus_file = f"{entry['corpus']}-reboot.fp"
        (VERIFY / corpus_file / f"{platform_id}.log").unlink(missing_ok=True)
        still_used = any(
            e["corpus"] == entry["corpus"] and e["role"] == "corpus" for e in lock.values()
        )
        if entry["role"] == "corpus" and not still_used:
            (CORPORA / corpus_file).unlink(missing_ok=True)
            shutil.rmtree(VERIFY / corpus_file, ignore_errors=True)
        notes.append(f"- `{platform_id}`: end of life, retired")
    return notes


def cmd_propose(args: argparse.Namespace) -> int:
    lock = load_lock()
    metas = [json.loads(p.read_text()) for p in sorted(Path(args.captures).glob("*/meta.json"))]
    # Corpora first, so a verify-only release is judged against the new ones.
    metas.sort(key=lambda meta: meta["role"] != "corpus")
    notes = []
    for meta in metas:
        reason = adopt(meta, Path(args.captures) / meta["id"], lock)
        if reason:
            notes.append(f"- `{meta['id']}` ({meta['os']}, kernel {meta['kernel']}): {reason}")
    current = {p.id for p in platforms()}
    notes += retire(sorted(set(lock) - current), lock)
    if not notes:
        print("no change")
        return 0
    LOCK.write_text(json.dumps(dict(sorted(lock.items())), indent=2) + "\n")
    body = (
        "Captured by `tools/fingerprints/refresh.py` under QEMU/KVM.\n\n"
        + "\n".join(notes)
        + "\n\n"
        + overlap_report()
    )
    if args.summary:
        Path(args.summary).write_text(body)
    print(body)
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as handle:
            handle.write("changed=true\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="list supported platforms and what to do")
    check.add_argument("--only", help="comma-separated platform ids to capture")
    check.add_argument("--output", help="also write the plan here")
    check.set_defaults(func=cmd_check)

    capture = sub.add_parser("capture", help="boot a platform and capture its reboot")
    capture.add_argument("platform")
    capture.add_argument("--out", required=True)
    capture.add_argument("--cache", default=str(Path.home() / ".cache" / "petit-images"))
    capture.add_argument("--work", help="keep disks and console logs here, not in a temp dir")
    capture.add_argument("--captures", type=int, help="override how many reboots to capture")
    capture.add_argument("--image", help="a local qcow2 instead of the manifest's")
    capture.add_argument("--as", dest="as_", default="", help="with --image: ROLE:CORPUS")
    capture.add_argument("--log", default="journal", choices=["journal", "messages"])
    capture.add_argument(
        "--seed",
        action="store_true",
        help="with --image: the image runs cloud-init, give it the seed",
    )
    capture.set_defaults(func=cmd_capture)

    propose = sub.add_parser("propose", help="adopt captures that change something")
    propose.add_argument("captures")
    propose.add_argument("--summary", help="write the PR body here")
    propose.set_defaults(func=cmd_propose)

    sub.add_parser("verify", help="check every verify log")
    sub.add_parser("report", help="overlap report")

    args = parser.parse_args(argv)
    if args.command == "verify":
        return cmd_verify()
    if args.command == "report":
        return cmd_report()
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
