# Open questions

The live backlog. Everything unknown in `candidates/items/*.yaml` and
`household/household.yaml` should trace back to an entry here.

Format: `- [ ] **N. Question** — why it matters, and what it blocks.`
Check the box and link the note under `research/notes/` once it is answered.
Numbers are never reused.

Seeded 2026-11-27 when the repo was created. No research has been done yet.

## Household facts (the household supplies these — agents must not guess)

- [x] **1. ~~Due date~~** — withdrawn 2026-11-27. Nick does not want the
  due date in a git repo, and it is not needed. Do not ask for it or add a
  field for it.

- [x] **2. Which car(s) will the baby ride in?** Answered 2026-11-27
  (Nick): a **2022 Tesla Model Y**. We buy for that car. A 2026 Model Y L
  may be added later; it is recorded under `future_vehicles` and is not
  checked. (`household.yaml` `vehicles`)

- [ ] **3. 2022 Model Y trunk (and frunk) dimensions** — usable length ×
  width × height, noting the hatch slope and wheel wells. **Stand-in
  recorded 2026-11-27:** trunk [40, 35.75, 19], frunk [27.6, 13.8, 11],
  the smallest of several independent measurements of 2020-21 cars, which
  disagree by 2-3 in
  ([note](notes/2026-11-27-model-y-2022-cargo-and-rear-seat.md)). Tesla
  publishes volumes only. Still wanted: a tape measure on our car (floor
  length, width between the wheel wells, height to the cargo cover, the
  hatch opening, and the sub-trunk well).
  (`vehicles[].trunk_in`, `vehicles[].frunk_in`)

- [ ] **4. Rear-seat width for car seat positions.** LATCH answered
  2026-11-27: lower anchors on the second-row outboard seats only; the
  center seat is seat-belt install only (Tesla manual). Width: Tesla gives
  none per position. One 2020 measurement says 18 in outboard, which is too
  thin to use. Tape-measure the outboard seat. Blocks the car seat width
  screen. (`vehicles[].rear_seat_width_in`)

- [ ] **5. Narrowest doorway, stairs, and stroller storage spot** — does the
  stroller need carrying up steps, and where will it live folded?
  (`home.narrowest_doorway_in`, `home.stairs_to_entry`,
  `home.stroller_storage_in`)

- [ ] **6. Bedside floor space and mattress-top height** — for the
  bassinet. Known 2026-11-27: a queen mattress on an upholstered platform
  frame that sticks out past the mattress, forming a ledge (see item 19).
  Still needed, by tape measure: the floor space beside the bed, the
  mattress-top height, how far the ledge sticks out, how far below the
  mattress top it sits, its height from the floor, and the clear gap under
  the frame. (`home.bedside_space_in`, `home.bed_top_height_in`,
  `home.bed_ledge_out_in`, `home.bed_ledge_drop_in`,
  `home.bed_ledge_top_height_in`, `home.bed_frame_floor_gap_in`)

- [ ] **7. Budget for each category** — or a total. (`budget_usd`)

- [x] **8. How will the stroller be used?** Answered 2026-11-27 (Nick):
  used for travel right away, from the start; never for running or
  jogging. That puts a compact fold and low weight ahead of big wheels and
  suspension, and the stroller must work for a newborn from day one (lie
  flat, or carry the infant car seat). Follow-up: item 20.
  (`lifestyle.notes`)

## Shape decisions (each likely becomes an ADR)

- [x] **9. Infant car seat + travel system, or a convertible seat from
  birth?** Decided 2026-11-27 (Nick):
  **an infant seat that clicks onto a compatible stroller**, then a
  convertible once it is outgrown — see
  [0002](../decisions/0002-infant-car-seat-that-clicks-onto-the-stroller.md).
  Nick accepted the cost of the second seat. The original question: An infant (bucket) seat clicks out of its base and onto a
  compatible stroller, but is outgrown at about 9-18 months. A convertible
  seat stays in the car and lasts years, but the baby has to be moved in and
  out every trip. This decision comes first: it decides whether the car
  seat ↔ stroller compatibility matters at all.

