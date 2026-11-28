# Stroller

The stroller itself, including a frame that exists only to carry an infant
car seat.

## Decisions

- [0002](../../decisions/0002-infant-car-seat-that-clicks-onto-the-stroller.md) —
  **accepted.** The stroller must accept the chosen infant car seat, per a
  manufacturer's chart or manual. The car seat is chosen first.
- [0004](../../decisions/0004-buy-the-uppababy-aria-v2.md) — **accepted.**
  The car seat is the UPPAbaby Aria V2, so the stroller must take it.
- [0003](../../decisions/0003-no-rotation-now-buy-for-the-long-run.md) —
  **accepted.** The stroller outlasts the infant seat: newborn-capable on
  its own, rated to about 50 lb, and takes the infant seat by adapter.
  Frame strollers are out.

Open question 10 (full-size, compact or travel) is still open — see
[`research/open-questions.md`](../../research/open-questions.md).

## Candidates

Eight candidates from the first round (2026-11-28), all of which take the
Aria V2 or may: five UPPAbaby strollers, the Mockingbird Travel and Single
3.0, and the Zoe Tour V3. Specs only so far; usability is not yet judged.
See [`candidates/items/stroller.yaml`](../../candidates/items/stroller.yaml)
and the generated [`docs/COMPARISON.md`](../../docs/COMPARISON.md).

## What to judge

A recommendation covers every row below, or lists the rows it skipped
(AGENTS.md rules 8 and 9). This list is a starting point. It is not yet
based on reviews.

- **What it is:** weight as used, folded size, child limit (about 50 lb,
  0003), newborn mode without the car seat, maker-listed adapter for the
  chosen car seat.
- **Getting it right:** how securely the car seat locks on, and how you can
  tell it is locked. Brake reliability. Stability with the car seat on,
  including how high the carrier sits (open question 28).
- **Daily friction:** fold and unfold (one hand? does it stand when
  folded?), push and steering on rough ground, canopy, basket access with
  the car seat on, carrying it folded through an airport.
- **Sources:** see "Usability research" in [`AGENTS.md`](../../AGENTS.md).

## What fits what

A stroller can be checked against the car's trunk, the narrowest doorway,
where it will be stored, and an airline overhead bin. It can also be checked against each car seat
candidate as a travel system: does the seat click on directly, with an
adapter, or not at all? That compatibility is recorded in each stroller's
`compat` block. See [`docs/FIT.md`](../../docs/FIT.md) and the `fit-check`
skill.

## Open questions

See `research/open-questions.md` items 3, 5, 10, 12, 13, 18, 22, 28 and
44-48.
Known use: travel from the start, including flying; no jogging (items 8 and 20).
