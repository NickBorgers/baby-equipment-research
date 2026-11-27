# Open questions

The live backlog. Everything unknown in `candidates/items/*.yaml` and
`household/household.yaml` should trace back to an entry here.

Format: `- [ ] **N. Question** — why it matters, and what it blocks.`
Check the box and link the note under `research/notes/` once it is answered.
Numbers are never reused.

Seeded 2026-11-27 when the repo was created. No research has been done yet.

## Household facts (the household supplies these — agents must not guess)

- [ ] **1. Due date** — sets how much time there is to research and order,
  and whether holiday/Black Friday pricing is in play.
  (`household.yaml` `due_date`)

- [ ] **2. Which car(s) will the baby ride in?** Make, model and year for
  each. A trunk measurement and the rear-seat width decide which strollers
  and car seats fit. (`household.yaml` `vehicles`)

- [ ] **3. Trunk dimensions for each car** — usable length × width × height,
  tape-measured, noting the hatch slope and wheel wells. Blocks the "stroller
  in the trunk" check. (`vehicles[].trunk_in`)

- [ ] **4. Rear-seat width for car seat positions** — and which positions
  have LATCH anchors. Blocks the car seat width screen.
  (`vehicles[].rear_seat_width_in`)

- [ ] **5. Narrowest doorway, stairs, and stroller storage spot** — does the
  stroller need carrying up steps, and where will it live folded?
  (`home.narrowest_doorway_in`, `home.stairs_to_entry`,
  `home.stroller_storage_in`)

- [ ] **6. Bedside floor space and mattress-top height** — for the
  bassinet. (`home.bedside_space_in`, `home.bed_top_height_in`)

- [ ] **7. Budget for each category** — or a total. (`budget_usd`)

- [ ] **8. How will the stroller be used?** City sidewalks, suburban car
  trips, gravel/trails, jogging, air travel, public transit. This decides
  which stroller trade-offs matter most. (`lifestyle.notes`)

## Shape decisions (each likely becomes an ADR)

- [ ] **9. Infant car seat + travel system, or a convertible seat from
  birth?** An infant (bucket) seat clicks out of its base and onto a
  compatible stroller, but is outgrown at about 9-18 months. A convertible
  seat stays in the car and lasts years, but the baby has to be moved in and
  out every trip. This decision comes first: it decides whether the car
  seat ↔ stroller compatibility matters at all.

- [ ] **10. Full-size, compact, or travel stroller — or more than one?**
  Depends on items 3, 5 and 8.

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
  213a). Also NHTSA's ease-of-use ratings and car seat expiry norms.

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