- [ ] **10. Full-size, compact, or travel stroller — or more than one?**
  Depends on items 3, 5, 8 and 20. Item 8's answer (travel from the start,
  no jogging) points toward compact or travel, but that is not decided.

- [ ] **11. Basic bassinet or a smart (responsive) bassinet — and buy, rent,
  or used?** Smart bassinets are much more expensive and are often rented.
  Their safety claims need primary sources, not marketing copy.

- [ ] **12. Is used or hand-me-down gear acceptable, and for which
  categories?** Car seats have an expiry date and should not be reused after
  a crash, so a used car seat needs a known history. Strollers and bassinets
  need a recall check against the exact model and manufacture date.

- [ ] **13. Same brand across categories?** Staying in one brand ecosystem
  can simplify the travel system but narrows the choices.

## Safety standards and how to check them (source before relying on them)

- [x] **14. FMVSS 213a status.** Answered 2026-11-27
  ([note](notes/2026-11-27-fmvss-213a-status-and-infant-seats.md)). The
  compliance date is **2026-12-05**, delayed from 2025 by a final rule of
  2026-09-09. It applies by date of manufacture: seats made earlier can still
  be sold. No label wording specific to 213a exists. A seat made on or after
  2026-12-05 must comply; an earlier one needs the maker's explicit claim.
  Split off as still open: item 24 (pending petition) and NHTSA ease-of-use
  ratings and car seat expiry norms (item 26).

- [ ] **15. Bassinets: the CPSC bassinet standard.** Confirm from CPSC what
  the mandatory bassinet/cradle standard is (16 CFR 1218, which incorporates
  ASTM F2194), what it covers for bedside sleepers, and AAP safe-sleep
  guidance that applies to bassinet choice.

- [ ] **16. Strollers: the stroller standard.** Confirm the mandatory CPSC
  stroller/carriage standard (16 CFR 1227 / ASTM F833) and what it covers.

- [ ] **17. How to check recalls.** Record the exact NHTSA (car seat) and
  CPSC (stroller, bassinet) recall search process, so each candidate's
  `safety.checked_on` means the same thing.

- [ ] **18. Travel-system compatibility sources.** Find where each
  manufacturer publishes its car seat compatibility and adapter charts, so
  `compat` entries come from primary sources rather than retailer listings.

## Raised by household facts (2026-11-27)

- [ ] **19. Can a bedside bassinet sit safely against our bed?** The frame
  is an upholstered platform that sticks out past the mattress, forming a
  ledge. Bedside sleepers are meant to sit flush against the mattress, with
  no gap a baby could slip into, and many have feet that slide under the bed
  frame. The ledge may hold the bassinet away from the mattress, or block
  those feet. **Look for designs made for platform beds or ledges.** Nick's
  example lead (2026-11-27, not yet evaluated): the
  [Arm's Reach Versatile Co-Sleeper](https://www.armsreach.com/products/versatile-co-sleeper),
  which specifically accommodates a platform ledge. For each bedside
  candidate, record what ledge geometry the maker says it accommodates
  (how far out, how far down, any under-bed clearance needed). Then compare
  it with the `home.bed_ledge_*` measurements; a fit check can be added once
  makers' specs show what to compare. Find
  out from manufacturers' manuals and the CPSC bassinet/bedside sleeper
  standard (item 15) what each candidate requires, and measure the ledge
  (item 6). If no bedside model fits safely, that points to a freestanding
  bassinet instead. This may need a new fit check once the requirements
  are known.

- [x] **20. Does "travel" include flying?** Answered 2026-11-27 (Nick):
  **yes.** So the stroller's fold size (overhead bin or gate check) and
  weight matter, and so does whether the car seat can be used on the plane.
  Follow-ups: items 21 and 22. The stroller fit report now has an
  "overhead bin" check. (`household.yaml` `travel`)

## Raised by flying and FMVSS 213a (2026-11-27)

- [x] **21. FAA approval for car seats.** Answered 2026-11-27
  ([note](notes/2026-11-27-faa-car-seat-use-on-aircraft.md)). The label
  is the red "This Restraint is Certified for Use in Motor Vehicles and
  Aircraft". A carrier with a belt path can go without its base (FAA InFO
  15013), but the manual decides: UPPAbaby Mesa V3 says never use the base on
  aircraft. FAA guide: ≤16 in wide fits "most" seats. Airlines must allow a
  ticketed child in an approved seat. New specs: `aircraft_install`,
  `carrier_width_in`.

