"""Validate the candidate products and render the generated docs.

    python tools/candidates.py          # validate, then write docs/
    python tools/candidates.py --check  # validate and fail if docs/ is out of date

`make check` runs the second form, so a change to the YAML that was never
regenerated cannot slip past review.

It writes docs/COMPARISON.md, docs/FIT.md, one page per candidate under
docs/products/, and docs/products/README.md as their index. A page left in
docs/products/ for a candidate that no longer exists counts as stale.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # run as a script

from tools import fit, repo  # noqa: E402

ID_RE = re.compile(r"\A[a-z0-9]+(-[a-z0-9]+)*\Z")
DATE_RE = re.compile(r"\A\d{4}-\d{2}-\d{2}\Z")
ROLLUP_STATUSES = ("selected", "ordered", "owned")

#: The spec fields shown in each category's comparison table, in order.
SUMMARY_SPECS = {
    "stroller": ("weight_lb", "folded_in", "max_child_lb"),
    "car-seat": ("weight_lb", "child_weight_lb", "expiry_years", "faa_approved"),
    "bassinet": ("footprint_in", "fits_bed_height_in", "max_child_lb"),
}


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_str_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


#: A Markdown link: [text](target). Every pro, con, summary and notes field
#: must cite its source with one, so a reader can click through to it.
LINK_RE = re.compile(r"\[[^\]]+\]\([^)\s]+\)")


def has_link(text: str) -> bool:
    return bool(LINK_RE.search(str(text)))


def validate(
    items: list[dict], schema: dict, decisions: dict, notes: set[str] | None = None
) -> list[str]:
    """Return a list of human-readable problems. Empty list means valid.

    `notes` is the set of research note filenames that `research_notes` may
    name. None means read them from research/notes/.
    """
    if notes is None:
        notes = repo.list_notes()
    errors: list[str] = []
    seen: dict[str, str] = {}  # id -> the file that first declared it

    known_fields = set(schema["required_fields"]) | set(schema["optional_fields"])
    categories = set(schema["categories"])
    statuses = set(schema["statuses"])

    for item in items:
        source = item.get("_source", "?")
        item_id = item.get("id")
        where = f"{source}: {item_id or '<no id>'}"

        for field in schema["required_fields"]:
            if item.get(field) is None:
                errors.append(f"{where}: missing required field `{field}`")

        for field in item:
            if field != "_source" and field not in known_fields:
                errors.append(f"{where}: unknown field `{field}`")

        if item_id is not None:
            if not ID_RE.match(str(item_id)):
                errors.append(f"{where}: id must be kebab-case")
            if item_id in seen:
                errors.append(f"{where}: duplicate id, already defined in {seen[item_id]}")
            else:
                seen[item_id] = source

        category = item.get("category")
        if category is not None and category not in categories:
            errors.append(f"{where}: unknown category `{category}`")

        status = item.get("status")
        if status is not None and status not in statuses:
            errors.append(f"{where}: unknown status `{status}`")

        price = item.get("price_usd")
        if price is not None and (not _is_number(price) or price < 0):
            errors.append(f"{where}: price_usd must be a non-negative number or null")

        for field in ("pros", "cons"):
            value = item.get(field)
            if value is not None and not _is_str_list(value):
                errors.append(f"{where}: {field} must be a list of text")
            elif value:
                for n, entry in enumerate(value, start=1):
                    if not has_link(entry):
                        errors.append(
                            f"{where}: {field} #{n} cites no source; add a Markdown link "
                            f"to the source or its research note: {entry[:60]!r}"
                        )

        summary = item.get("summary")
        if summary is not None and not (isinstance(summary, str) and summary.strip()):
            errors.append(f"{where}: summary must be text, or be omitted")
        elif summary is not None and not has_link(summary):
            errors.append(f"{where}: summary cites no source; add a Markdown link")

        item_notes = item.get("notes")
        if isinstance(item_notes, str) and item_notes.strip() and not has_link(item_notes):
            errors.append(f"{where}: notes cite no source; add Markdown links")

        errors.extend(validate_research_notes(item, where, notes))
        errors.extend(validate_decision(item, where, decisions))
        errors.extend(validate_specs(item, where, schema))
        errors.extend(validate_safety(item, where, schema))

    errors.extend(validate_compat(items, schema))
    return errors


def validate_research_notes(item: dict, where: str, notes: set[str]) -> list[str]:
    listed = item.get("research_notes")
    if listed is None:
        return []
    if not _is_str_list(listed):
        return [f"{where}: research_notes must be a list of note filenames"]
    errors = []
    for name in listed:
        if "/" in name:
            errors.append(
                f"{where}: research_notes entry `{name}` should be the filename only, "
                "e.g. 2026-11-27-topic.md"
            )
        elif name not in notes:
            errors.append(f"{where}: research_notes names `{name}`, not in research/notes/")
    for name in sorted({n for n in listed if listed.count(n) > 1}):
        errors.append(f"{where}: research_notes lists `{name}` more than once")
    return errors


def validate_decision(item: dict, where: str, decisions: dict) -> list[str]:
    decision = item.get("decision")
    if decision is None:
        return []
    if not isinstance(decision, str) or not re.fullmatch(r"\d{4}", decision):
        return [f"{where}: decision must be a four-digit ADR id in quotes"]
    if decision not in decisions:
        return [f"{where}: decision {decision} has no file in decisions/"]
    adr_status = str(decisions[decision]["front_matter"].get("status", ""))
    if adr_status.startswith("superseded"):
        return [
            f"{where}: decision {decision} is {adr_status}; "
            "point the item at the ADR that replaced it"
        ]
    return []


def _check_kind(kind: str, value) -> str | None:
    """Return a description of what is wrong with `value`, or None if it fits `kind`."""
    if value is None:
        return None
    if kind == "number":
        return None if _is_number(value) and value >= 0 else "a non-negative number"
    if kind == "bool":
        return None if isinstance(value, bool) else "true or false"
    if kind == "str":
        return None if isinstance(value, str) else "text"
    if kind in ("dims2", "dims3", "range"):
        size = 3 if kind == "dims3" else 2
        if not (
            isinstance(value, list)
            and len(value) == size
            and all(_is_number(v) and v >= 0 for v in value)
        ):
            return f"a list of {size} non-negative numbers"
        if kind == "range" and value[0] > value[1]:
            return "[min, max] with min <= max"
        return None
    return f"a known kind (schema says `{kind}`)"


def validate_specs(item: dict, where: str, schema: dict) -> list[str]:
    specs = item.get("specs")
    if specs is None:
        return []
    if not isinstance(specs, dict):
        return [f"{where}: specs must be a mapping or be omitted"]

    allowed = schema["spec_fields"].get(item.get("category"), {})
    errors = []
    for field, value in specs.items():
        if field not in allowed:
            errors.append(f"{where}: unknown spec `{field}` for category {item.get('category')}")
            continue
        problem = _check_kind(allowed[field], value)
        if problem:
            errors.append(f"{where}: specs.{field} must be {problem} or null")
    return errors


def validate_safety(item: dict, where: str, schema: dict) -> list[str]:
    safety = item.get("safety")
    if safety is None:
        return []
    if not isinstance(safety, dict):
        return [f"{where}: safety must be a mapping or be omitted"]

    errors = []
    for field in safety:
        if field not in schema["safety_fields"]:
            errors.append(f"{where}: unknown safety field `{field}`")

    standards = safety.get("standards")
    if standards is not None and not _is_str_list(standards):
        errors.append(f"{where}: safety.standards must be a list of text")

    checked_on = safety.get("checked_on")
    if checked_on is not None and not DATE_RE.match(str(checked_on)):
        errors.append(f"{where}: safety.checked_on must be YYYY-MM-DD")

    recalls = safety.get("recalls")
    if recalls is None:
        return errors
    if not isinstance(recalls, list):
        return [*errors, f"{where}: safety.recalls must be a list"]
    for index, recall in enumerate(recalls):
        label = f"{where}: safety.recalls[{index}]"
        if not isinstance(recall, dict):
            errors.append(f"{label} must be a mapping")
            continue
        if not recall.get("url"):
            errors.append(f"{label} needs a url — a recall claim without a source is a rumor")
        if not DATE_RE.match(str(recall.get("date", ""))):
            errors.append(f"{label} needs a date as YYYY-MM-DD")
    return errors


def validate_compat(items: list[dict], schema: dict) -> list[str]:
    """Compat lives on strollers and may only name car seats in this repo."""
    seats = {item.get("id") for item in items if item.get("category") == "car-seat"}
    allowed = set(schema["compat_fields"])
    errors: list[str] = []

    for item in items:
        compat = item.get("compat")
        if compat is None:
            continue
        where = f"{item.get('_source', '?')}: {item.get('id') or '<no id>'}"
        if item.get("category") != "stroller":
            errors.append(f"{where}: compat only belongs on strollers")
            continue
        if not isinstance(compat, dict):
            errors.append(f"{where}: compat must be a mapping or be omitted")
            continue

        for field in compat:
            if field not in allowed:
                errors.append(f"{where}: unknown compat field `{field}`")

        named: list[str] = []
        for field in ("accepts_car_seats", "incompatible"):
            value = compat.get(field)
            if value is None:
                continue
            if not _is_str_list(value):
                errors.append(f"{where}: compat.{field} must be a list of car-seat ids")
                continue
            named.extend(value)

        adapters = compat.get("needs_adapter")
        if adapters is not None:
            if not isinstance(adapters, dict) or not all(
                isinstance(v, str) and v for v in adapters.values()
            ):
                errors.append(f"{where}: compat.needs_adapter must map car-seat id -> adapter name")
            else:
                named.extend(adapters)

        for seat_id in named:
            if seat_id not in seats:
                errors.append(f"{where}: compat names `{seat_id}`, which is not a car-seat id")
        duplicates = sorted({s for s in named if named.count(s) > 1})
        for seat_id in duplicates:
            errors.append(f"{where}: compat lists `{seat_id}` in more than one place")

    return errors


#: Decision 0001: car seats must be certified to this. Shown as its own column.
SIDE_IMPACT_STANDARD = "FMVSS 213a"


def meets_213a(item: dict) -> bool:
    """True if FMVSS 213a is recorded in the item's safety.standards.

    False means "not recorded", which is not the same as "fails" — the table
    shows it as `?`.
    """
    standards = (item.get("safety") or {}).get("standards") or []
    wanted = SIDE_IMPACT_STANDARD.replace(" ", "").lower()
    return any(str(s).replace(" ", "").lower() == wanted for s in standards)


def _format_spec(value, kind: str = "") -> str:
    if value is None:
        return "?"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        return ("–" if kind == "range" else "×").join(f"{v:g}" for v in value)
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def render_comparison(items: list[dict], schema: dict, decisions: dict) -> str:
    out = [repo.GENERATED_BANNER, "", "# Candidate comparison", ""]

    live = [item for item in items if item.get("status") != "rejected"]
    unpriced = [item for item in live if item.get("price_usd") is None]
    committed = [item for item in items if item.get("status") in ROLLUP_STATUSES]

    out += [
        f"{len(items)} candidates. {len(committed)} are decided "
        f"(selected, ordered or owned); {len(unpriced)} still have no price.",
        "",
        "`?` means not researched yet. See `research/open-questions.md`. "
        "The car seat `213a` column is decision 0001's side-impact requirement.",
        "",
        "Each candidate links to its own page. All pages are listed in "
        "[products/README.md](products/README.md).",
        "",
    ]

    for category in schema["categories"]:
        group = [item for item in items if item.get("category") == category]
        out += [f"## {category}", ""]
        if not group:
            out += ["No candidates yet.", ""]
            continue
        spec_names = SUMMARY_SPECS.get(category, ())
        kinds = schema["spec_fields"].get(category, {})
        side_impact = category == "car-seat"
        header = [
            "Candidate",
            "Status",
            "Price",
            *(["213a"] if side_impact else []),
            *spec_names,
            "Pros",
            "Cons",
            "ADR",
        ]
        out += ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
        for item in sorted(group, key=lambda i: (i.get("status") == "rejected", i["id"])):
            price = item.get("price_usd")
            price_text = "?" if price is None else f"${price:,.2f}"
            specs = item.get("specs") or {}
            adr = item.get("decision")
            if adr and adr in decisions:
                adr_text = f"[{adr}](../decisions/{decisions[adr]['path'].name})"
            else:
                adr_text = "—"
            row = [
                f"[`{item['id']}`](products/{item['id']}.md) — {item['name']}",
                str(item.get("status")),
                price_text,
                *((["yes" if meets_213a(item) else "?"]) if side_impact else []),
                *(_format_spec(specs.get(name), kinds.get(name, "")) for name in spec_names),
                str(len(item.get("pros") or [])),
                str(len(item.get("cons") or [])),
                adr_text,
            ]
            out.append("| " + " | ".join(row) + " |")
        out.append("")

    committed_priced = [item for item in committed if item.get("price_usd") is not None]
    known_total = sum(item["price_usd"] for item in committed_priced)
    committed_unpriced = len(committed) - len(committed_priced)
    out += [
        "## Cost of decided items",
        "",
        f"Known so far: **${known_total:,.2f}** across {len(committed_priced)} priced, "
        "decided items.",
        "",
    ]
    if committed_unpriced:
        out += [f"This is a floor — {committed_unpriced} decided items are still unpriced.", ""]
    return "\n".join(out)


# --- product pages ----------------------------------------------------------
#
# One page per candidate under docs/products/, plus an index. Every line on a
# page comes from the item's YAML, the fit checks, or the ADR files. Nothing
# is written for a field that is absent: no summary means no summary section.

MISUSE_PREFIX = "Misuse risk:"

#: Unit words that may appear inside a spec field name, and how to show them.
UNITS = {"lb": "lb", "in": "in", "years": "years"}

#: Words in spec field names that are acronyms.
ACRONYMS = {"faa": "FAA"}


def _spec_label(field: str) -> tuple[str, str]:
    """Split a spec field name into a readable label and its unit.

    "folded_in" -> ("Folded", "in"); "child_height_in_max" -> ("Child height max", "in").
    """
    parts = field.split("_")
    unit = next((UNITS[p] for p in parts if p in UNITS), "")
    words = [ACRONYMS.get(p, p) for p in parts if p not in UNITS]
    label = " ".join(words)
    return label[:1].upper() + label[1:], unit


def _cell(text) -> str:
    """Make text safe inside a Markdown table cell."""
    return str(text).replace("|", "\\|").replace("\n", " ")


def _product_link(item_id: str, known: set[str]) -> str:
    return f"[`{item_id}`]({item_id}.md)" if item_id in known else f"`{item_id}`"


def _ordered_cons(cons: list[str]) -> list[str]:
    """Misuse-risk cons first, prefix in bold. Other cons keep their order."""
    misuse = [c for c in cons if c.startswith(MISUSE_PREFIX)]
    other = [c for c in cons if not c.startswith(MISUSE_PREFIX)]
    return [f"**{MISUSE_PREFIX}**{c[len(MISUSE_PREFIX) :]}" for c in misuse] + other


def _render_compat(item: dict, items: list[dict], known: set[str]) -> list[str]:
    """Which car seats a stroller takes, or which strollers take a car seat."""
    lines: list[str] = []
    if item.get("category") == "stroller":
        compat = item.get("compat") or {}
        direct = compat.get("accepts_car_seats") or []
        never = compat.get("incompatible") or []
        if direct:
            links = ", ".join(_product_link(s, known) for s in direct)
            lines.append(f"- **Takes directly:** {links}")
        for seat, adapter in (compat.get("needs_adapter") or {}).items():
            lines.append(f"- **Takes with adapter:** {_product_link(seat, known)} ({adapter})")
        if never:
            links = ", ".join(_product_link(s, known) for s in never)
            lines.append(f"- **Confirmed incompatible:** {links}")
        if not lines:
            lines.append("- No car seat compatibility recorded yet.")
    elif item.get("category") == "car-seat":
        for stroller in items:
            if stroller.get("category") != "stroller":
                continue
            compat = stroller.get("compat") or {}
            link = _product_link(stroller["id"], known)
            adapters = compat.get("needs_adapter") or {}
            if item["id"] in (compat.get("accepts_car_seats") or []):
                lines.append(f"- **Clicks onto** {link} directly.")
            elif item["id"] in adapters:
                lines.append(f"- **Clicks onto** {link} with {adapters[item['id']]}.")
            elif item["id"] in (compat.get("incompatible") or []):
                lines.append(f"- **Does not fit** {link}: no adapter exists.")
        if not lines:
            lines.append("- No stroller lists this seat in its compat yet.")
    return [*lines, ""] if lines else []


def render_product(
    item: dict, items: list[dict], schema: dict, decisions: dict, household: dict
) -> str:
    """The Markdown page for one candidate."""
    item_id = item["id"]
    known = {i["id"] for i in items}
    category = item.get("category")
    specs = item.get("specs") or {}
    kinds = schema["spec_fields"].get(category, {})
    safety = item.get("safety") or {}
    unknowns: list[str] = []

    out = [repo.GENERATED_BANNER, "", f"# {item['name']}", ""]

    price = item.get("price_usd")
    out += [
        f"- **Id:** `{item_id}`",
        f"- **Category:** {category}",
        f"- **Status:** {item.get('status')}",
        "- **Price:** " + ("not researched yet" if price is None else f"${price:,.2f}"),
    ]
    if price is None:
        unknowns.append("Price.")
    if item.get("brand"):
        out.append(f"- **Brand:** {item['brand']}")
    if item.get("vendor_url"):
        out.append(f"- **Maker's page:** <{item['vendor_url']}>")
    adr = item.get("decision")
    if adr and adr in decisions:
        title = decisions[adr]["front_matter"].get("title", "")
        label = f"ADR {adr}: {title}" if title else f"ADR {adr}"
        out.append(f"- **Decision:** [{label}](../../decisions/{decisions[adr]['path'].name})")
    else:
        out.append("- **Decision:** none yet")
    out.append("")

    if item.get("summary"):
        out += ["## Summary", "", item["summary"].strip(), ""]

    out += ["## Key specs", ""]
    if kinds:
        out += ["| Spec | Value |", "| --- | --- |"]
        for field, kind in kinds.items():
            label, unit = _spec_label(field)
            value = specs.get(field)
            if value is None:
                text = "?"
                unknowns.append(f"Spec `{field}`.")
            else:
                text = _format_spec(value, kind)
                if unit and not isinstance(value, bool):
                    text = f"{text} {unit}"
            out.append(f"| {_cell(label)} | {_cell(text)} |")
        out += ["", "`?` means not researched yet.", ""]
    else:
        out += ["No spec fields are defined for this category.", ""]

    out += ["## Safety", ""]
    standards = safety.get("standards") or []
    out.append("- **Standards:** " + (", ".join(standards) if standards else "none recorded yet"))
    if not standards:
        unknowns.append("Safety standards.")
    if category == "car-seat":
        side = "recorded" if meets_213a(item) else "not recorded"
        out.append(f"- **{SIDE_IMPACT_STANDARD} (decision 0001):** {side}")
        if not meets_213a(item):
            unknowns.append(f"{SIDE_IMPACT_STANDARD} certification.")
    checked_on = safety.get("checked_on")
    recalls = safety.get("recalls") or []
    out.append(f"- **Recall search last run:** {checked_on or 'never'}")
    if not checked_on:
        unknowns.append("Recall search.")
    if recalls:
        out.append("- **Recalls:**")
        for recall in recalls:
            summary = recall.get("summary") or "no summary recorded"
            out.append(f"  - {recall.get('date')}: {summary} ([source]({recall.get('url')}))")
    elif checked_on:
        out.append(f"- **Recalls:** none found in the search of {checked_on}")
    else:
        out.append("- **Recalls:** not checked yet")
    out.append("")

    pros = item.get("pros") or []
    out += ["## Pros", ""]
    out += [f"- {p}" for p in pros] if pros else ["None recorded yet."]
    out.append("")

    cons = _ordered_cons(item.get("cons") or [])
    out += ["## Cons", ""]
    if cons and cons[0].startswith(f"**{MISUSE_PREFIX}"):
        out += ["Misuse risks come first.", ""]
    out += [f"- {c}" for c in cons] if cons else ["None recorded yet."]
    out.append("")

    out += ["## Fit and compatibility", ""]
    out += _render_compat(item, items, known)
    if item.get("status") == "rejected":
        out += ["Rejected candidates are not fit-checked.", ""]
    else:
        checks = [
            check
            for group in fit.run(items, household).values()
            for check in group
            if item_id in (check.subject, check.against)
        ]
        if checks:
            out += ["| Against | Result | Detail |", "| --- | --- | --- |"]
            for check in checks:
                other = check.against if check.subject == item_id else check.subject
                other_text = _product_link(other, known) if other in known else _cell(other)
                result = f"**{check.outcome}**" if check.outcome == fit.NO_FIT else check.outcome
                out.append(f"| {other_text} | {result} | {_cell(check.detail)} |")
                unknowns += [
                    f"Fit input: {label}."
                    for label in check.missing
                    if not label.startswith(f"{item_id} specs.")  # already listed as a spec
                ]
            out += ["", "[FIT.md](../FIT.md) explains the method.", ""]
        else:
            out += ["No fit checks apply yet.", ""]

    out += ["## Still unknown", ""]
    unique = list(dict.fromkeys(unknowns))
    out += [f"- {u}" for u in unique] if unique else ["Nothing the data can flag."]
    out += ["", "The notes below and `research/open-questions.md` may list more.", ""]

    if item.get("notes"):
        out += ["## Notes", "", str(item["notes"]).strip(), ""]

    out += ["## Research notes", ""]
    research = item.get("research_notes") or []
    if research:
        out += [f"- [{name}](../../research/notes/{name})" for name in research]
    else:
        out.append("None linked yet. List them in `research_notes` in the item's YAML.")
    out.append("")
    return "\n".join(out)


def render_products_index(items: list[dict], schema: dict) -> str:
    """docs/products/README.md: every product page, by category and status."""
    status_order = {s: i for i, s in enumerate(schema["statuses"])}
    out = [repo.GENERATED_BANNER, "", "# Products", ""]
    out += [
        "One page per candidate, generated from `candidates/items/*.yaml`. "
        "Each page summarizes the data and links the research notes behind it. "
        "The side-by-side table is in [COMPARISON.md](../COMPARISON.md).",
        "",
    ]
    for category in schema["categories"]:
        group = [i for i in items if i.get("category") == category]
        out += [f"## {category}", ""]
        if not group:
            out += ["No products yet.", ""]
            continue
        out += ["| Product | Status | Price |", "| --- | --- | --- |"]
        group.sort(key=lambda i: (status_order.get(i.get("status"), len(status_order)), i["id"]))
        for item in group:
            price = item.get("price_usd")
            price_text = "?" if price is None else f"${price:,.2f}"
            out.append(
                f"| [{_cell(item['name'])}]({item['id']}.md) | {item.get('status')} "
                f"| {price_text} |"
            )
        out.append("")
    return "\n".join(out)


def generate() -> dict[Path, str]:
    """The generated files and what they should contain."""
    items = repo.load_candidates()
    schema = repo.load_schema()
    household = repo.load_household()
    decisions = repo.load_decisions()
    files = {
        repo.DOCS_DIR / "COMPARISON.md": render_comparison(items, schema, decisions),
        repo.DOCS_DIR / "FIT.md": fit.render(items, household),
        repo.PRODUCTS_DIR / "README.md": render_products_index(items, schema),
    }
    for item in items:
        page = render_product(item, items, schema, decisions, household)
        files[repo.PRODUCTS_DIR / f"{item['id']}.md"] = page
    return files


def orphan_pages(expected: dict[Path, str]) -> list[Path]:
    """Pages in docs/products/ that no candidate generates any more."""
    return sorted(p for p in repo.PRODUCTS_DIR.glob("*.md") if p not in expected)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate only; fail if the generated docs are out of date",
    )
    args = parser.parse_args(argv)

    items = repo.load_candidates()
    errors = validate(items, repo.load_schema(), repo.load_decisions())
    if errors:
        print(f"Candidate validation failed ({len(errors)} problem(s)):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    expected = generate()
    orphans = orphan_pages(expected)
    if args.check:
        stale = [path for path, content in expected.items() if repo.is_stale(path, content)]
        stale += orphans
        if stale:
            print("Generated docs are out of date:", file=sys.stderr)
            for path in stale:
                print(f"  - {path.relative_to(repo.ROOT)}", file=sys.stderr)
            print("Run `make docs` and commit the result.", file=sys.stderr)
            return 1
        print(f"Candidates valid ({len(items)} items); generated docs are current.")
        return 0

    changed_paths = [
        path for path, content in expected.items() if repo.write_if_changed(path, content)
    ]
    for path in orphans:
        path.unlink()
        print(f"{path.relative_to(repo.ROOT)}: removed (no such candidate)")
    for path in changed_paths:
        print(f"{path.relative_to(repo.ROOT)}: updated")
    print(f"{len(expected) - len(changed_paths)} generated file(s) unchanged.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
