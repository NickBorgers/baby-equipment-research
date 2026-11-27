# Car seat

The car seat for the newborn period: either an infant (rear-facing bucket)
seat with a base that stays in the car, or a convertible seat used from
birth.

## Decisions

- [0001](../../decisions/0001-car-seat-must-meet-fmvss-213a.md) —
  **accepted.** The seat must be certified to FMVSS 213a, the federal
  side-impact test. The specific unit bought must be too.

- [0002](../../decisions/0002-infant-car-seat-that-clicks-onto-the-stroller.md) —
  **accepted.** Start with an infant seat that clicks onto a compatible
  stroller. A convertible follows once it is outgrown.

## Candidates

None yet. See [`candidates/items/car-seat.yaml`](../../candidates/items/car-seat.yaml)
and the generated [`docs/COMPARISON.md`](../../docs/COMPARISON.md).

## What fits what

A car seat is screened against each car's rear-seat width (a rough screen
only; the vehicle's and seat's manuals decide). An infant seat may also pair
with a stroller as a travel system, which is recorded on the stroller's
`compat` block, not here. See [`docs/FIT.md`](../../docs/FIT.md).

## Safety notes for whoever picks this up

Every safety claim (standards met, recalls, expiry) needs a primary source:
NHTSA or the manufacturer. Car seats expire, and should not be reused after
a crash — so used seats need a known history (open question 12).

## Open questions

See `research/open-questions.md` items 3, 4, 12, 13, 14, 17, 18, 21 (FAA approval) 23 (213a availability), 27 (when outgrown) and 28 (ride height on the stroller).
It will be used on planes (item 20).