- [ ] **22. Airline bin size and stroller policy.** Mostly answered
  2026-11-27 ([note](notes/2026-11-27-delta-american-stroller-car-seat-policy.md)):
  both are 22 × 14 × 9 in (Delta confirmed; aa.com could not be fetched).
  Both check strollers and car seats free; Delta confirmed gate check. Still
  open: whether American's 20 lb stroller limit is still live (a 2025 blog
  says it was removed) — read aa.com in a browser. Which airlines:
  answered 2026-11-27 (Nick) — **Delta and American Airlines**, most often.
  Still to research: each airline's carry-on/overhead bin size and stroller policy
  (some reportedly allow a compact folded stroller in the bin; gate check is
  common — confirm for each).
  Fills `travel.airlines` and `travel.overhead_bin_in`, which the overhead
  bin check needs.

- [ ] **23. Which infant car seats are certified to FMVSS 213a now, and
  how do we verify a specific unit?** First pass done 2026-11-27
  ([note](notes/2026-11-27-fmvss-213a-status-and-infant-seats.md)):
  explicit claims from UPPAbaby Mesa V3 and Aria V2, Chicco KeyFit 30 and
  KeyFit Max, and Doona +; Joie Mint Latch/Rue pending confirmation. None
  found for Nuna PIPA, Maxi-Cosi, KeyFit 35 or Clek Liingo. Verify a unit
  by its "Manufactured in" date (on or after 2026-12-05 means certified)
  or by the maker's confirmation. Original question: Required by
  [0001](../decisions/0001-car-seat-must-meet-fmvss-213a.md). Check each
  manufacturer's own statements and manuals, and NHTSA. Find out how the
  manufacture date and certification label show on the box and the seat,
  so a store unit made before the rule is not bought by mistake. Nick
  expects certified seats may be scarce at first; if none fit, raise it
  with him rather than relaxing 0001.

## Raised by the 2026-11-27 research round

- [ ] **24. Will the 213a date move again?** A petition for
  reconsideration from the "Baby Safety Alliance" (2026-10-23) was logged in
  NHTSA docket NHTSA-2025-0046 on 2026-11-24. Its content could not be
  fetched. Check the docket and the Federal Register around 2026-12-05.

- [ ] **25. How do we treat "tested according to FMVSS 213a" and
  "complies with new FMVSS213 side impact" wording?** Britax Willow S,
  Graco SnugRide and Cybex Aton G2 use it instead of "certified to 213a".
  Decision 0001 needs a ruling from Nick, or a confirmation from each maker.
  After 2026-12-05 this goes away for units made after that date.

- [ ] **26. NHTSA ease-of-use ratings and car seat expiry norms.** Split
  from item 14. nhtsa.gov blocked automated fetches, so it may need a
  browser.

## Raised by decision 0002 (2026-11-27)

- [ ] **27. When are infant seats typically outgrown, and by what limit?**
  Usually height or head room runs out before the 30 lb weight limit. The
  "9-18 months" estimate used in discussion is unsourced. Find the
  manufacturers' rules (e.g. head within 1 in of the shell top) for each
  shortlisted seat. This tells us when the convertible is needed.

- [ ] **28. How high does the carrier sit on each stroller, and how stable
  is it?** Nick, 2026-11-27: on the UPPAbaby Minu V3 the carrier sits high,
  which raises the center of gravity. For each seat and stroller pairing,
  find the carrier's height from the ground and any handlebar load limit
  from the manual. Also find how ASTM F833 (16 CFR 1227) tests stability
  with a car seat attached: the 2026-11-27 attempt to read the standard
  failed (the iteh.ai sample returned 404).

