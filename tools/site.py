"""Assemble the GitHub Pages site from the repo's Markdown.

The repo keeps its Markdown where the work happens: decisions in
`decisions/`, notes in `research/notes/`, and generated pages in `docs/`.
This script copies those files into one tree, `build/site-src/`, and writes
`build/mkdocs.yml`. MkDocs then turns that tree into HTML in `build/site/`.

Nothing here is hand-edited, and nothing here is committed. `build/` is
rebuilt from scratch on every run. GitHub Actions runs it on every push to
main (`.github/workflows/pages.yml`). No page on the site is written by hand,
so the site cannot drift from the repo.

THE HOME PAGE is generated from two sources:

- the candidates' statuses, for "where we are" in each category, and
- each accepted ADR's `summary` and `if_yours_differs` front matter, for
  "our decisions". The build fails if an accepted ADR lacks either field.

WHAT THE COPY CHANGES, AND WHY.

- **Links.** A page moves when it is copied (`docs/products/x.md` becomes
  `products/x.md`). Each relative
  link is resolved against the page's place in the repo, then rewritten to
  point at the target's place in the site. A link to a repo file that is
  not part of the site (a YAML file, AGENTS.md) becomes a link to that file
  on GitHub. A link to nothing is left alone, so `mkdocs build --strict`
  fails on it.
- **Front matter.** ADRs and research notes start with YAML front matter.
  MkDocs would hide it. The copy turns the useful fields (status, date,
  confidence, the question, an ADR's summary and the products it compared)
  into boxes under the page title instead.
- **Index pages.** The decisions and the research notes get a generated
  index page each, because neither folder has one in the repo.

Run `make site` to build, or `make serve` to preview at localhost:8000.
"""

from __future__ import annotations

import posixpath
import re
import shutil
import sys
from pathlib import Path

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import repo  # noqa: E402

ROOT = repo.ROOT
BUILD_DIR = ROOT / "build"
SITE_SRC = BUILD_DIR / "site-src"
CONFIG_FILE = BUILD_DIR / "mkdocs.yml"

REPO_URL = "https://github.com/NickBorgers/baby-equipment-research"
SITE_URL = "https://nickborgers.github.io/baby-equipment-research/"

CATEGORIES = ("car-seat", "stroller", "bassinet")
CATEGORY_NAMES = {"car-seat": "Car seat", "stroller": "Stroller", "bassinet": "Bassinet"}
DECIDED_STATUSES = ("selected", "ordered", "owned")

