---
name: fit-check
description: Check baby-equipment compatibility and fit — car seat on stroller (travel system), folded stroller in the trunk / through the door / in storage, car seat in the back seat, bassinet beside the bed — using tools/fit.py, and interpret the "insufficient data" results. Use for any question of the form "will this work with that car / stroller / room?".
---

# Checking compatibility and fit

The checks live in `tools/fit.py` and are rendered into `docs/FIT.md`. To
print the report without writing anything, run:

```sh
make fit
```

## The three outcomes

- **fits**: every input is known, and it fits.
- **does not fit**: every input needed is known, and it does not fit.
- **insufficient data**: something is still null.

An unknown **never** counts as a fit.

## The checks

| Check | Compares | Inputs |
| --- | --- | --- |
| Travel system | does the car seat click onto the stroller? | the stroller's `compat` |
| Trunk | folded stroller vs. trunk, rotation allowed | stroller `specs.folded_in`, `vehicles[].trunk_in` |
| Doorway | open stroller width vs. narrowest door | stroller `specs.open_width_in`, `home.narrowest_doorway_in` |
| Storage | folded stroller vs. storage spot | stroller `specs.folded_in`, `home.stroller_storage_in` |
| Overhead bin | folded stroller vs. strictest airline bin (only when `travel.flies` is not false) | stroller `specs.folded_in`, `travel.overhead_bin_in` |
| Back seat | car seat width vs. rear seat width | car seat `specs.base_width_in`, `vehicles[].rear_seat_width_in` |
| Bassinet floor | footprint vs. bedside floor space | bassinet `specs.footprint_in`, `home.bedside_space_in` |
| Bed height | bed height within the maker's range (bedside models only) | bassinet `specs.bedside_attach`, `specs.fits_bed_height_in`, `home.bed_top_height_in` |

The candidate inputs live in `candidates/items/*.yaml`. The household inputs
live in `household/household.yaml`. Rejected candidates are skipped, and so
are `future_vehicles`.

An "overhead bin: does not fit" is not a dealbreaker by itself: airlines
commonly let you gate-check a stroller (confirm per airline, open question
22). It is one trade-off among others.

## Reading the results

- **Box checks allow rotation.** Both sets of dimensions are sorted, largest
  first. A real trunk has a sloped hatch and wheel wells, so treat a "fits"
  as a screen and test it in person before buying.
- **The back-seat check is a rough screen.** Whether a car seat fits a
  vehicle depends on the seat belt or LATCH geometry and the recline angle.
  The vehicle's manual and the seat's manual decide, not this check.
- **Travel system "unknown" is not "incompatible".** It means the stroller's
  `compat` does not list that seat. Find the manufacturer's compatibility
  chart (open question 18) and record the answer.
- **The bed-height check is skipped** only when a bassinet is known *not* to
  attach at the bedside (`bedside_attach: false`). If that is unknown, the
  check still runs and reports insufficient data.

## The research queue

The "What blocks a real answer" section of `docs/FIT.md` lists exactly which
fields are missing. Household fields are for Nick to measure, so ask him.
Candidate fields need research: use the `research-note` skill, then
`candidate-update`.

Never make a check pass by inventing inputs.
