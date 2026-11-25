"""Contract check, run inside the built image by sdlc's `contract` check.

The shipped `petit` starts and hashes the fixture log exactly as the committed
output says. Was container.yml's boot-command, which sdlc 0.15's image job does
not run (crunchtools/sdlc#118).
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    subprocess.run(["petit", "--version"], check=True)
    got = subprocess.run(
        ["petit", "--hash", str(ROOT / "test/data/test01.log")],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    want = (ROOT / "test/output/test01-hash.output").read_text()
    if got.rstrip("\n") != want.rstrip("\n"):
        print("petit --hash test01.log does not match test/output/test01-hash.output")
        return 1
    print("contract: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
