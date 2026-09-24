#!/usr/bin/env python3
"""
sync_usi.py — bridge between the USI corpus and this job-search workspace.

USI (the "Unified Source of Information" - a repo you maintain outside this
workspace, located via the USI_HOME environment variable or a ~/USI default) is
the single source of truth for all profile information: one Markdown block per item,
each with YAML frontmatter, filterable by audience / type / tag. This script calls
USI's own neutral export API (scripts/build.py) and drops fresh context packs into
documents/usi/, which the /sync-usi skill then folds into the candidate profile
files under .claude/skills/job-application-assistant/ and CLAUDE.md.

It produces (in documents/usi/):
  usi-content.md   — every CV-surfaceable block (audience = cv), body only.
  usi-content.json — the same blocks WITH frontmatter. Needed for the itemized
                      skills, tools, project stacks, metrics and language levels,
                      which live in frontmatter and are absent from the .md pack.
  usi-strategy.md  — the meta blocks: positioning strategy + impact/bullet bank
                      (type = meta, all audiences, incl. private). Never quote
                      private strategy content in outgoing documents.

Run from the repo root:
    python tools/sync_usi.py

The USI repo location can be overridden with the USI_HOME environment variable.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# --- configuration ---------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
USI_HOME = Path(os.environ.get("USI_HOME", Path.home() / "USI"))
USI_BUILD = USI_HOME / "scripts" / "build.py"
OUT_DIR = REPO_ROOT / "documents" / "usi"

# Each pack = (output filename, extra build.py args).
PACKS = [
    ("usi-content.md", ["--audience", "cv", "--format", "context"]),
    ("usi-content.json", ["--audience", "cv", "--format", "json"]),
    ("usi-strategy.md", ["--type", "meta", "--format", "context"]),
]


def run_pack(filename: str, args: list[str]) -> None:
    out_path = OUT_DIR / filename
    cmd = [sys.executable, str(USI_BUILD), *args, "-o", str(out_path)]
    print(f"  -> {filename}: {' '.join(args)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(
            f"USI build failed for {filename}:\n{result.stdout}\n{result.stderr}"
        )
    print(f"     {result.stdout.strip()}")


def main() -> None:
    if not USI_BUILD.exists():
        sys.exit(
            f"Could not find the USI export API at:\n  {USI_BUILD}\n"
            f"Set USI_HOME to the USI repo root, e.g.\n"
            f'  set USI_HOME=C:\\path\\to\\USI   (cmd)\n'
            f'  $env:USI_HOME="C:\\path\\to\\USI" (PowerShell)'
        )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Syncing profile source packs from USI at: {USI_HOME}")
    for filename, args in PACKS:
        run_pack(filename, args)
    print(f"Done. Packs written to: {OUT_DIR.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
