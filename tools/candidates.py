"""Validate the candidate products and render the generated docs.

    python tools/candidates.py          # validate, then write docs/
    python tools/candidates.py --check  # validate and fail if docs/ is out of date

`make check` runs the second form, so a change to the YAML that was never
regenerated cannot slip past review.
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
    "car-seat": ("weight_lb", "child_weight_lb", "expiry_years"),
    "bassinet": ("footprint_in", "fits_bed_height_in", "max_child_lb"),
}


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_str_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def validate(items: list[dict], schema: dict, decisions: dict) -> list[str]:
    """Return a list of human-readable problems. Empty list means valid."""
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

        errors.extend(validate_decision(item, where, decisions))
        errors.extend(validate_specs(item, where, schema))
        errors.extend(validate_safety(item, where, schema))

    errors.extend(validate_compat(items, schema))
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
                errors.append(
                    f"{where}: compat.needs_adapter must map car-seat id -> adapter name"
                )
            else:
                named.extend(adapters)

        for seat_id in named:
            if seat_id not in seats:
                errors.append(f"{where}: compat names `{seat_id}`, which is not a car-seat id")
        duplicates = sorted({s for s in named if named.count(s) > 1})
        for seat_id in duplicates:
            errors.append(f"{where}: compat lists `{seat_id}` in more than one place")

    return errors


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
        "`?` means not researched yet. See `research/open-questions.md`.",
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
        header = ["Candidate", "Status", "Price", *spec_names, "Pros", "Cons", "ADR"]
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
                f"`{item['id']}` — {item['name']}",
                str(item.get("status")),
                price_text,
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


def generate() -> dict[Path, str]:
    """The generated files and what they should contain."""
    items = repo.load_candidates()
    schema = repo.load_schema()
    household = repo.load_household()
    return {
        repo.DOCS_DIR / "COMPARISON.md": render_comparison(items, schema, repo.load_decisions()),
        repo.DOCS_DIR / "FIT.md": fit.render(items, household),
    }


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
    if args.check:
        stale = [path for path, content in expected.items() if repo.is_stale(path, content)]
        if stale:
            print("Generated docs are out of date:", file=sys.stderr)
            for path in stale:
                print(f"  - {path.relative_to(repo.ROOT)}", file=sys.stderr)
            print("Run `make docs` and commit the result.", file=sys.stderr)
            return 1
        print(f"Candidates valid ({len(items)} items); generated docs are current.")
        return 0

    for path, content in expected.items():
        changed = repo.write_if_changed(path, content)
        state = "updated" if changed else "unchanged"
        print(f"{path.relative_to(repo.ROOT)}: {state}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
