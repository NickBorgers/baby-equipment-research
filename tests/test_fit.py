"""The fit math, and above all its refusal to guess.

A stroller with an unresearched folded size silently treated as "fits" is how
a stroller gets bought that does not go in the car. Most of these tests exist
to prove that does not happen.
"""

from __future__ import annotations

import pytest

from tools import fit


def stroller(**specs):
    compat = specs.pop("compat", None)
    item = {"id": "s", "name": "S", "category": "stroller", "status": "candidate", "specs": specs}
    if compat is not None:
        item["compat"] = compat
    return item


def seat(seat_id="c", **specs):
    return {"id": seat_id, "name": "C", "category": "car-seat", "status": "candidate",
            "specs": specs}


def bassinet(**specs):
    return {"id": "b", "name": "B", "category": "bassinet", "status": "candidate", "specs": specs}


# --- primitives -------------------------------------------------------------


def test_fits_within_allows_rotation():
    assert fit.fits_within([10, 20, 30], [31, 11, 21]) == fit.FITS


def test_fits_within_rejects_too_big():
    assert fit.fits_within([10, 20, 32], [31, 11, 21]) == fit.NO_FIT


def test_fits_within_exact_size_fits():
    assert fit.fits_within([10, 20], [20, 10]) == fit.FITS


@pytest.mark.parametrize(
    "item, space",
    [(None, [1, 2, 3]), ([1, 2, 3], None), ([1, None, 3], [9, 9, 9]), ([1, 2, 3], [9, 9, None])],
)
def test_fits_within_unknown_is_never_a_fit(item, space):
    assert fit.fits_within(item, space) == fit.UNKNOWN


def test_fits_within_refuses_mismatched_dimensions():
    with pytest.raises(ValueError):
        fit.fits_within([1, 2], [1, 2, 3])


def test_at_most():
    assert fit.at_most(24, 30) == fit.FITS
    assert fit.at_most(31, 30) == fit.NO_FIT
    assert fit.at_most(None, 30) == fit.UNKNOWN
    assert fit.at_most(24, None) == fit.UNKNOWN


def test_within_range():
    assert fit.within_range(25, [20, 30]) == fit.FITS
    assert fit.within_range(31, [20, 30]) == fit.NO_FIT
    assert fit.within_range(None, [20, 30]) == fit.UNKNOWN
    assert fit.within_range(25, None) == fit.UNKNOWN
    assert fit.within_range(25, [20, None]) == fit.UNKNOWN


# --- travel system ----------------------------------------------------------


def test_travel_system_direct():
    check = fit.travel_system(stroller(compat={"accepts_car_seats": ["c"]}), seat())
    assert check.outcome == fit.FITS
    assert "no adapter" in check.detail


def test_travel_system_with_adapter_names_it():
    check = fit.travel_system(stroller(compat={"needs_adapter": {"c": "Adapter X"}}), seat())
    assert check.outcome == fit.FITS
    assert "Adapter X" in check.detail


def test_travel_system_incompatible():
    check = fit.travel_system(stroller(compat={"incompatible": ["c"]}), seat())
    assert check.outcome == fit.NO_FIT


def test_travel_system_unlisted_is_unknown_not_incompatible():
    check = fit.travel_system(stroller(), seat())
    assert check.outcome == fit.UNKNOWN
    assert check.missing == ["s compat for c"]


# --- the other checks -------------------------------------------------------


def test_trunk_names_what_is_missing():
    check = fit.trunk(stroller(folded_in=None), {"name": "Car", "trunk_in": None})
    assert check.outcome == fit.UNKNOWN
    assert "s specs.folded_in" in check.missing
    assert "household vehicle 'Car' trunk_in" in check.missing


def test_trunk_fits():
    check = fit.trunk(stroller(folded_in=[30, 20, 12]), {"name": "Car", "trunk_in": [40, 35, 20]})
    assert check.outcome == fit.FITS
    assert check.missing == []


