<!-- GENERATED FILE — do not edit by hand.
     Edit the YAML under candidates/ and household/, then run `make docs`. -->

# Compatibility and fit

42 checks: 28 fit, 9 do not fit, 5 have insufficient data.

An unknown never counts as a fit. See `tools/fit.py` for the method and the `fit-check` skill for how to read this.

## Travel system (car seat on stroller)

| Candidate | Against | Result | Detail |
| --- | --- | --- | --- |
| `uppababy-minu-v3` | uppababy-aria-v2 | fits | with adapter: Adapters for Minu V3 (Aria & Mesa), 0904-MMA-WW |
| `uppababy-minu-v3` | uppababy-mesa-v3 | fits | with adapter: Adapters for Minu V3 (Aria & Mesa), 0904-MMA-WW |
| `uppababy-kona` | uppababy-aria-v2 | fits | direct, no adapter |
| `uppababy-kona` | uppababy-mesa-v3 | insufficient data | not listed in the stroller's compat |
| `uppababy-cruz-v3` | uppababy-aria-v2 | fits | direct, no adapter |
| `uppababy-cruz-v3` | uppababy-mesa-v3 | fits | direct, no adapter |
| `uppababy-vista-v3` | uppababy-aria-v2 | fits | direct, no adapter |
| `uppababy-vista-v3` | uppababy-mesa-v3 | fits | direct, no adapter |
| `uppababy-ridge-v2` | uppababy-aria-v2 | fits | with adapter: Adapters for Ridge (Aria, Mesa & Bassinet), 0901-RMA-WW |
| `uppababy-ridge-v2` | uppababy-mesa-v3 | fits | with adapter: Adapters for Ridge (Aria, Mesa & Bassinet), 0901-RMA-WW |
| `mockingbird-travel-stroller` | uppababy-aria-v2 | fits | with adapter: FlexConnect strap adapter (included), or QuickConnect UPPAbaby Adapter ($50) |
| `mockingbird-travel-stroller` | uppababy-mesa-v3 | insufficient data | not listed in the stroller's compat |
| `zoe-tour-v3` | uppababy-aria-v2 | fits | with adapter: Tour V3 UPPAbaby Car Seat Adapter, model 810033595783 ($55) |
| `zoe-tour-v3` | uppababy-mesa-v3 | fits | with adapter: Tour V3 UPPAbaby Car Seat Adapter, model 810033595783 ($55) |
| `mockingbird-single-3` | uppababy-aria-v2 | fits | with adapter: Mockingbird Car Seat Adapter, Uppababy option ($50) |
| `mockingbird-single-3` | uppababy-mesa-v3 | fits | with adapter: Mockingbird Car Seat Adapter, Uppababy option ($50) |

## Stroller in the trunk

| Candidate | Against | Result | Detail |
| --- | --- | --- | --- |
| `uppababy-minu-v3` | 2022 Tesla Model Y trunk | fits | folded size vs. trunk, rotation allowed |
| `uppababy-kona` | 2022 Tesla Model Y trunk | fits | folded size vs. trunk, rotation allowed |
| `uppababy-cruz-v3` | 2022 Tesla Model Y trunk | fits | folded size vs. trunk, rotation allowed |
| `uppababy-vista-v3` | 2022 Tesla Model Y trunk | fits | folded size vs. trunk, rotation allowed |
| `uppababy-ridge-v2` | 2022 Tesla Model Y trunk | **does not fit** | folded size vs. trunk, rotation allowed |
| `mockingbird-travel-stroller` | 2022 Tesla Model Y trunk | fits | folded size vs. trunk, rotation allowed |
| `zoe-tour-v3` | 2022 Tesla Model Y trunk | fits | folded size vs. trunk, rotation allowed |
| `mockingbird-single-3` | 2022 Tesla Model Y trunk | fits | folded size vs. trunk, rotation allowed |

## Stroller through the door

| Candidate | Against | Result | Detail |
| --- | --- | --- | --- |
| `uppababy-minu-v3` | narrowest doorway | fits | open width vs. door width |
| `uppababy-kona` | narrowest doorway | fits | open width vs. door width |
| `uppababy-cruz-v3` | narrowest doorway | fits | open width vs. door width |
| `uppababy-vista-v3` | narrowest doorway | fits | open width vs. door width |
| `uppababy-ridge-v2` | narrowest doorway | fits | open width vs. door width |
| `mockingbird-travel-stroller` | narrowest doorway | fits | open width vs. door width |
| `zoe-tour-v3` | narrowest doorway | fits | open width vs. door width |
| `mockingbird-single-3` | narrowest doorway | insufficient data | open width vs. door width |

## Stroller in its storage spot

Nothing to check yet.

## Stroller in an overhead bin

| Candidate | Against | Result | Detail |
| --- | --- | --- | --- |
| `uppababy-minu-v3` | airline overhead bin | **does not fit** | folded size vs. strictest bin limit; gate check is the fallback |
| `uppababy-kona` | airline overhead bin | **does not fit** | folded size vs. strictest bin limit; gate check is the fallback |
| `uppababy-cruz-v3` | airline overhead bin | **does not fit** | folded size vs. strictest bin limit; gate check is the fallback |
| `uppababy-vista-v3` | airline overhead bin | **does not fit** | folded size vs. strictest bin limit; gate check is the fallback |
| `uppababy-ridge-v2` | airline overhead bin | **does not fit** | folded size vs. strictest bin limit; gate check is the fallback |
| `mockingbird-travel-stroller` | airline overhead bin | **does not fit** | folded size vs. strictest bin limit; gate check is the fallback |
| `zoe-tour-v3` | airline overhead bin | **does not fit** | folded size vs. strictest bin limit; gate check is the fallback |
| `mockingbird-single-3` | airline overhead bin | **does not fit** | folded size vs. strictest bin limit; gate check is the fallback |

## Car seat in the back seat

| Candidate | Against | Result | Detail |
| --- | --- | --- | --- |
| `uppababy-aria-v2` | 2022 Tesla Model Y rear seat | insufficient data | rough screen only — the vehicle and seat manuals decide |
| `uppababy-mesa-v3` | 2022 Tesla Model Y rear seat | insufficient data | rough screen only — the vehicle and seat manuals decide |

## Bassinet beside the bed

Nothing to check yet.

## What blocks a real answer

- household vehicle '2022 Tesla Model Y' rear_seat_width_in
- mockingbird-single-3 specs.open_width_in
- mockingbird-travel-stroller compat for uppababy-mesa-v3
- uppababy-aria-v2 specs.base_width_in
- uppababy-kona compat for uppababy-mesa-v3
- uppababy-mesa-v3 specs.base_width_in
