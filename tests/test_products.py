"""The product pages, and the `research_notes` and `summary` fields behind them.

These use self-contained fixtures, so they hold whatever is or isn't in
candidates/items/ at the time.
"""

from __future__ import annotations

import pytest

from tools import candidates, repo

NOTE = "2026-01-01-sample.md"


@pytest.fixture(scope="module")
def schema():
    return repo.load_schema()


def _item(**overrides):
    item = {"id": "sample", "name": "Sample", "category": "stroller", "status": "candidate"}
    item.update(overrides)
    return item


def _errors(schema, *items, notes=None):
    return candidates.validate(list(items), schema, {}, notes or set())


def _has(errors, text):
    return any(text in error for error in errors)


def _page(item, *others, schema, decisions=None, household=None):
    items = [item, *others]
    return candidates.render_product(item, items, schema, decisions or {}, household or {})


def _section(text, heading):
    """The body of one `## heading` section."""
    body = text.split(f"## {heading}\n", 1)[1]
    return body.split("\n## ", 1)[0]


# --- the real repo data -----------------------------------------------------


def test_every_research_note_named_by_the_repo_exists():
    notes = repo.list_notes()
    for item in repo.load_candidates():
        for name in item.get("research_notes") or []:
            assert name in notes, f"{item['id']}: {name}"


def test_generate_writes_one_page_per_candidate():
    paths = set(candidates.generate())
    assert repo.PRODUCTS_DIR / "README.md" in paths
    for item in repo.load_candidates():
        assert repo.PRODUCTS_DIR / f"{item['id']}.md" in paths


# --- validation -------------------------------------------------------------


def test_research_notes_that_exist_pass(schema):
    assert _errors(schema, _item(research_notes=[NOTE]), notes={NOTE}) == []


def test_missing_research_note_is_rejected(schema):
    errors = _errors(schema, _item(research_notes=["2026-01-01-nope.md"]), notes={NOTE})
    assert _has(errors, "not in research/notes/")


def test_research_note_with_a_path_is_rejected(schema):
    errors = _errors(schema, _item(research_notes=[f"research/notes/{NOTE}"]), notes={NOTE})
    assert _has(errors, "filename only")


def test_research_notes_must_be_a_list(schema):
    assert _has(_errors(schema, _item(research_notes=NOTE), notes={NOTE}), "must be a list")


def test_research_note_listed_twice_is_rejected(schema):
    errors = _errors(schema, _item(research_notes=[NOTE, NOTE]), notes={NOTE})
    assert _has(errors, "more than once")


def test_validate_reads_real_notes_when_none_are_given(schema):
    real = sorted(repo.list_notes())[0]
    assert candidates.validate([_item(research_notes=[real])], schema, {}) == []


def test_summary_must_be_text(schema):
    assert _has(_errors(schema, _item(summary=["a"])), "summary must be text")
    assert _has(_errors(schema, _item(summary="  ")), "summary must be text")
    assert _errors(schema, _item(summary="Two plain sentences. Like this.")) == []


# --- one product page -------------------------------------------------------


def test_sections_come_in_order(schema):
    seat = _item(
        id="seat-a",
        category="car-seat",
        summary="A sample seat.",
        pros=["light"],
        cons=["pricey"],
        notes="Free text.",
        research_notes=[NOTE],
    )
    text = _page(seat, schema=schema)
    headings = [line[3:] for line in text.splitlines() if line.startswith("## ")]
    assert headings == [
        "Summary",
        "Key specs",
        "Safety",
        "Pros",
        "Cons",
        "Fit and compatibility",
        "Still unknown",
        "Notes",
        "Research notes",
    ]
    assert text.startswith(repo.GENERATED_BANNER)
    assert "\n# Sample\n" in text
    assert "A sample seat." in _section(text, "Summary")


def test_no_summary_means_no_summary_section(schema):
    text = _page(_item(), schema=schema)
    assert "## Summary" not in text
    assert "## Notes" not in text


def test_top_facts(schema):
    decisions = {
        "0002": {
            "path": repo.DECISIONS_DIR / "0002-pick.md",
            "front_matter": {"title": "Pick it", "status": "accepted"},
        }
    }
    item = _item(status="selected", price_usd=499, decision="0002")
    text = _page(item, schema=schema, decisions=decisions)
    assert "- **Status:** selected" in text
    assert "- **Price:** $499.00" in text
    assert "[ADR 0002: Pick it](../../decisions/0002-pick.md)" in text

    unpriced = _page(_item(), schema=schema)
    assert "- **Price:** not researched yet" in unpriced
    assert "- **Decision:** none yet" in unpriced
    assert "- Price." in _section(unpriced, "Still unknown")


def test_specs_carry_units_and_mark_unknowns(schema):
    seat = _item(
        category="car-seat",
        specs={"weight_lb": 9.5, "child_weight_lb": [4, 35], "faa_approved": True},
    )
    text = _page(seat, schema=schema)
    specs = _section(text, "Key specs")
    assert "| Weight | 9.5 lb |" in specs
    assert "| Child weight | 4–35 lb |" in specs
    assert "| Child height max | ? |" in specs
    assert "| FAA approved | yes |" in specs  # a bool gets no unit
    unknown = _section(text, "Still unknown")
    assert "Spec `child_height_in_max`." in unknown
    assert "Spec `weight_lb`." not in unknown


