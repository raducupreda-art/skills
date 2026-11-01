#!/usr/bin/env python3
"""Let the model call the skills listed in unlocked.txt: drop their
disable-model-invocation line. A listed skill that is gone or already open stops the sync."""
import pathlib
import sys

FLAG = "disable-model-invocation: true\n"


def unlock(root, names):
    root = pathlib.Path(root)
    found = {path.parent.name: path for path in root.rglob("SKILL.md")}
    for name in names:
        if name not in found:
            raise SystemExit(f"unlock: {name} is gone upstream")
        text = found[name].read_text()
        head, sep, body = text.partition("\n---\n")
        if FLAG not in head + "\n":
            raise SystemExit(f"unlock: {name} is no longer locked upstream")
        found[name].write_text((head + "\n").replace(FLAG, "").rstrip("\n") + sep + body)


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    unlock(sys.argv[1], (here / "unlocked.txt").read_text().split())
