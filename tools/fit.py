"""Compatibility and fit: does this gear work with this car, this house, this bed?

    python tools/fit.py    # print the report without writing anything

Every check has exactly three outcomes:

- **fits** — every input is known, and it fits.
- **does not fit** — every input needed to say so is known, and it does not.
- **insufficient data** — something is still null.

An unknown NEVER passes. A stroller whose folded size is unresearched does not
"probably fit" the trunk. A check that silently treats an unknown as fine is
how a stroller gets bought that does not go in the car.

Inputs come from `specs` and `compat` on the candidates in
`candidates/items/*.yaml`, and from `vehicles` and `home` in
`household/household.yaml`. `rejected` candidates and `future_vehicles` are
skipped.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # run as a script

from tools import repo  # noqa: E402

FITS = "fits"
NO_FIT = "does not fit"
UNKNOWN = "insufficient data"


@dataclass
class Check:
    """One fit question and its answer."""

    subject: str              # the candidate id
    against: str              # what it was checked against
    outcome: str              # FITS | NO_FIT | UNKNOWN
    detail: str = ""
    missing: list[str] = field(default_factory=list)  # what to research to get an answer


# --- the primitives ---------------------------------------------------------


def fits_within(item_dims, space_dims) -> str:
    """Does a box of `item_dims` fit inside a space of `space_dims`?

    Both are lists of the same length, in any order. Each is sorted largest
    first and compared side by side, so [10, 20, 30] fits in [31, 11, 21].
    Allowing rotation like this is generous — a real trunk has a sloped hatch
    and wheel wells — so a "fits" here is a screen, not a guarantee.
    """
    if item_dims is None or space_dims is None:
        return UNKNOWN
    if any(v is None for v in [*item_dims, *space_dims]):
        return UNKNOWN
    if len(item_dims) != len(space_dims):
        raise ValueError(f"cannot compare {len(item_dims)}-D with {len(space_dims)}-D")
    pairs = zip(sorted(item_dims, reverse=True), sorted(space_dims, reverse=True), strict=True)
    return FITS if all(a <= b for a, b in pairs) else NO_FIT


def at_most(value, limit) -> str:
    """Is `value` no larger than `limit`? Unknown on either side is UNKNOWN."""
    if value is None or limit is None:
        return UNKNOWN
    return FITS if value <= limit else NO_FIT


def within_range(value, bounds) -> str:
    """Is `value` inside the [min, max] `bounds`? Unknown on either side is UNKNOWN."""
    if value is None or bounds is None or any(b is None for b in bounds):
        return UNKNOWN
    low, high = bounds
    return FITS if low <= value <= high else NO_FIT


def _missing(pairs: list[tuple[str, object]]) -> list[str]:
    return [label for label, value in pairs if value is None]


def _specs(item: dict) -> dict:
    return item.get("specs") or {}


# --- the checks -------------------------------------------------------------


def travel_system(stroller: dict, seat: dict) -> Check:
    """Does this infant car seat click onto this stroller?"""
    compat = stroller.get("compat") or {}
    seat_id = seat["id"]
    against = seat_id
    if seat_id in (compat.get("accepts_car_seats") or []):
        return Check(stroller["id"], against, FITS, "direct, no adapter")
    adapters = compat.get("needs_adapter") or {}
    if seat_id in adapters:
        return Check(stroller["id"], against, FITS, f"with adapter: {adapters[seat_id]}")
    if seat_id in (compat.get("incompatible") or []):
        return Check(stroller["id"], against, NO_FIT, "no adapter exists")
    return Check(
        stroller["id"],
        against,
        UNKNOWN,
        "not listed in the stroller's compat",
        [f"{stroller['id']} compat for {seat_id}"],
    )


def trunk(stroller: dict, vehicle: dict) -> Check:
    folded = _specs(stroller).get("folded_in")
    space = vehicle.get("trunk_in")
    name = vehicle.get("name", "vehicle")
    return Check(
        stroller["id"],
        f"{name} trunk",
        fits_within(folded, space),
        "folded size vs. trunk, rotation allowed",
        _missing([
            (f"{stroller['id']} specs.folded_in", folded),
            (f"household vehicle '{name}' trunk_in", space),
        ]),
    )


def doorway(stroller: dict, home: dict) -> Check:
    width = _specs(stroller).get("open_width_in")
    door = home.get("narrowest_doorway_in")
    return Check(
        stroller["id"],
        "narrowest doorway",
        at_most(width, door),
        "open width vs. door width",
        _missing([
            (f"{stroller['id']} specs.open_width_in", width),
            ("household home.narrowest_doorway_in", door),
        ]),
    )


def storage(stroller: dict, home: dict) -> Check:
    folded = _specs(stroller).get("folded_in")
    space = home.get("stroller_storage_in")
    return Check(
        stroller["id"],
        "stroller storage spot",
        fits_within(folded, space),
        "folded size vs. storage space",
        _missing([
            (f"{stroller['id']} specs.folded_in", folded),
            ("household home.stroller_storage_in", space),
        ]),
    )


def overhead_bin(stroller: dict, travel: dict) -> Check:
    folded = _specs(stroller).get("folded_in")
    space = travel.get("overhead_bin_in")
    return Check(
        stroller["id"],
        "airline overhead bin",
        fits_within(folded, space),
        "folded size vs. strictest bin limit; gate check is the fallback",
        _missing([
            (f"{stroller['id']} specs.folded_in", folded),
            ("household travel.overhead_bin_in", space),
        ]),
    )


def bassinet_floor(bassinet: dict, home: dict) -> Check:
    footprint = _specs(bassinet).get("footprint_in")
    space = home.get("bedside_space_in")
    return Check(
        bassinet["id"],
        "bedside floor space",
        fits_within(footprint, space),
        "footprint vs. floor space",
        _missing([
            (f"{bassinet['id']} specs.footprint_in", footprint),
            ("household home.bedside_space_in", space),
        ]),
    )


def bassinet_bed_height(bassinet: dict, home: dict) -> Check | None:
    """For bedside models only: does the maker's bed-height range cover our bed?

    Returns None for a bassinet known NOT to attach bedside — the question
    does not apply. An unknown `bedside_attach` still asks it, as UNKNOWN.
    """
    specs = _specs(bassinet)
    attach = specs.get("bedside_attach")
    if attach is False:
        return None
    bounds = specs.get("fits_bed_height_in")
    bed = home.get("bed_top_height_in")
    missing = _missing([
        (f"{bassinet['id']} specs.bedside_attach", attach),
        (f"{bassinet['id']} specs.fits_bed_height_in", bounds),
        ("household home.bed_top_height_in", bed),
    ])
    outcome = UNKNOWN if attach is None else within_range(bed, bounds)
    return Check(bassinet["id"], "adult bed height", outcome, "bed height vs. maker's range",
                 missing)


def car_seat_width(seat: dict, vehicle: dict) -> Check:
    width = _specs(seat).get("base_width_in")
    space = vehicle.get("rear_seat_width_in")
    name = vehicle.get("name", "vehicle")
    return Check(
        seat["id"],
        f"{name} rear seat",
        at_most(width, space),
        "rough screen only — the vehicle and seat manuals decide",
        _missing([
            (f"{seat['id']} specs.base_width_in", width),
            (f"household vehicle '{name}' rear_seat_width_in", space),
        ]),
    )


# --- running everything -----------------------------------------------------


def _live(items: list[dict], category: str) -> list[dict]:
    return [
        item
        for item in items
        if item.get("category") == category and item.get("status") != "rejected"
    ]


def run(items: list[dict], household: dict) -> dict[str, list[Check]]:
    """Every check, grouped by section. Sections with nothing to check are empty."""
    strollers = _live(items, "stroller")
    seats = _live(items, "car-seat")
    bassinets = _live(items, "bassinet")
    vehicles = household.get("vehicles") or []
    home = household.get("home") or {}
    travel = household.get("travel") or {}
    flies = travel.get("flies") is not False  # unknown still asks the question

    bed_checks = [bassinet_bed_height(b, home) for b in bassinets]
    return {
        "Travel system (car seat on stroller)": [
            travel_system(s, c) for s in strollers for c in seats
        ],
        "Stroller in the trunk": [trunk(s, v) for s in strollers for v in vehicles],
        "Stroller through the door": [doorway(s, home) for s in strollers],
        "Stroller in its storage spot": [storage(s, home) for s in strollers],
        "Stroller in an overhead bin": [overhead_bin(s, travel) for s in strollers]
        if flies
        else [],
        "Car seat in the back seat": [car_seat_width(c, v) for c in seats for v in vehicles],
        "Bassinet beside the bed": [bassinet_floor(b, home) for b in bassinets]
        + [check for check in bed_checks if check is not None],
    }


def render(items: list[dict], household: dict) -> str:
    results = run(items, household)
    every = [check for checks in results.values() for check in checks]
    counts = {outcome: sum(c.outcome == outcome for c in every) for outcome in (FITS, NO_FIT,
                                                                                 UNKNOWN)}

    out = [repo.GENERATED_BANNER, "", "# Compatibility and fit", ""]
    out += [
        f"{len(every)} checks: {counts[FITS]} fit, {counts[NO_FIT]} do not fit, "
        f"{counts[UNKNOWN]} have insufficient data.",
        "",
        "An unknown never counts as a fit. See `tools/fit.py` for the method and the "
        "`fit-check` skill for how to read this.",
        "",
    ]
    if not (household.get("vehicles") or []):
        out += ["No vehicles in `household/household.yaml` yet, so no trunk or "
                "back-seat checks run.", ""]

    for section, checks in results.items():
        out += [f"## {section}", ""]
        if not checks:
            out += ["Nothing to check yet.", ""]
            continue
        out += ["| Candidate | Against | Result | Detail |", "| --- | --- | --- | --- |"]
        for check in checks:
            result = f"**{check.outcome}**" if check.outcome == NO_FIT else check.outcome
            out.append(f"| `{check.subject}` | {check.against} | {result} | {check.detail} |")
        out.append("")

    blockers = sorted({label for check in every for label in check.missing})
    out += ["## What blocks a real answer", ""]
    if not every:
        out += ["No checks ran yet — there are no candidates to check."]
    elif blockers:
        out += [f"- {label}" for label in blockers]
    else:
        out += ["Nothing — every check that runs has its inputs."]
    out.append("")
    return "\n".join(out)


def main() -> int:
    print(render(repo.load_candidates(), repo.load_household()))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
