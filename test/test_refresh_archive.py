"""refresh.py's raw archive: whole logs, scrubbed as one, xz on disk."""

from __future__ import annotations

import importlib.util
import lzma
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "refresh", ROOT / "tools" / "fingerprints" / "refresh.py"
)
assert _SPEC is not None
assert _SPEC.loader is not None
refresh = importlib.util.module_from_spec(_SPEC)
sys.modules["refresh"] = refresh
_SPEC.loader.exec_module(refresh)


def read(path: Path) -> list[str]:
    return lzma.decompress(path.read_bytes()).decode().splitlines()


def test_both_boots_are_kept_whole_and_share_one_address_map(tmp_path):
    files = {
        "previous.log": "a: lease 10.1.2.3\nb: mac 52:54:00:12:34:56\n",
        "current.log": "c: lease 10.1.2.3\nd: dns 10.9.9.9\ne: done\n",
        "kernel": "6.12.0\n",
        "os-release": 'NAME="Test"\n',
    }
    refresh.archive_raw(files, tmp_path)
    previous, current = read(tmp_path / "previous.log.xz"), read(tmp_path / "current.log.xz")
    assert len(previous) == 2
    assert len(current) == 3
    assert previous[0] == "a: lease 192.0.2.1"
    assert current[0] == "c: lease 192.0.2.1"
    assert current[1] == "d: dns 192.0.2.3"
    assert "52:54:00:12:34:56" not in previous[1]
    assert (tmp_path / "kernel").read_text() == "6.12.0\n"
    assert (tmp_path / "os-release").exists()


def test_messages_only_release(tmp_path):
    refresh.archive_raw({"messages.log": "x\ny\n"}, tmp_path)
    assert read(tmp_path / "messages.log.xz") == ["x", "y"]
    assert sorted(p.name for p in tmp_path.iterdir()) == ["messages.log.xz"]


def test_a_leak_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh.socket, "gethostname", lambda: "leakyhost")
    with pytest.raises(SystemExit):
        refresh.archive_raw({"current.log": "hello from leakyhost\n"}, tmp_path / "out")
    assert not (tmp_path / "out").exists()
