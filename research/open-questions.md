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
  width × height, noting the hatch slope and wheel wells. Blocks the
  "stroller in the trunk" check. Ideally tape-measured on our car.
  Otherwise, published measurements for a 2022 (pre-refresh) Model Y are
  researchable — record their source, at medium confidence at best.
  (`vehicles[].trunk_in`, `vehicles[].frunk_in`)

- [ ] **4. Rear-seat width for car seat positions** — and which positions
  have LATCH anchors. Blocks the car seat width screen.
  (`vehicles[].rear_seat_width_in`)

- [ ] **5. Narrowest doorway, stairs, and stroller storage spot** — does the
  stroller need carrying up steps, and where will it live folded?
  (`home.narrowest_doorway_in`, `home.stairs_to_entry`,
  `home.stroller_storage_in`)

- [ ] **6. Bedside floor space and mattress-top height** — for the
  bassinet. Known 2026-11-27: a queen mattress on an upholstered frame with
  a ledge around the mattress edge (see item 19). Still needed: the floor
  space beside the bed, the mattress-top height, and the ledge's width and
  height. (`home.bedside_space_in`, `home.bed_top_height_in`,
  `home.bed_notes`)

- [ ] **7. Budget for each category** — or a total. (`budget_usd`)

- [x] **8. How will the stroller be used?** Answered 2026-11-27 (Nick):
  used for travel right away, from the start; never for running or
  jogging. That puts a compact fold and low weight ahead of big wheels and
  suspension, and the stroller must work for a newborn from day one (lie
  flat, or carry the infant car seat). Follow-up: item 20.
  (`lifestyle.notes`)

## Shape decisions (each likely becomes an ADR)

- [ ] **9. Infant car seat + travel system, or a convertible seat from
  birth?** An infant (bucket) seat clicks out of its base and onto a
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

- [ ] **14. Car seats: FMVSS 213, and the status of the side-impact rule.**
  Confirm from NHTSA what FMVSS 213 requires and the current status and
  compliance date of NHTSA's side-impact requirement for car seats (FMVSS
  213a). From memory, not yet sourced: the final rule came out in 2023 with
  a compliance date in December 2026. If so, that is within weeks of now.
  Also find what a 213a-certified seat's label or manual says, NHTSA's
  ease-of-use ratings, and car seat expiry norms. **Needed by
  [0001](../decisions/0001-car-seat-must-meet-fmvss-213a.md).**

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
  is upholstered and has a ledge around the mattress edge. Bedside sleepers
  are meant to sit flush against the mattress, with no gap a baby could
  slip into, and many have feet that slide under the bed frame. A ledge
  may hold the bassinet away from the mattress, or block those feet. Find
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

- [ ] **21. FAA approval for car seats.** Confirm from the FAA what label
  wording makes a car seat approved for aircraft, and whether infant seats
  without their base can be used on board. Also: does the seat fit a
  typical economy seat width? Fills the car seat's `specs.faa_approved`.

- [ ] **22. Airline bin size and stroller policy.** Which airlines:
  answered 2026-11-27 (Nick) — **Delta and American Airlines**, most often.
  Still to research: each airline's carry-on/overhead bin size and stroller policy
  (some reportedly allow a compact folded stroller in the bin; gate check is
  common — confirm for each).
  Fills `travel.airlines` and `travel.overhead_bin_in`, which the overhead
  bin check needs.

- [ ] **23. Which infant car seats are certified to FMVSS 213a now, and
  how do we verify a specific unit?** Required by
  [0001](../decisions/0001-car-seat-must-meet-fmvss-213a.md). Check each
  manufacturer's own statements and manuals, and NHTSA. Find out how the
  manufacture date and certification label show on the box and the seat,
  so a store unit made before the rule is not bought by mistake. Nick
  expects certified seats may be scarce at first; if none fit, raise it
  with him rather than relaxing 0001.

