"""Catch superseded figures left behind in hand-written prose.

Numbers computed from the YAML get copied into prose all over this repo: the
README, AGENTS.md, the ADRs, the category pages, the candidate notes. Then a
price or a measurement changes and every copy is silently wrong, with no way for a reader to tell
whether the reasoning around a stale number is stale too.

HOW THIS CHECK WORKS. It does not try to guess which numbers are wrong. It
keeps an explicit list of figures that WERE computed and no longer are, in
`figures-superseded.yaml`, and fails if one appears in a hand-written file
without being marked as deliberate history.

That design was chosen over the obvious alternative — compare every figure in
prose against everything the tool computes — because the obvious one cannot
tell a stale figure from an unrelated real one: "$299" can be a superseded
stroller price, and also, separately, the real price of a bassinet.

The list doubles as a changelog of every figure that has moved, and why.

WHEN YOU CHANGE A FIGURE: add the old value to `figures-superseded.yaml`, then
run `make check`. It will point at every stale copy. Fix them, or mark the ones
that are deliberate history.

TO QUOTE A SUPERSEDED FIGURE ON PURPOSE — as history, or to explain what
changed — put `figure-check: ignore` on the same line.

Two trees are never checked:

- `research/notes/` — dated snapshots. A note written in May should keep
  May's numbers; that is what a note is for.
- `docs/` — generated from the YAML, and already covered by candidates.py's staleness
  check.
"""

from __future__ import annotations

import re
from pathlib import Path

from tools import repo

#: Hand-written files that SUMMARISE the design. A summary must be current, or
#: it misleads the reader who trusts it.
#:
#: `candidates/items/*.yaml` notes are deliberately NOT here, for the same
#: reason `research/notes/` is not: they are an append-only, dated log of how
#: each candidate reached its current state. An entry recording "as of May it
#: was $499" is correct and useful. Rewriting it would destroy the reasoning
#: trail, and marking every historical figure would bury the prose in
#: markers. The authoritative current numbers live in `docs/`, which is
#: generated and cannot drift.
CHECKED_GLOBS = (
    "README.md",
    "AGENTS.md",
    "decisions/*.md",
    "categories/*/README.md",
    "household/household.yaml",
)

#: Not a decision, and its placeholder numbers are meant to be meaningless.
SKIPPED = ("decisions/0000-template.md",)

#: Put this on a line to exempt it.
IGNORE_MARKER = "figure-check: ignore"

SUPERSEDED_FILE = "figures-superseded.yaml"


def checked_files(root: Path | None = None) -> list[Path]:
    root = root or repo.ROOT
    skipped = {root / s for s in SKIPPED}
    found: list[Path] = []
    for pattern in CHECKED_GLOBS:
        for path in sorted(root.glob(pattern)):
            if path not in skipped:
                found.append(path)
    return found


def load_superseded(root: Path | None = None) -> list[dict]:
    root = root or repo.ROOT
    path = root / SUPERSEDED_FILE
    if not path.exists():
        return []
    data = repo.load_yaml(path) or {}
    return data.get("superseded") or []


def _pattern(value: str) -> re.Pattern[str]:
    """Match a figure with or without comma grouping, on a word boundary."""
    bare = value.replace(",", "")
    grouped = f"{float(bare):,.1f}".rstrip("0").rstrip(".") if "." in bare else f"{int(bare):,}"
    alternatives = {re.escape(bare), re.escape(grouped), re.escape(value)}
    return re.compile(rf"(?<![\d.]){'|'.join(sorted(alternatives))}(?![\d.])")


def drifted(root: Path | None = None) -> list[str]:
    """Superseded figures found in hand-written prose."""
    root = root or repo.ROOT
    entries = load_superseded(root)
    if not entries:
        return []

    compiled = [
        (entry, _pattern(str(entry["value"])), str(entry.get("unit", "")))
        for entry in entries
    ]

    problems: list[str] = []
    for path in checked_files(root):
        rel = path.relative_to(root)
        for lineno, line in enumerate(path.read_text().splitlines(), start=1):
            if IGNORE_MARKER in line:
                continue
            for entry, pattern, unit in compiled:
                if unit and unit not in line:
                    continue
                if not pattern.search(line):
                    continue
                problems.append(
                    f"{rel}:{lineno}: {entry['value']} {unit} is superseded "
                    f"by {entry['replaced_by']} ({entry['what']}). "
                    f"Update it, or add '{IGNORE_MARKER}' to the line if you "
                    f"are quoting it as history."
                )
    return problems


def main() -> int:
    problems = drifted()
    if not problems:
        count = len(load_superseded())
        print(f"No superseded figures in prose ({count} tracked).")
        return 0
    print("Superseded figures found in hand-written prose:")
    for problem in problems:
        print(f"  - {problem}")
    print(f"\nSee {SUPERSEDED_FILE} for what replaced each one.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
