---
question: What are Delta's and American's carry-on size limits and their stroller and car seat rules?
date: 2026-11-27
category: general
confidence: medium
candidates: []
---

# Delta and American: carry-on size, strollers, car seats

## Question

For the two airlines we fly most, what is the carry-on size limit? Can a
stroller be checked free, gate-checked, or carried on board? What are the
rules for using a car seat on board?

## Sources

All accessed 2026-11-27.

**Delta** (primary: pages fetched and read directly):

- [Delta, Carry-on baggage](https://www.delta.com/us/en/baggage/carry-on-baggage)
- [Delta, Children & infant items](https://www.delta.com/us/en/baggage/special-items/children-infant-items)
- [Delta, Children & infant baggage](https://www.delta.com/us/en/children-infant-travel/children-infant-baggage)
- [Delta, Infant travel](https://www.delta.com/us/en/children-infant-travel/infant-travel)

**American** (secondary / unverified: every aa.com page returned HTTP 403
to the research tool, so these findings come from search-engine summaries of
the pages, not the pages themselves):

- [AA, Carry-on baggage](https://www.aa.com/i18n/travel-info/baggage/carry-on-baggage.jsp) — not fetchable
- [AA, Traveling with children](https://www.aa.com/web/i18n/travel-info/special-assistance/traveling-children.html) — not fetchable
- [AA, Conditions of carriage](https://www.aa.com/web/i18n/customer-service/support/conditions-of-carriage.html) — not fetchable
- [View from the Wing, 2025-08-04](https://viewfromthewing.com/american-airlines-now-allows-any-collapsible-stroller-onboard-free-heres-the-policy-to-show-gate-agents-who-say-no)
  — secondary (travel blog)

## Findings

### Delta (primary)

- **Carry-on size:** "Individual length, width and height measurements may
  not exceed 22" x 14" x 9" (56 cm x 35 cm x 23 cm) respectively."
  "Combined length + width + height of baggage must not exceed 45 linear
  inches (114 cm)." "These measurements include any handles or wheels."
- **Strollers and car seats are free** and do not count toward the
  baggage allowance: "we don't charge any fees for traveling with strollers
  or child-restraint seats". They "may be checked at the curbside, the
  ticket counter or at the gate."
- **On board:** "Special items like strollers, wheelchairs, child safety
  seats or assistive devices" are "free to carry on your flight, in addition
  to your usual carry-on items." No Delta page read states a size or
  weight limit for gate-checking, or says a stroller must fit the bin.
- **Car seat on board:** the infant-travel page says "To use a FAA-approved
  safety seat, you must purchase a ticket for your child". The baggage pages
  also allow use "if there is an open passenger seat in your row"; otherwise
  it is gate-checked. These two pages conflict.
- **Placement:** "The window seat is the preferred location". Avoid "Aisle
  seats," "Emergency exit rows," and "Bulkhead seats when the safety seat is
  a combination car seat and stroller." Children under 2 may not sit in a
  seat with an airbag seat belt, so no car seat in Delta One flatbeds on the
  A330-200/-300. "An accompanying adult must sit next to the child."
- **Onboard bassinets (SkyCots):** only on widebody flights (international,
  or domestic over 1,500 miles), for children "under 25lbs (11.3 kg) and up to
  26 inches (66 cm) long", two per aircraft, requested through Reservations.

### American (secondary / unverified)

- **Carry-on size:** 22 × 14 × 9 in, handles and wheels included. Personal
  item 18 × 14 × 8 in.
- **Strollers and car seats:** "Each ticketed customer is allowed 1
  stroller and 1 car seat to be checked free of charge when traveling with a
  child." Strollers and child safety seats do not count as a bag or
  personal item. Non-collapsible strollers, and wagons without built-in
  straps, go to the ticket counter.
- **Weight limit, unresolved:** one indexed conditions-of-carriage text
  says a carry-on stroller must be "fully collapsible", "under 20 lbs." and
  fit the overhead bin. View from the Wing (2025-08-04) reports that AA
  removed the weight limit in July 2025: "There is no longer any weight
  restriction on strollers." It reports that a collapsible stroller that fits
  carry-on size can go in the bin or closet, space permitting. It is unclear
  which text is live.
- **Car seat on board:** must be FAA-approved. Window seat preferred. Not in
  an exit row or the rows just in front of or behind an overwing exit. Needs
  a purchased or unoccupied adjoining seat, otherwise "the gate agent will
  check the safety seat to your final destination."

## Confidence

- **Delta: high.** Read directly from delta.com.
- **American: low to medium.** The carry-on figure matches Delta's and is
  widely repeated, but nothing was read from aa.com itself. The stroller
  weight rule has two conflicting versions.

Overall **medium**, until the American pages are read directly.

## Candidate impact

- `household.yaml` `travel.overhead_bin_in` = **[22, 14, 9]**. Both
  airlines share this carry-on limit (Delta confirmed; AA unverified). It is
  a carry-on bag limit, used here as the screen for "does the folded
  stroller go in the bin". Neither airline's pages confirmed here promise a
  stroller that size will be allowed in the bin.
- An overhead-bin "does not fit" is not a dealbreaker. Both airlines check
  strollers free at the gate, Delta confirmed.
- Stroller weight matters for American only if the 20 lb rule is still live.

## Open questions

- Read the American pages directly (in a browser): the live stroller weight
  rule, and whether a carry-on-size stroller may go in the bin.
- Delta: no stated gate-check size or weight limit, and no stated rule that a
  carry-on stroller must fit the bin. Ask Delta if it becomes decisive.
- To be sure the car seat is used on board, buy the baby a seat. Both
  airlines otherwise depend on an empty adjoining seat.
