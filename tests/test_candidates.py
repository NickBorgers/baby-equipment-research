"""The candidate data has to stay internally consistent as agents edit it."""

from __future__ import annotations

import pytest

from tools import candidates, repo


@pytest.fixture(scope="module")
def schema():
    return repo.load_schema()


@pytest.fixture(scope="module")
def items():
    return repo.load_candidates()


@pytest.fixture(scope="module")
def decisions():
    return repo.load_decisions()


# --- the real repo data -----------------------------------------------------


def test_repo_data_is_valid(items, schema, decisions):
    errors = candidates.validate(items, schema, decisions)
    assert errors == [], "\n".join(errors)


def test_every_category_has_an_items_file_and_a_page(schema):
    for category in schema["categories"]:
        assert (repo.CANDIDATES_DIR / f"{category}.yaml").exists(), category
        assert (repo.ROOT / "categories" / category / "README.md").exists(), category


def test_every_category_has_spec_fields(schema):
    assert set(schema["spec_fields"]) == set(schema["categories"])


def test_adrs_have_complete_front_matter(decisions):
    required = {"id", "title", "status", "date", "category", "candidates"}
    for adr_id, adr in decisions.items():
        missing = required - set(adr["front_matter"])
        assert not missing, f"{adr_id}: front matter missing {sorted(missing)}"


def test_adr_ids_match_their_filenames(decisions):
    for adr_id, adr in decisions.items():
        assert adr["front_matter"]["id"] == adr_id, adr["path"].name


def test_adr_candidates_exist(decisions, items):
    known = {item["id"] for item in items}
    for adr_id, adr in decisions.items():
        listed = adr["front_matter"].get("candidates") or []
        unknown = set(listed) - known
        assert not unknown, f"{adr_id} lists unknown candidates {sorted(unknown)}"


def test_adr_categories_are_known(decisions, schema):
    known = set(schema["categories"]) | {"general"}
    for adr_id, adr in decisions.items():
        assert adr["front_matter"]["category"] in known, adr_id


def test_generated_docs_are_current():
    stale = [
        path.relative_to(repo.ROOT).as_posix()
        for path, content in candidates.generate().items()
        if repo.is_stale(path, content)
    ]
    assert stale == [], f"run `make docs`; stale: {stale}"


# --- the validator has to actually catch mistakes, on self-contained
# fixtures rather than the real repo data, so these hold regardless of what
# is or isn't in candidates/items/ at any given time -------------------------


def _item(**overrides):
    item = {"id": "sample", "name": "Sample", "category": "stroller", "status": "candidate"}
    item.update(overrides)
    return item


def _errors(schema, *items, decisions=None):
    return candidates.validate(list(items), schema, decisions or {})


def _has(errors, text):
    return any(text in error for error in errors)


def test_a_complete_valid_set_passes(schema):
    seat = _item(
        id="seat-a",
        category="car-seat",
        price_usd=299.99,
        specs={"weight_lb": 9.5, "child_weight_lb": [4, 35], "expiry_years": 7},
        safety={
            "standards": ["FMVSS 213"],
            "recalls": [{"date": "2025-01-02", "url": "https://example.com", "summary": "x"}],
            "checked_on": "2026-11-27",
        },
        pros=["light"],
        cons=["pricey"],
    )
    stroller = _item(
        id="stroller-a",
        specs={"folded_in": [30, 20, 12], "one_hand_fold": True, "weight_lb": None},
        compat={"accepts_car_seats": ["seat-a"]},
    )
    bassinet = _item(
        id="bassinet-a",
        category="bassinet",
        specs={"footprint_in": [35, 20], "fits_bed_height_in": [20, 30]},
    )
    assert _errors(schema, seat, stroller, bassinet) == []


def test_missing_required_field_is_rejected(schema):
    item = _item()
    del item["status"]
    assert _has(_errors(schema, item), "missing required field `status`")


def test_duplicate_id_is_rejected(schema):
    assert _has(_errors(schema, _item(), _item()), "duplicate id")


def test_non_kebab_id_is_rejected(schema):
    assert _has(_errors(schema, _item(id="Bad_Id")), "kebab-case")


def test_unknown_field_is_rejected(schema):
    assert _has(_errors(schema, _item(prise=42)), "unknown field")


def test_unknown_category_is_rejected(schema):
    assert _has(_errors(schema, _item(category="high-chair")), "unknown category")


def test_unknown_status_is_rejected(schema):
    assert _has(_errors(schema, _item(status="maybe-someday")), "unknown status")


def test_negative_price_is_rejected(schema):
    assert _has(_errors(schema, _item(price_usd=-5)), "price_usd")


def test_pros_must_be_a_list(schema):
    assert _has(_errors(schema, _item(pros="light")), "pros must be a list")


def test_missing_adr_is_rejected(schema):
    assert _has(_errors(schema, _item(decision="9999")), "9999")