def test_dims_show_as_a_size(schema):
    stroller = _item(specs={"folded_in": [30, 20, 12]})
    assert "| Folded | 30×20×12 in |" in _page(stroller, schema=schema)


def test_safety(schema):
    recall = {"date": "2025-01-02", "url": "https://example.com/r", "summary": "Buckle"}
    seat = _item(
        category="car-seat",
        safety={
            "standards": ["FMVSS 213", "FMVSS 213a"],
            "recalls": [recall],
            "checked_on": "2026-11-27",
        },
    )
    safety = _section(_page(seat, schema=schema), "Safety")
    assert "- **Standards:** FMVSS 213, FMVSS 213a" in safety
    assert "- **FMVSS 213a (decision 0001):** recorded" in safety
    assert "- **Recall search last run:** 2026-11-27" in safety
    assert "  - 2025-01-02: Buckle ([source](https://example.com/r))" in safety

    clean = _item(safety={"recalls": [], "checked_on": "2026-11-27"})
    assert "none found in the search of 2026-11-27" in _page(clean, schema=schema)

    never = _page(_item(category="car-seat"), schema=schema)
    assert "- **Recalls:** not checked yet" in never
    assert "- **FMVSS 213a (decision 0001):** not recorded" in never
    assert "Recall search." in _section(never, "Still unknown")


def test_misuse_risk_cons_come_first(schema):
    item = _item(cons=["Heavy.", "Misuse risk: indicator lies.", "Pricey."])
    cons = _section(_page(item, schema=schema), "Cons")
    lines = [line for line in cons.splitlines() if line.startswith("- ")]
    assert lines == ["- **Misuse risk:** indicator lies.", "- Heavy.", "- Pricey."]
    assert "Misuse risks come first." in cons


def test_no_misuse_note_without_misuse_cons(schema):
    cons = _section(_page(_item(cons=["Heavy."]), schema=schema), "Cons")
    assert "Misuse risks" not in cons


def test_compat_shows_on_both_the_stroller_and_the_seat(schema):
    seat = _item(id="seat-a", category="car-seat")
    other = _item(id="seat-b", category="car-seat")
    stroller = _item(
        id="stroller-a",
        compat={"accepts_car_seats": ["seat-a"], "needs_adapter": {"seat-b": "Adapter X"}},
    )
    on_stroller = _section(_page(stroller, seat, other, schema=schema), "Fit and compatibility")
    assert "- **Takes directly:** [`seat-a`](seat-a.md)" in on_stroller
    assert "- **Takes with adapter:** [`seat-b`](seat-b.md) (Adapter X)" in on_stroller
    assert "| [`seat-a`](seat-a.md) | fits | direct, no adapter |" in on_stroller

    on_seat = _section(_page(seat, stroller, other, schema=schema), "Fit and compatibility")
    assert "- **Clicks onto** [`stroller-a`](stroller-a.md) directly." in on_seat
    on_other = _section(_page(other, stroller, seat, schema=schema), "Fit and compatibility")
    assert "with Adapter X" in on_other


def test_unknown_fit_lists_what_to_research(schema):
    stroller = _item(id="stroller-a", specs={"open_width_in": 24})
    unknown = _section(_page(stroller, schema=schema), "Still unknown")
    assert "Fit input: household home.narrowest_doorway_in." in unknown


def test_rejected_product_is_not_fit_checked(schema):
    text = _page(_item(status="rejected"), schema=schema)
    assert "Rejected candidates are not fit-checked." in text


def test_research_notes_render_as_links(schema):
    text = _page(_item(research_notes=[NOTE]), schema=schema)
    assert f"- [{NOTE}](../../research/notes/{NOTE})" in text
    assert "None linked yet." in _page(_item(), schema=schema)


def test_pipes_in_a_spec_do_not_break_the_table(schema):
    seat = _item(category="car-seat", specs={"aircraft_install": "lap | belt"})
    assert "| Aircraft install | lap \\| belt |" in _page(seat, schema=schema)


# --- the index and the file set ---------------------------------------------


def test_index_groups_by_category_then_status(schema):
    items = [
        _item(id="z-picked", name="Z", status="selected", price_usd=10),
        _item(id="a-maybe", name="A", status="candidate"),
        _item(id="seat-a", name="Seat", category="car-seat"),
    ]
    text = candidates.render_products_index(items, schema)
    stroller = _section(text, "stroller")
    assert stroller.index("a-maybe.md") < stroller.index("z-picked.md")  # lifecycle order
    assert "| [Z](z-picked.md) | selected | $10.00 |" in stroller
    assert "[Seat](seat-a.md)" in _section(text, "car-seat")
    assert "No products yet." in _section(text, "bassinet")


def test_comparison_links_to_the_index(schema):
    text = candidates.render_comparison([], schema, {})
    assert "[products/README.md](products/README.md)" in text


def test_a_page_with_no_candidate_is_an_orphan(tmp_path, monkeypatch):
    monkeypatch.setattr(repo, "PRODUCTS_DIR", tmp_path)
    kept, gone = tmp_path / "kept.md", tmp_path / "gone.md"
    kept.write_text("x")
    gone.write_text("x")
    assert candidates.orphan_pages({kept: "x"}) == [gone]
