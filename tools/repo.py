"""Shared loading helpers for the repo's data files.

Everything under tools/ reads the repo through this module, so paths and
parsing live in one place.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

CANDIDATES_DIR = ROOT / "candidates" / "items"
CANDIDATES_SCHEMA = ROOT / "candidates" / "schema.yaml"
DECISIONS_DIR = ROOT / "decisions"
HOUSEHOLD_FILE = ROOT / "household" / "household.yaml"
DOCS_DIR = ROOT / "docs"

GENERATED_BANNER = (
    "<!-- GENERATED FILE — do not edit by hand.\n"
    "     Edit the YAML under candidates/ and household/, then run `make docs`. -->"
)


def load_yaml(path: Path):
    """Parse one YAML file."""
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_schema() -> dict:
    return load_yaml(CANDIDATES_SCHEMA)


def load_household() -> dict:
    return load_yaml(HOUSEHOLD_FILE) or {}


def load_candidates() -> list[dict]:
    """Every candidate product, with the file it came from recorded on each one.

    The `_source` key is added for error messages only. It is not part of the
    schema and is never written back out.
    """
    items: list[dict] = []
    for path in sorted(CANDIDATES_DIR.glob("*.yaml")):
        parsed = load_yaml(path) or []
        if not isinstance(parsed, list):
            raise ValueError(f"{path.name}: expected a list of candidates")
        for item in parsed:
            if not isinstance(item, dict):
                raise ValueError(f"{path.name}: expected each candidate to be a mapping")
            item["_source"] = path.name
            items.append(item)
    return items


def load_decisions() -> dict[str, dict]:
    """ADRs keyed by their four-digit id, with parsed front matter.

    The template (0000) is skipped — it is a form, not a decision.
    """
    decisions: dict[str, dict] = {}
    for path in sorted(DECISIONS_DIR.glob("[0-9][0-9][0-9][0-9]-*.md")):
        adr_id = path.name[:4]
        if adr_id == "0000":
            continue
        decisions[adr_id] = {
            "path": path,
            "front_matter": parse_front_matter(path),
        }
    return decisions


FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_front_matter(path: Path) -> dict:
    """Read the YAML front matter from a Markdown file, or {} if there is none."""
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def write_if_changed(path: Path, content: str) -> bool:
    """Write `content` to `path`. Returns True if the file changed."""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def is_stale(path: Path, content: str) -> bool:
    """True if the file on disk does not match what we would generate."""
    if not path.exists():
        return True
    return path.read_text(encoding="utf-8") != content
