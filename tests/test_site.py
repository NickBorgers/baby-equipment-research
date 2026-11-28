"""The GitHub Pages assembly in tools/site.py: page mapping and link rewriting."""

from __future__ import annotations

from pathlib import Path

from tools import site

PAGES = {
    "guide/index.md": "index.md",
    "docs/products/a.md": "products/a.md",
    "decisions/0004-x.md": "decisions/0004-x.md",
    "categories/car-seat/README.md": "categories/car-seat.md",
}


def test_link_follows_the_page_to_its_new_place():
    assert (
        site.rewrite_link("../docs/products/a.md", "guide/index.md", "index.md", PAGES)
        == "products/a.md"
    )
    assert (
        site.rewrite_link("../../decisions/0004-x.md", "docs/products/a.md", "products/a.md", PAGES)
        == "../decisions/0004-x.md"
    )


def test_fragment_is_kept():
    out = site.rewrite_link("../docs/products/a.md#pros", "guide/index.md", "index.md", PAGES)
    assert out == "products/a.md#pros"


def test_folder_link_means_its_readme():
    out = site.rewrite_link("../categories/car-seat/", "guide/index.md", "index.md", PAGES)
    assert out == "categories/car-seat.md"


def test_repo_file_outside_the_site_links_to_github(tmp_path):
    (tmp_path / "candidates").mkdir()
    (tmp_path / "candidates" / "x.yaml").write_text("")
    out = site.rewrite_link(
        "../candidates/x.yaml", "guide/index.md", "index.md", PAGES, root=tmp_path
    )
    assert out == f"{site.REPO_URL}/blob/main/candidates/x.yaml"


def test_missing_target_is_left_alone_for_strict_build_to_catch(tmp_path):
    assert (
        site.rewrite_link("nope.md", "guide/index.md", "index.md", PAGES, root=tmp_path)
        == "nope.md"
    )


def test_external_and_anchor_links_are_untouched():
    for target in ("https://example.com/a.md", "#top", "mailto:x@example.com"):
        assert site.rewrite_link(target, "guide/index.md", "index.md", PAGES) == target


def test_rewrite_links_keeps_titles():
    text = 'See [A](../docs/products/a.md "title").'
    assert (
        site.rewrite_links(text, "guide/index.md", "index.md", PAGES)
        == 'See [A](products/a.md "title").'
    )


def test_front_matter_becomes_a_box_under_the_title():
    meta, body = site.split_front_matter(
        "---\nstatus: accepted\ndate: 2026-01-01\n---\n\n# T\n\nText\n"
    )
    out = site.insert_after_title(body, site.meta_box(meta, "decisions/0001-x.md"))
    assert out.index("# T") < out.index("**Status:** accepted") < out.index("Text")


def test_every_mapped_source_exists_and_the_template_is_excluded():
    pages = site.page_map()
    assert all((site.ROOT / src).exists() for src in pages)
    assert not any(src.startswith("decisions/0000") for src in pages)
    assert "index.md" not in pages.values(), "the home page is generated, not copied"


def _adr(**meta):
    base = {"id": "0009", "title": "T", "status": "accepted", "date": "2026-01-01"}
    base.update(meta)
    return (Path("decisions/0009-t.md"), base)


def test_accepted_adr_without_reader_fields_fails():
    problems = site.validate_decisions([_adr()])
    assert any("summary" in p for p in problems)
    assert any("if_yours_differs" in p for p in problems)


def test_proposed_adr_may_skip_reader_fields():
    assert site.validate_decisions([_adr(status="proposed")]) == []


def test_complete_adr_passes():
    adr = _adr(summary="We chose X.", if_yours_differs=["If Y, pick Z."])
    assert site.validate_decisions([adr]) == []


def test_every_accepted_adr_in_the_repo_has_reader_fields():
    assert site.validate_decisions(site.load_decisions()) == []


def test_category_status_comes_from_candidates():
    items = [
        {"id": "a", "name": "A", "category": "car-seat", "status": "selected"},
        {"id": "b", "name": "B", "category": "stroller", "status": "candidate"},
        {"id": "c", "name": "C", "category": "stroller", "status": "rejected"},
    ]
    assert site.category_status("car-seat", items) == ("**Decided**", "[A](products/a.md)")
    assert site.category_status("stroller", items)[0] == "Researching (1 candidates)"
    assert site.category_status("bassinet", items)[0] == "Not started"


def test_home_page_shows_each_accepted_decision_with_its_fields():
    items = [{"id": "a", "name": "A", "category": "car-seat", "status": "selected"}]
    adr = _adr(summary="We chose X.", if_yours_differs=["If Y, pick Z."], candidates=["a"])
    old = _adr(id="0008", status="superseded-by-0009", title="Old")
    page = site.home_page([old, adr], items)
    assert "We chose X." in page
    assert "- If Y, pick Z." in page
    assert "[A](products/a.md)" in page
    assert "Replaced decisions" in page and "Old" in page
