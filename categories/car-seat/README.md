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
- [0003](../../decisions/0003-no-rotation-now-buy-for-the-long-run.md) —
  **accepted.** The infant seat does not rotate. The follow-on seat must
  rotate, and should be the last seat if possible.

## Candidates

None yet. Seats that pass 0001 are listed in the
[market survey](../../research/notes/2026-11-27-infant-car-seat-market-survey.md).
See [`candidates/items/car-seat.yaml`](../../candidates/items/car-seat.yaml)
and the generated [`docs/COMPARISON.md`](../../docs/COMPARISON.md).

## What to judge

A recommendation covers every row below, or lists the rows it skipped
(AGENTS.md rules 8 and 9). The usability rows come from a summary of
hands-on Primo Viaggio Nido reviews that Nick shared on 2026-11-27. It has
not been re-read at its sources yet (open question 36).

**What the seat is** (specs and manuals):

- 213a claim (0001), child limits, expiry.
- Carrier weight **as used**, with canopy and inserts. The maker's figure
  often leaves these out.
- Carrier width (airline seats), aircraft install, baseless install.
- Model Y fit and front legroom.
- Strollers it clicks onto, and which adapters they need.

**Getting it right every time** (safety-relevant usability):

- **Recline.** Can you reach the recline the manual requires in our car
  without a pool noodle? Can you trust the indicator? Why recline matters
  for a newborn needs a primary source (manual or AAP) before it is cited.
- **Insert and harness fit across ages.** At newborn size, 4 months and 7
  months: where the crotch buckle sits, whether the head slumps, whether
  the insert digs in. Does the manual say clearly when to change inserts?
- **Base install hardware.** Does the lock-off stay locked? Is there a
  tensioner? Is the load leg easy to adjust, with a "set correctly"
  indicator?
- **Click-in indicator.** Can it show "locked" when the carrier is not?
- **Baseless install stability.** It matters for taxis and travel.

**Daily friction:**

- Buckle and chest clip effort. Harness adjustment.
- Carrying the carrier: handle, weight, length.
- Click on and off the base and the stroller.
- Canopy, fabric feel, cleaning.
- Durability of small parts, such as covers, doors and storage clips.

**Sources:** see "Usability research" in [`AGENTS.md`](../../AGENTS.md).

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
