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
  `safety.checked_on` means the same thing. Progress 2026-11-27
  ([note](notes/2026-11-27-infant-car-seat-market-survey.md)): nhtsa.gov
  and api.nhtsa.gov block scripts, but NHTSA's static recall flat file
  (`static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL_POST_2010.zip`, child-restraint
  records have type `C`) downloads and can be searched by make and model.
  Still open: the CPSC side, and whether a flat-file search is accepted as
  equal to the official per-model lookup.

- [ ] **18. Travel-system compatibility sources.** Find where each
  manufacturer publishes its car seat compatibility and adapter charts, so
  `compat` entries come from primary sources rather than retailer listings.
  Progress 2026-11-27
  ([note](notes/2026-11-27-infant-car-seat-market-survey.md)): UPPAbaby
  lists strollers in each seat's manual; Chicco says "all Chicco strollers
  (except the Liteway and Urbino)"; Joie publishes chart v6 on
  dl.joiebaby.com; Britax an Adobe InDesign chart (06.2026); Peg Perego a
  universal adapter list (July 2026) covering about 15 stroller brands.
  Third-party charts seen: Thule (lists no Mesa V3 or KeyFit Max),
  Mockingbird, Bugaboo (Chicco KeyFit), Silver Cross. UPPAbaby's support
  site returned 403.

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
  KeyFit Max, and Doona +; Joie Mint Latch/Rue pending confirmation.
  Second pass 2026-11-27
  ([note](notes/2026-11-27-infant-car-seat-market-survey.md)): Joie
  confirmed on joiebaby.com (brand page: "All Joie car seats meet the new
  213a and 213b safety standards, with the exception of chili spin 360");
  Doona X confirmed in its manual; **Peg Perego Primo Viaggio** (all four
  variants) declares FMVSS 571-213a in its 2025 US manuals. Doona+'s claim
  is on its website only, not in its manual. None
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
  Checked 2026-11-27 (web search, Federal Register): no notice moves the
  date; the [2026-09-09 final rule](https://www.federalregister.gov/documents/2026/09/09/2026-18380/federal-motor-vehicle-safety-standard-no-213a-child-restraint-systems-side-impact-protection-federal)
  still stands. Check again just before buying.

- [ ] **25. How do we treat "tested according to FMVSS 213a" and
  "complies with new FMVSS213 side impact" wording?** Britax Willow S,
  Graco SnugRide and Cybex Aton G2 use it instead of "certified to 213a".
  Decision 0001 needs a ruling from Nick, or a confirmation from each maker.
  After 2026-12-05 this goes away for units made after that date.
  Two more cases found 2026-11-27: Cybex's Aton G2 Swivel and Cloud G Pro
  manuals claim **213b** (which requires 213a, by inference) while the
  pages avoid "213a"; Joie's Rue LX Spin page says "Tested to ... FMVSS
  213a" while Joie's brand page says all its seats "meet" 213a
  ([rotation note](notes/2026-11-27-rotating-infant-car-seats.md)).

- [ ] **26. NHTSA ease-of-use ratings and car seat expiry norms.** Split
  from item 14. nhtsa.gov blocked automated fetches, so it may need a
  browser.
  **Ease-of-use part answered 2026-11-27:** the program is current and
  readable through `api.nhtsa.gov/childSeats?dataSet=ratings` with a
  browser User-Agent. KeyFit 30 ClearTex 3 stars, Rue 4, Mint 4, Mesa V2 5;
  Mesa V3, Aria V2, KeyFit Max, Primo Viaggio and Juni not rated in the
  feed. See the [ratings note](notes/2026-11-27-nhtsa-ease-of-use-ratings.md).
  Expiry norms remain open.

## Raised by decision 0002 (2026-11-27)

- [ ] **27. When are infant seats typically outgrown, and by what limit?**
  Usually height or head room runs out before the 30 lb weight limit. The
  "9-18 months" estimate used in discussion is unsourced. Find the
  manufacturers' rules (e.g. head within 1 in of the shell top) for each
  shortlisted seat. This tells us when the convertible is needed.
  Progress 2026-11-27
  ([note](notes/2026-11-27-infant-car-seat-market-survey.md)): every seat
  read uses a 1 in head-room rule (head at least 1 in below the top of
  the shell or headrest) plus a height cap: 30 in for Aria V2, KeyFit 30
  and Joie; 32 in for Mesa V3, KeyFit Max, Doona, Peg Perego and Cybex.
  Still open: at what age that typically happens (needs growth data, not
  manuals).

- [ ] **28. How high does the carrier sit on each stroller, and how stable
  is it?** Nick, 2026-11-27: on the UPPAbaby Minu V3 the carrier sits high,
  which raises the center of gravity. For each seat and stroller pairing,
  find the carrier's height from the ground and any handlebar load limit
  from the manual. Also find how ASTM F833 (16 CFR 1227) tests stability
  with a car seat attached: the 2026-11-27 attempt to read the standard
  failed (the iteh.ai sample returned 404).
  Progress 2026-11-28, Aria V2
  ([note](notes/2026-11-28-uppababy-aria-v2-on-stroller-and-model-y.md)):
  no ground-to-carrier height published for any UPPAbaby stroller. No
  manual gives a handlebar limit in pounds; basket limits are 20 lb (Minu
  V3, Ridge V2) and 30 lb (Vista V3, Cruz V3). No tip-over reports found
  (Reddit blocked). Still open: a tape measure in a store.

## Raised by the infant car seat survey (2026-11-27)

- [ ] **29. Will a 17-17.75 in carrier fit our airline seats?** Every
  qualifying infant carrier is wider than the FAA's 16 in guide (narrowest:
  Chicco KeyFit 30, 16.75 in;
  [note](notes/2026-11-27-infant-car-seat-market-survey.md)). Look up
  Delta's and American's published seat widths (14 CFR 121.311(k)) for the
  aircraft we usually fly, especially regional jets, once a seat is chosen.
  Mostly answered 2026-11-27
  ([note](notes/2026-11-27-airline-seat-width-vs-infant-carriers.md)): the
  narrowest Main seats on Delta's and American's A319/A320/A321 and 737s
  (16.2-16.6 in) are narrower than the KeyFit 30, Mesa V3 and Primo Viaggio carriers. Regional
  jets and the A220 are 17.3-18.6 in. The FAA (AC 120-87C 10.f) says the
  airline must move a ticketed car seat that does not fit to another seat in
  the same class. Still open: which rows are narrow, and whether the
  carrier's widest point sits at armrest height.

- [ ] **30. Model Y fit for anything but the KeyFit 30.** The only
  independent infant seat test in a pre-refresh Model Y is Cars.com's
  KeyFit 30 (grade A). Unknown: fit of each shortlisted seat; whether the
  rear footwell suits a load leg (the 2022.40 Tesla manual says nothing
  about support legs); and whether a rotating base has room to swing the
  carrier side-on. A test install at a store, or owner reports, would do.
  Progress 2026-11-27
  ([note](notes/2026-11-27-model-y-infant-seat-fit-and-load-leg.md)): no
  independent test of the Primo Viaggio or the Mesa in a Model Y; one owner
  report for a Mesa. Tesla's 2022.16 Japan-edition manual says "All
  passenger seats Model Y support the use of a child restraint system with
  a safety leg". Tesla's service manual shows no floor compartment in the
  second-row footwell. Load leg settled 2026-11-27 (Nick): the Model Y
  floor is a solid plate over the battery structure, with no hollow
  compartment, so a load leg has a solid floor to stand on. Still open: fit
  of each seat, and a test install in our car.
  Aria V2, 2026-11-28
  ([note](notes/2026-11-28-uppababy-aria-v2-on-stroller-and-model-y.md)):
  no Model Y report for any Aria. Nick, 2026-11-28: the Model Y always
  uses the base, so baseless fit there (e.g. whether its shoulder belt
  wraps the V2 shell) does not matter. What matters is the base install:
  LATCH or belt, load leg, recline and front legroom.

- [ ] **31. Is Joie actually in stock in the US, and what is "Baby Safety
  Alliance certified"?** Joie's Rue, Mint Latch and Rue LX Spin pages carry
  a "coming soon" notify form that may or may not be shown. The Rue LX Spin
  page names the Baby Safety Alliance as a certifier; that is the group
  whose 213a petition is pending (item 24).
  **Partly answered 2026-11-27:** the Rue is in stock at Babylist (six
  colors). See the [Rue note](notes/2026-11-27-joie-rue-usability.md).
  The Mint Latch is "In Stock" at Target ($299.99; $379.99 with Base AR).
  See the [Mint Latch note](notes/2026-11-27-joie-mint-latch-usability.md).
  The Baby Safety Alliance question remains open.
  joiebaby.com now returns 403 to scripts.

- [ ] **32. Which Maxi-Cosi infant seats claim 213a?** Maxi-Cosi says 213a
  seats carry a "new SIP logo on packaging and product pages" but its
  product pages blocked scripted reads (429/403). Read them in a browser
  (Peri 180, Ambra, Mico Pro/Pro+).

- [ ] **33. Rotating seats: missing specs.** Not blocking since
  [0003](../decisions/0003-no-rotation-now-buy-for-the-long-run.md)
  (no rotating infant seat); kept for reference. Cybex Aton G2 Swivel base
  weight and size (Cybex does not publish them); Graco SnugRide Turn &
  Slide aircraft rule, 213a wording and how to tell the post-recall design
  from recalled units (campaign 26C003000), since gracobaby.com blocked
  scripts ([note](notes/2026-11-27-rotating-infant-car-seats.md)).

## Raised by decision 0003 (2026-11-27)

- [ ] **34. Is there a US base that carries both an infant seat and a
  next-stage seat?** In Europe some brands sell one base for both their
  infant carrier and their toddler seat. If a US system exists that meets
  0001 and rotates in the next stage, it would save buying a second base.
  Not researched; low priority.

- [ ] **35. Which rotating seats for the next stage meet 213a and fit the
  Model Y?** Required by
  [0003](../decisions/0003-no-rotation-now-buy-for-the-long-run.md):
  rotating convertible or all-in-one, preferably running to booster, with
  an expiry that covers the years it is meant for. Research when the infant
  seat is close to outgrown (item 27), not now.

## Raised by the usability review (2026-11-27)

- [x] **36. Re-check the Primo Viaggio Nido usability findings at their
  sources.** On 2026-11-27 Nick shared a summary written by another agent.
  It reports a recline indicator that cannot be trusted, poor insert fit,
  a lock-off that does not hold, and a click-in indicator that can show
  green when the carrier is not locked. It also reports a stiff buckle and
  an as-used carrier weight of 10.6–11 lb, against the maker's 8.2 lb. Its
  sources are BabyGearLab (2023, Nido 4-35), CSFTL and Consumer Reports.
  None of it has been re-read yet. Re-read each source, note which version
  it tested, and write a research note. No seat is shortlisted yet. Any
  seat considered needs the same usability pass (AGENTS.md rule 8).
  **Answered 2026-11-27:** see the
  [Primo Viaggio note](notes/2026-11-27-peg-perego-primo-viaggio-usability.md).
  Every review tested the 4-35 Nido; none tested the current 4-30. Click-in
  false green, insert fit, stiff buckle and the 10-11 lb carrier are
  confirmed for older versions. The lock-off finding is disputed. "Recline
  indicator cannot be trusted" is not supported as worded. Usability notes
  for the other seats are under `research/notes/` dated 2026-11-27.

- [x] **37. Does the Romer Juni pass decision 0001?** The same summary
  ranks it above the Nido. It was never in the market survey. Check its
  213a claim, its stroller range and its Model Y fit.
  **Answered 2026-11-27: no.** Its page and 01.26 manual claim only
  general FMVSS conformance. See the
  [Juni note](notes/2026-11-27-romer-juni-213a-gate.md). Re-check if a
  manual revision or label after 2026-12-05 adds a 213a claim.

## Raised by the infant seat shortlist (2026-11-27)

- [ ] **38. Which shortlisted infant seat do we buy?** Nick picks one of
  `uppababy-aria-v2`, `uppababy-mesa-v3` or `chicco-keyfit-30-cleartex`
  (see `docs/COMPARISON.md` and the usability notes of 2026-11-27). The
  agent leaned toward the Aria V2 for travel: the lightest carrier and a
  stable baseless install. The Mesa V3 offers a fallback baseless routing
  and a 32 in limit. The KeyFit 30 is cheapest and Model Y tested. Then
  write the ADR with the `adr-write` skill; its step 4 checks every "What
  to judge" row. Include carrier height on the stroller (item 28). After
  that, start the stroller search under 0003.
  Nick, 2026-11-28: resume Aria V2 research before choosing. Done the same
  day in three notes:
  [carrier-only install](notes/2026-11-28-uppababy-aria-v2-carrier-only-install.md),
  [hands-on and fit](notes/2026-11-28-uppababy-aria-v2-hands-on-and-fit-update.md),
  [stroller and Model Y](notes/2026-11-28-uppababy-aria-v2-on-stroller-and-model-y.md).
  Still no CPST hands-on V2 review, measured headrest height, ride height
  on a stroller or Model Y report.

## Raised by the Aria V2 follow-up (2026-11-28)

- [ ] **39. What does UPPAbaby advise when a shoulder belt will not wrap
  the Aria V2?** The V2 manual has no fallback routing, only "contact
  Customer Service". Also ask why V2 dropped the V1's other baseless
  methods, and whether "buckle after wrapping" is allowed. See the
  [install note](notes/2026-11-28-uppababy-aria-v2-carrier-only-install.md).

- [ ] **40. Recheck for a CPST hands-on Aria V2 review.** Safe in the Seat
  listed it as "Review Coming Soon" on 2026-11-24. Most V2 fit evidence is
  incentivized panel reviews. See the
  [fit update](notes/2026-11-28-uppababy-aria-v2-hands-on-and-fit-update.md).
