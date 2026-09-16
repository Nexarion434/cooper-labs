#!/usr/bin/env python3
"""Rebuild every shipped HTML from its description, with relative asset paths.

    python3 assets/scripts/rebuild_html.py      # templates/ and examples/, in place

Run it after a change to the CSS, to a builder or to a description: the HTML
files next to the JSON are what a reader opens and what `new_doc.py` copies,
so they must never lag behind the engine. Each file is built with `--relative`
(`../css/`, `../img/`), the way it is shipped.
"""
import sys, subprocess, pathlib


def _root(name):
    """assets/, wherever this script sits: the marketplace repo, or the scratch tree."""
    here = pathlib.Path(__file__).resolve()
    for base in (here.parent, *here.parents[1:3]):
        for cand in (base / "plugins" / name / "assets", base / "plugin" / "assets", base / "assets"):
            if (cand / "scripts" / "build_doc.py").exists():
                return cand
    sys.exit("no assets/ found next to this script")


ROOT = _root("cooper-brand")
S = ROOT / "scripts"

BUILDER = {"social": "build_social.py", "deck": "build_deck.py", "fact-sheet": "build_fact_sheet.py",
           "note": "build_note.py", "quote": "build_quote.py"}


def builder(stem):
    for key, script in BUILDER.items():
        if stem == key or stem.startswith(key + "-"):
            return script
    return "build_doc.py"


def main():
    bad = 0
    for folder in ("templates", "examples"):
        for j in sorted((ROOT / folder).glob("*.json")):
            out = j.with_suffix(".html")
            cmd = [sys.executable, str(S / builder(j.stem)), str(j), str(out), "--relative"]
            r = subprocess.run(cmd, capture_output=True, text=True)
            print(("ok   " if r.returncode == 0 else "FAIL ") + f"{folder}/{out.name}  {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()}")
            bad += r.returncode != 0
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
