---
question: Can four claims that had no source (in ADRs 0001-0003 and the Ridge V2 notes) be verified, and what do the sources actually say?
date: 2026-11-28
category: general
confidence: medium
candidates: [uppababy-ridge-v2, uppababy-aria-v2]
---

# Sources for four claims that had none

## Question

When every source got a link, four claims had none. The rule was to verify each one or remove it:

1. ADR 0001: "Side impacts are a common, serious crash type."
2. ADR 0002: "How well a small newborn fits also varies a lot between convertibles."
3. ADR 0003: the infant base and stroller adapters are "roughly $150-250 of parts".
4. Ridge V2 notes: "UPPAbaby says not to jog with an infant car seat attached."

## Sources

- [NHTSA FMVSS 213a final rule, 87 FR, 2022-06-30](https://www.govinfo.gov/content/pkg/FR-2022-06-30/html/2022-13658.htm)
  — primary. A `researcher` run read it with Firecrawl on 2026-11-28 and searched the preamble.
- [Car Seats For The Littles, "Choosing a Convertible Car Seat for a Newborn"](https://csftl.org/choosing-a-convertible-car-seat-for-a-newborn/)
  — independent (a group of child passenger safety technicians). Read 2026-11-28. The page has no date. Its images date from 2013-2018.
- [UPPAbaby Extra Aria Base](https://uppababy.com/accessories/car-seats-accessories/base-for-aria/)
  — primary (maker). Read 2026-11-28.
- [UPPAbaby Car Seat Adapters for Minu V3](https://uppababy.com/accessories/strollers-accessories/adapters-for-minu-v3/)
  — primary (maker). Read 2026-11-28.
- [UPPAbaby support: "Can I jog with an infant car seat on the Ridge?"](https://support.uppababy.com/hc/en-us/articles/4403595638039-Can-I-jog-with-an-infant-car-seat-on-the-Ridge)
  — primary (maker help center). Read 2026-11-28. Updated 2024-02-28.
- [UPPAbaby Ridge V2 US manual, 251216](https://back.prod.uppababy.com/media/6b/04/ab/1772548603/NA_1403-RDG-NA_RidgeV2Manual_251216.pdf)
  — primary. Searched for "jog", "run" and "car seat" on 2026-11-28.

## Findings

### 1. Side impacts (verified)

- The rule's preamble says: "Impacts to the side of a vehicle rank almost equal to frontal crashes as a source of occupant fatalities and serious injuries to children ages 0 to 12 years."
- It reports 213 deaths of children aged 0-12 who were restrained in child seats in the rear seat. Of these, "approximately 31 percent occurred in frontal crashes, 25 percent in side crashes, 22 percent in rollovers, and 19 percent in rear crashes."
- The data come from older studies (for example FARS 1995-2009). They are not current crash rates.
- "Common" is supported by these shares of child deaths, not by how often side crashes happen overall.

### 2. Newborn fit in convertibles (verified, older seat list)

- CSFTL: "not all convertible or multimode car seats are created equal when it comes to fitting a brand new baby."
- Some seats "will not fit a newborn or young infant". The main reason is lowest harness slots that sit too high for a newborn's torso (the page says about 7 in).
- The lowest slot height of the listed seats ranges from 5 in to 10 in.
- The seat list is older than the 2026 models. A current seat must be checked on its own.

### 3. Parts thrown away after the infant stage (corrected)

- The Extra Aria Base costs $229.99. It fits the Aria, Aria V2 and Mesa Max.
- Minu V3 adapters cost $39.99. The Ridge adapter ($39.99), the Zoe adapter ($55) and the Mockingbird adapter ($50) come from the [specs note](2026-11-28-uppababy-strollers-specs-and-gates.md) and the [other strollers note](2026-11-28-non-uppababy-strollers-for-aria-v2.md), not re-read today.
- Base plus adapter is $230-285 at list price. The old figure of $150-250 was too low.
- The base comes in the seat's box, so the real cost of discarding it is lower than the list price.

### 4. Jogging with a car seat on the Ridge (verified)

- The FAQ says: "No. You should not jog with an infant car seat attached to the Ridge. Jogging is intended for a child in the Ridge seat only."
- The FAQ does not say whether it covers the Ridge V1 or V2.
- The Ridge V2 manual does not say this. Page 22 says: "It is recommended to wait until the child is at least 6 months old to use this jogger for running or off-road use."

## Confidence

Medium overall. The quotes are high confidence: they come from sources read today. The NHTSA data are old. The CSFTL seat list is old and has no date. Three of the adapter prices were not re-read today.

## Candidate impact

- `uppababy-ridge-v2`: the jogging note now cites the FAQ.
- ADRs 0001, 0002 and 0003 now cite these sources. The decisions do not change. In 0003, the cost figure is corrected from $150-250 to $230-285.

## Open questions

- None new.
