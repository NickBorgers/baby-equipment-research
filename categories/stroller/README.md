# Stroller

The stroller itself, including a frame that exists only to carry an infant
car seat.

## Decisions

- [0002](../../decisions/0002-infant-car-seat-that-clicks-onto-the-stroller.md) —
  **accepted.** The stroller must accept the chosen infant car seat, per a
  manufacturer's chart or manual. The car seat is chosen first.

Open question 10 (full-size, compact or travel) is still open — see
[`research/open-questions.md`](../../research/open-questions.md).

## Candidates

None yet. See [`candidates/items/stroller.yaml`](../../candidates/items/stroller.yaml)
and the generated [`docs/COMPARISON.md`](../../docs/COMPARISON.md).

## What fits what

A stroller can be checked against the car's trunk, the narrowest doorway,
where it will be stored, and an airline overhead bin. It can also be checked against each car seat
candidate as a travel system: does the seat click on directly, with an
adapter, or not at all? That compatibility is recorded in each stroller's
`compat` block. See [`docs/FIT.md`](../../docs/FIT.md) and the `fit-check`
skill.

## Open questions

See `research/open-questions.md` items 3, 5, 10, 12, 13, 16, 18, 22 and 28.
Known use: travel from the start, including flying; no jogging (items 8 and 20).