LINK_RE = re.compile(r"(\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
H1_RE = re.compile(r"^# (.+)$", re.MULTILINE)


# --------------------------------------------------------------------------
# Which repo file goes where in the site
# --------------------------------------------------------------------------


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def decision_files() -> list[Path]:
    """Accepted and superseded ADRs. The template is not a decision."""
    return sorted(
        p
        for p in repo.DECISIONS_DIR.glob("[0-9][0-9][0-9][0-9]-*.md")
        if not p.name.startswith("0000")
    )


def note_files() -> list[Path]:
    return sorted(repo.NOTES_DIR.glob("*.md"))


def product_files() -> list[Path]:
    return sorted(p for p in repo.PRODUCTS_DIR.glob("*.md") if p.name != "README.md")


def page_map() -> dict[str, str]:
    """Map each repo path (posix, relative to ROOT) to its path in the site."""
    pages: dict[str, str] = {}
    pages["docs/COMPARISON.md"] = "compare/comparison.md"
    pages["docs/FIT.md"] = "compare/fit.md"
    pages["docs/products/README.md"] = "products/index.md"
    for path in product_files():
        pages[_rel(path)] = f"products/{path.name}"
    for path in decision_files():
        pages[_rel(path)] = f"decisions/{path.name}"
    pages["research/open-questions.md"] = "research/open-questions.md"
    for path in note_files():
        pages[_rel(path)] = f"research/notes/{path.name}"
    for category in CATEGORIES:
        pages[f"categories/{category}/README.md"] = f"categories/{category}.md"
    return pages


# --------------------------------------------------------------------------
# Rewriting one page
# --------------------------------------------------------------------------


def rewrite_link(target: str, src: str, dest: str, pages: dict[str, str], root: Path = ROOT) -> str:
    """Return `target`, a link written in repo file `src`, as seen from site page `dest`."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE) or target.startswith(("#", "/")):
        return target
    path, _, fragment = target.partition("#")
    suffix = f"#{fragment}" if fragment else ""
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(src), path))

    # A link to a folder means its README.
    candidates = [resolved, posixpath.join(resolved, "README.md")]
    for candidate in candidates:
        if candidate in pages:
            relative = posixpath.relpath(pages[candidate], posixpath.dirname(dest) or ".")
            return relative + suffix

    on_disk = root / resolved
    if resolved != ".." and not resolved.startswith("../") and on_disk.exists():
        kind = "tree" if on_disk.is_dir() else "blob"
        return f"{REPO_URL}/{kind}/main/{resolved}{suffix}"
    return target


def rewrite_links(text: str, src: str, dest: str, pages: dict[str, str], root: Path = ROOT) -> str:
    def replace(match: re.Match) -> str:
        return (
            match.group(1) + rewrite_link(match.group(2), src, dest, pages, root) + match.group(3)
        )

    return LINK_RE.sub(replace, text)


def split_front_matter(text: str) -> tuple[dict, str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    return meta, text[match.end() :]


def _indent(text: str) -> str:
    """Indent a block so it sits inside an admonition."""
    return "\n".join(("    " + line) if line else "" for line in text.splitlines())


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {' '.join(str(item).split())}" for item in items)


def products_table(ids: list[str], products: dict[str, dict], link_prefix: str) -> str:
    """A table of the candidates an ADR compared, from their YAML. Empty if none."""
    rows = []
    for item_id in ids:
        item = products.get(item_id)
        if not item:
            rows.append(f"| `{item_id}` | ? | ? |")
            continue
        price = item.get("price_usd")
        price_text = f"${price:,.2f}" if isinstance(price, int | float) else "?"
        link = f"[{item['name']}]({link_prefix}{item_id}.md)"
        rows.append(f"| {link} | {item.get('status', '?')} | {price_text} |")
    if not rows:
        return ""
    return "| Product | Status | Price |\n| --- | --- | --- |\n" + "\n".join(rows)


def decision_boxes(meta: dict, products: dict[str, dict], link_prefix: str) -> str:
    """The summary, "if yours differs" and products blocks for one ADR."""
    blocks = []
    if meta.get("summary"):
        blocks.append('!!! abstract "In short"\n' + _indent(" ".join(meta["summary"].split())))
    if meta.get("if_yours_differs"):
        blocks.append(
            '!!! tip "If your situation differs"\n' + _indent(_bullets(meta["if_yours_differs"]))
        )
    table = products_table(meta.get("candidates") or [], products, link_prefix)
    if table:
        blocks.append("**Products compared:**\n\n" + table)
    return "\n\n".join(blocks)


def meta_box(meta: dict, src: str, products: dict[str, dict] | None = None) -> str:
    """Boxes for an ADR's or a note's front matter. Empty if none."""
    if src.startswith("decisions/"):
        status = meta.get("status", "?")
        parts = [
            f"**Status:** {status}",
            f"**Date:** {meta.get('date', '?')}",
            f"**Category:** {meta.get('category', '?')}",
        ]
        kind = "warning" if str(status).startswith("superseded") else "info"
        record = f'!!! {kind} "Decision record"\n    ' + " · ".join(parts)
        extra = decision_boxes(meta, products or {}, "../products/")
        return record + ("\n\n" + extra if extra else "") + "\n"
    if src.startswith("research/notes/"):
        lines = []
        if meta.get("question"):
            lines.append(f"**Question:** {meta['question']}")
        date, confidence = meta.get("date", "?"), meta.get("confidence", "?")
        lines.append(f"**Researched:** {date} · **Confidence:** {confidence}")
        body = "\n\n".join(lines).replace("\n", "\n    ")
        return '!!! note "Research note"\n    ' + body + "\n"
    return ""


def insert_after_title(body: str, block: str) -> str:
    if not block:
        return body
    match = H1_RE.search(body)
    if not match:
        return block + "\n" + body
    return body[: match.end()] + "\n\n" + block + body[match.end() :]


def title_of(text: str, fallback: str) -> str:
    match = H1_RE.search(text)
    return match.group(1).strip() if match else fallback


def render_page(
    src: str,
    dest: str,
    pages: dict[str, str],
    root: Path = ROOT,
    products: dict[str, dict] | None = None,
) -> str:
    text = (root / src).read_text(encoding="utf-8")
    meta, body = split_front_matter(text)
    body = insert_after_title(body, meta_box(meta, src, products))
    body = rewrite_links(body, src, dest, pages, root)
    edit = f"{REPO_URL}/blob/main/{src}"
    return body.rstrip() + f"\n\n---\n\n<small>Source: [`{src}`]({edit})</small>\n"


# --------------------------------------------------------------------------
# Generated index pages
# --------------------------------------------------------------------------


def decisions_index() -> str:
    rows = []
    for path in decision_files():
        meta, body = split_front_matter(path.read_text(encoding="utf-8"))
        title = meta.get("title") or title_of(body, path.stem)
        adr_id = meta.get("id", path.stem[:4])
        status, date = meta.get("status", "?"), meta.get("date", "?")
        rows.append(f"| [{adr_id}]({path.name}) | {title} | {status} | {date} |")
    return (
        "# Decisions\n\n"
        "Each choice that shapes what we buy has a decision record (an ADR). "
        "A record states the context, the decision, the reasons and the alternatives we rejected. "
        "We never rewrite an accepted record. "
        "A changed decision gets a new record that supersedes the old one.\n\n"
        "| ADR | Decision | Status | Date |\n| --- | --- | --- | --- |\n" + "\n".join(rows) + "\n"
    )


def notes_index() -> str:
    by_category: dict[str, list[str]] = {}
    for path in note_files():
        meta, body = split_front_matter(path.read_text(encoding="utf-8"))
        category = str(meta.get("category", "general"))
        title = title_of(body, path.stem)
        row = (
            f"| {meta.get('date', '?')} | [{title}]({path.name}) | {meta.get('confidence', '?')} |"
        )
        by_category.setdefault(category, []).append(row)
    sections = []
    for category in sorted(by_category):
        sections.append(
            f"## {category}\n\n| Date | Note | Confidence |\n| --- | --- | --- |\n"
            + "\n".join(by_category[category])
        )
    return (
        "# Research notes\n\n"
        "One note answers one question. Each note lists its sources with the date we read them, "
        "says how much we trust each one, and states what is still unknown.\n\n"
        + "\n\n".join(sections)
        + "\n"
    )


HOME_INTRO = """# Our baby gear research

We are choosing a car seat, a stroller and a bassinet for our first baby.
This site shows what we decided, why, and the evidence behind each choice.

Your situation may differ from ours. So each decision below also says when
another choice would suit another family better.
"""

HOME_EVIDENCE = (
    """## How we treat evidence

- **Every fact has a source we read.** Each research note lists its sources,
  the date we read them, and how far we trust each one.
- **Safety claims need a primary source:** NHTSA, CPSC, the standard itself,
  or the maker's manual. A review or a store listing is not enough.
- **Reviews are medium confidence at best.** Owner reviews are low unless
  several agree.
- **Model years matter.** We say which version a review tested.
- **Unknown stays unknown.** A `?` means "not researched yet", never "fine".

We are parents doing research, not child passenger safety technicians.
Read your seat's manual, and have a technician check your install.

This site is generated from
[the research repo]("""
    + REPO_URL
    + """) on every change.
"""
)


def category_status(category: str, items: list[dict]) -> tuple[str, str]:
    """Return (status, our pick) for one category, from the candidates' statuses."""
    in_category = [i for i in items if i.get("category") == category]
    decided = [i for i in in_category if i.get("status") in DECIDED_STATUSES]
    if decided:
        picks = ", ".join(f"[{i['name']}](products/{i['id']}.md)" for i in decided)
        return "**Decided**", picks
    open_items = [i for i in in_category if i.get("status") != "rejected"]
    if open_items:
        return f"Researching ({len(open_items)} candidates)", "—"
    return "Not started", "—"


def home_page(decisions: list[tuple[Path, dict]], items: list[dict]) -> str:
    products = {i["id"]: i for i in items}
    rows = []
    for category in CATEGORIES:
        status, pick = category_status(category, items)
        rows.append(f"| {CATEGORY_NAMES[category]} | {status} | {pick} |")
    where = (
        "## Where we are\n\n| Category | Status | Our pick |\n| --- | --- | --- |\n"
        + "\n".join(rows)
        + "\n\nAll candidates side by side: [comparison](compare/comparison.md).\n"
    )

    accepted, replaced = [], []
    for path, meta in decisions:
        title = meta.get("title") or path.stem
        link = f"decisions/{path.name}"
        status = str(meta.get("status", ""))
        if status == "accepted":
            section = [
                f"### {meta.get('id')}: [{title}]({link})",
                f"Decided {meta.get('date', '?')}.",
                decision_boxes(meta, products, "products/"),
            ]
            accepted.append("\n\n".join(s for s in section if s))
        elif status.startswith("superseded"):
            replaced.append(f"- [{meta.get('id')}: {title}]({link}) — {status}")

    parts = [
        HOME_INTRO,
        where,
        "## Our decisions, in order\n\n"
        "Each decision builds on the ones before it. "
        "Open one for its full reasons and the alternatives we rejected.",
        "\n\n".join(accepted) or "No decisions yet.",
    ]
    if replaced:
        parts.append("## Replaced decisions\n\n" + "\n".join(replaced))
    parts.append(HOME_EVIDENCE)
    return "\n\n".join(p.strip() for p in parts) + "\n"


def validate_decisions(decisions: list[tuple[Path, dict]]) -> list[str]:
    """Each accepted ADR needs the two fields the home page shows."""
    problems = []
    for path, meta in decisions:
        if meta.get("status") != "accepted":
            continue
        where = f"decisions/{path.name}"
        summary = meta.get("summary")
        if not isinstance(summary, str) or not summary.strip():
            problems.append(f"{where}: accepted ADR needs a `summary` in its front matter")
        differs = meta.get("if_yours_differs")
        if (
            not isinstance(differs, list)
            or not differs
            or not all(isinstance(d, str) and d.strip() for d in differs)
        ):
            problems.append(
                f"{where}: accepted ADR needs `if_yours_differs`, a list of one or more strings"
            )
    return problems


def load_decisions() -> list[tuple[Path, dict]]:
    return [(path, repo.parse_front_matter(path)) for path in decision_files()]


# --------------------------------------------------------------------------
# Navigation and config
# --------------------------------------------------------------------------


def nav(pages: dict[str, str]) -> list:
    def titled(srcs: list[str]) -> list[dict]:
        return [
            {title_of(split_front_matter((ROOT / s).read_text(encoding="utf-8"))[1], s): pages[s]}
            for s in srcs
        ]

    products = ["products/index.md"] + titled([_rel(p) for p in product_files()])
    decisions = ["decisions/index.md"] + titled([_rel(p) for p in decision_files()])
    research = [
        {"Open questions": "research/open-questions.md"},
        {"What to judge, by category": titled([f"categories/{c}/README.md" for c in CATEGORIES])},
        {"Notes": ["research/notes/index.md"] + titled([_rel(p) for p in note_files()])},
    ]
    return [
        {"Home": "index.md"},
        {"Decisions": decisions},
        {
            "Compare": [
                {"Side by side": "compare/comparison.md"},
                {"Fit and compatibility": "compare/fit.md"},
            ]
        },
        {"Products": products},
        {"Research": research},
    ]


def config(pages: dict[str, str]) -> dict:
    return {
        "site_name": "Our baby gear research",
        "site_url": SITE_URL,
        "site_description": (
            "How we chose baby gear: what mattered, what we picked, and the evidence behind it."
        ),
        "repo_url": REPO_URL,
        "edit_uri": "",
        "docs_dir": "site-src",
        "site_dir": "site",
        "strict": True,
        "validation": {
            "links": {"not_found": "warn", "anchors": "warn", "unrecognized_links": "warn"}
        },
        "theme": {
            "name": "material",
            "features": [
                "navigation.tabs",
                "navigation.sections",
                "navigation.indexes",
                "navigation.top",
                "search.highlight",
                "content.tooltips",
            ],
            "palette": [
                {
                    "media": "(prefers-color-scheme: light)",
                    "scheme": "default",
                    "primary": "teal",
                    "toggle": {"icon": "material/weather-night", "name": "Dark mode"},
                },
                {
                    "media": "(prefers-color-scheme: dark)",
                    "scheme": "slate",
                    "primary": "teal",
                    "toggle": {"icon": "material/weather-sunny", "name": "Light mode"},
                },
            ],
        },
        "plugins": ["search"],
        "markdown_extensions": [
            "admonition",
            "attr_list",
            "tables",
            "pymdownx.details",
            "pymdownx.superfences",
            {"toc": {"permalink": True}},
            # The repo nests lists with 2 spaces, as GitHub does. Plain
            # Python-Markdown needs 4.
            {"mdx_truly_sane_lists": {"nested_indent": 2}},
        ],
        "nav": nav(pages),
    }


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------


def build() -> list[str]:
    """Write build/site-src/ and build/mkdocs.yml. Return the problems found."""
    pages = page_map()
    missing = [src for src in pages if not (ROOT / src).exists()]
    if missing:
        return [f"missing source file: {src}" for src in missing]
    decisions = load_decisions()
    problems = validate_decisions(decisions)
    if problems:
        return problems
    items = repo.load_candidates()
    products = {i["id"]: i for i in items}

    if SITE_SRC.exists():
        shutil.rmtree(SITE_SRC)
    for src, dest in pages.items():
        out = SITE_SRC / dest
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_page(src, dest, pages, products=products), encoding="utf-8")
    (SITE_SRC / "index.md").write_text(home_page(decisions, items), encoding="utf-8")
    (SITE_SRC / "decisions" / "index.md").write_text(decisions_index(), encoding="utf-8")
    (SITE_SRC / "research" / "notes" / "index.md").write_text(notes_index(), encoding="utf-8")

    CONFIG_FILE.write_text(
        "# GENERATED by tools/site.py — do not edit. Run `make site`.\n"
        + yaml.safe_dump(config(pages), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return []


def main() -> int:
    problems = build()
    for problem in problems:
        print(problem, file=sys.stderr)
    if not problems:
        print(f"wrote {SITE_SRC.relative_to(ROOT)}/ and {CONFIG_FILE.relative_to(ROOT)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