def test_unquoted_adr_is_rejected(schema):
    assert _has(_errors(schema, _item(decision=1)), "four-digit")


def test_superseded_adr_reference_is_rejected(schema):
    fake = {
        "0001": {
            "path": repo.DECISIONS_DIR / "0001-fake.md",
            "front_matter": {"status": "superseded-by-0099"},
        }
    }
    errors = _errors(schema, _item(decision="0001"), decisions=fake)
    assert _has(errors, "superseded")


def test_spec_from_another_category_is_rejected(schema):
    # expiry_years is a car-seat spec, not a stroller one
    assert _has(_errors(schema, _item(specs={"expiry_years": 7})), "unknown spec")


@pytest.mark.parametrize(
    "specs, text",
    [
        ({"folded_in": [30, 20]}, "folded_in"),  # dims3 needs 3
        ({"weight_lb": "light"}, "weight_lb"),
        ({"weight_lb": True}, "weight_lb"),  # a bool is not a number
        ({"one_hand_fold": "yes"}, "one_hand_fold"),
    ],
)
def test_bad_spec_values_are_rejected(schema, specs, text):
    assert _has(_errors(schema, _item(specs=specs)), f"specs.{text}")


def test_inverted_range_is_rejected(schema):
    seat = _item(category="car-seat", specs={"child_weight_lb": [35, 4]})
    assert _has(_errors(schema, seat), "min <= max")


def test_recall_without_url_is_rejected(schema):
    item = _item(safety={"recalls": [{"date": "2025-01-02", "summary": "x"}]})
    assert _has(_errors(schema, item), "needs a url")


def test_recall_without_date_is_rejected(schema):
    item = _item(safety={"recalls": [{"url": "https://example.com"}]})
    assert _has(_errors(schema, item), "needs a date")


def test_unknown_safety_field_is_rejected(schema):
    assert _has(_errors(schema, _item(safety={"rating": 5})), "unknown safety field")


def test_compat_naming_an_unknown_seat_is_rejected(schema):
    item = _item(compat={"accepts_car_seats": ["no-such-seat"]})
    assert _has(_errors(schema, item), "not a car-seat id")


def test_compat_naming_a_non_seat_is_rejected(schema):
    other = _item(id="other-stroller")
    item = _item(compat={"needs_adapter": {"other-stroller": "Adapter X"}})
    assert _has(_errors(schema, item, other), "not a car-seat id")


def test_compat_on_a_non_stroller_is_rejected(schema):
    seat = _item(category="car-seat", compat={"accepts_car_seats": []})
    assert _has(_errors(schema, seat), "only belongs on strollers")


def test_compat_listing_a_seat_twice_is_rejected(schema):
    seat = _item(id="seat-a", category="car-seat")
    stroller = _item(
        id="stroller-a",
        compat={"accepts_car_seats": ["seat-a"], "incompatible": ["seat-a"]},
    )
    assert _has(_errors(schema, seat, stroller), "more than one place")


def test_adapter_needs_a_name(schema):
    seat = _item(id="seat-a", category="car-seat")
    stroller = _item(id="stroller-a", compat={"needs_adapter": {"seat-a": ""}})
    assert _has(_errors(schema, seat, stroller), "adapter name")


def test_meets_213a_only_when_recorded():
    assert candidates.meets_213a({"safety": {"standards": ["FMVSS 213", "FMVSS 213a"]}})
    assert candidates.meets_213a({"safety": {"standards": ["fmvss213a"]}})
    assert not candidates.meets_213a({"safety": {"standards": ["FMVSS 213"]}})
    assert not candidates.meets_213a({})


def test_car_seat_table_has_a_213a_column(schema):
    seats = [
        _item(id="a", category="car-seat", safety={"standards": ["FMVSS 213a"]}),
        _item(id="b", category="car-seat"),
    ]
    text = candidates.render_comparison(seats, schema, {})
    assert "| Candidate | Status | Price | 213a |" in text
    assert "| `a` — Sample | candidate | ? | yes |" in text
    assert "| `b` — Sample | candidate | ? | ? |" in text  # not recorded is ?, not "no"


# --- rendering --------------------------------------------------------------


def test_comparison_marks_unknowns_and_skips_rejected_from_cost(schema):
    items = [
        _item(id="a", status="selected", price_usd=100, specs={"folded_in": [1, 2, 3]}),
        _item(id="b", status="rejected", price_usd=999),
        _item(id="c", status="selected"),
        _item(id="d", category="car-seat", specs={"child_weight_lb": [4, 35]}),
    ]
    text = candidates.render_comparison(items, schema, {})
    assert "$100.00" in text
    assert "1×2×3" in text
    assert "4–35" in text  # a range reads as a range, not a size
    assert "| ? |" in text  # unknown weight shows as ?
    assert "across 1 priced, decided items" in text
    assert "1 decided items are still unpriced" in text
