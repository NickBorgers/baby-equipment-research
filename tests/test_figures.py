"""Superseded figures must not survive in hand-written prose.

The repo's numbers are computed from the YAML, then copied into the README,
the ADRs, and the category pages. When a price or a measurement changes,
every copy goes quietly wrong.

`figures-superseded.yaml` lists figures that were computed once and no longer
are. These tests fail if one appears in prose unmarked.
"""

from __future__ import annotations

from tools import figures


def test_no_superseded_figures_in_prose():
    problems = figures.drifted()
    assert not problems, "Superseded figures found:\n" + "\n".join(problems)


def test_superseded_list_is_well_formed():
    """Every entry must say what replaced it and why, or it is not useful."""
    for entry in figures.load_superseded():
        for field in ("value", "unit", "replaced_by", "what"):
            assert entry.get(field), f"{entry} is missing '{field}'"


def test_the_checker_actually_catches_something(tmp_path):
    """A checker that never fires is worse than none — it gives false comfort."""
    (tmp_path / "figures-superseded.yaml").write_text(
        "superseded:\n"
        "  - value: '1,234'\n"
        "    unit: W\n"
        "    replaced_by: '5,678 W'\n"
        "    what: a figure invented for this test\n"
    )
    (tmp_path / "README.md").write_text("The load is 1,234 W.\n")

    problems = figures.drifted(root=tmp_path)
    assert len(problems) == 1
    assert "1,234" in problems[0]
    assert "5,678" in problems[0]


def test_the_ignore_marker_works(tmp_path):
    """Quoting a superseded figure as history is legitimate and must be possible."""
    (tmp_path / "figures-superseded.yaml").write_text(
        "superseded:\n"
        "  - value: '1,234'\n"
        "    unit: W\n"
        "    replaced_by: '5,678 W'\n"
        "    what: a figure invented for this test\n"
    )
    (tmp_path / "README.md").write_text(
        f"It was 1,234 W before the change. {figures.IGNORE_MARKER}\n"
    )

    assert figures.drifted(root=tmp_path) == []


def test_logs_are_not_checked(tmp_path):
    """Dated logs keep their figures. Only summaries must stay current.

    research/notes/ and candidates/items/ notes are append-only records of how
    something reached its current state. "As of May it was $499" is correct
    and useful. Rewriting it destroys the reasoning
    trail.
    """
    (tmp_path / "figures-superseded.yaml").write_text(
        "superseded:\n"
        "  - value: '1,234'\n"
        "    unit: W\n"
        "    replaced_by: '5,678 W'\n"
        "    what: a figure invented for this test\n"
    )
    notes = tmp_path / "research" / "notes"
    notes.mkdir(parents=True)
    (notes / "2026-01-01-example.md").write_text("The load is 1,234 W.\n")

    items = tmp_path / "candidates" / "items"
    items.mkdir(parents=True)
    (items / "stroller.yaml").write_text("  notes: as of January, 1,234 W\n")

    assert figures.drifted(root=tmp_path) == []


def test_a_different_unit_does_not_match(tmp_path):
    """1,234 A is not the same claim as 1,234 W."""
    (tmp_path / "figures-superseded.yaml").write_text(
        "superseded:\n"
        "  - value: '1,234'\n"
        "    unit: W\n"
        "    replaced_by: '5,678 W'\n"
        "    what: a figure invented for this test\n"
    )
    (tmp_path / "README.md").write_text("The breaker is 1,234 A.\n")

    assert figures.drifted(root=tmp_path) == []