def test_doorway():
    home = {"narrowest_doorway_in": 28}
    assert fit.doorway(stroller(open_width_in=24), home).outcome == fit.FITS
    assert fit.doorway(stroller(open_width_in=30), home).outcome == fit.NO_FIT
    assert fit.doorway(stroller(), home).outcome == fit.UNKNOWN


def test_car_seat_width():
    car = {"name": "Car", "rear_seat_width_in": 18}
    assert fit.car_seat_width(seat(base_width_in=17), car).outcome == fit.FITS
    assert fit.car_seat_width(seat(base_width_in=19), car).outcome == fit.NO_FIT


def test_bassinet_floor():
    home = {"bedside_space_in": [24, 40]}
    assert fit.bassinet_floor(bassinet(footprint_in=[38, 22]), home).outcome == fit.FITS
    assert fit.bassinet_floor(bassinet(footprint_in=[42, 22]), home).outcome == fit.NO_FIT


def test_bed_height_skipped_only_when_known_not_bedside():
    home = {"bed_top_height_in": 25}
    assert fit.bassinet_bed_height(bassinet(bedside_attach=False), home) is None


def test_bed_height_unknown_attach_is_unknown_even_with_a_range():
    home = {"bed_top_height_in": 25}
    check = fit.bassinet_bed_height(bassinet(fits_bed_height_in=[20, 30]), home)
    assert check.outcome == fit.UNKNOWN
    assert "b specs.bedside_attach" in check.missing


def test_bed_height_bedside():
    home = {"bed_top_height_in": 25}
    ok = bassinet(bedside_attach=True, fits_bed_height_in=[20, 30])
    low = bassinet(bedside_attach=True, fits_bed_height_in=[26, 30])
    assert fit.bassinet_bed_height(ok, home).outcome == fit.FITS
    assert fit.bassinet_bed_height(low, home).outcome == fit.NO_FIT


def test_overhead_bin():
    travel = {"flies": True, "overhead_bin_in": [22, 14, 9]}
    assert fit.overhead_bin(stroller(folded_in=[21, 13, 8]), travel).outcome == fit.FITS
    assert fit.overhead_bin(stroller(folded_in=[26, 18, 10]), travel).outcome == fit.NO_FIT
    assert fit.overhead_bin(stroller(), travel).outcome == fit.UNKNOWN


def test_overhead_bin_skipped_only_when_known_not_flying():
    section = "Stroller in an overhead bin"
    assert fit.run([stroller()], {"travel": {"flies": False}})[section] == []
    assert len(fit.run([stroller()], {"travel": {"flies": True}})[section]) == 1
    assert len(fit.run([stroller()], {})[section]) == 1  # unknown still asks


def test_future_vehicles_are_not_checked():
    household = {"future_vehicles": [{"name": "Later car", "trunk_in": [1, 1, 1]}]}
    assert fit.run([stroller()], household)["Stroller in the trunk"] == []


# --- running and rendering --------------------------------------------------


def test_rejected_candidates_are_skipped():
    rejected = stroller()
    rejected["status"] = "rejected"
    results = fit.run([rejected, seat()], {"vehicles": [{"name": "Car"}]})
    assert results["Travel system (car seat on stroller)"] == []
    assert results["Stroller in the trunk"] == []


def test_render_with_nothing_does_not_crash():
    text = fit.render([], {})
    assert "0 checks" in text
    assert "No vehicles" in text
    assert "Nothing to check yet." in text
    assert "No checks ran yet" in text  # zero checks must not read as "nothing blocks"


def test_render_lists_blockers_and_never_claims_a_fit_on_unknowns():
    text = fit.render([stroller(), seat()], {"vehicles": [{"name": "Car"}], "home": {}})
    assert "0 fit" in text
    assert "## What blocks a real answer" in text
    assert "- s specs.folded_in" in text
    assert "- household vehicle 'Car' trunk_in" in text
