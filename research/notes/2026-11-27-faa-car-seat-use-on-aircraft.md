---
question: What makes an infant car seat usable on a US airliner, and how is it installed there?
date: 2026-11-27
category: car-seat
confidence: high
candidates: []
---

# Using an infant car seat on a US airliner

## Question

What label makes a car seat approved for aircraft? Does the baby need their
own seat? Where can the car seat go? Can a rear-facing infant carrier be
installed without its base? How wide is too wide? Must the airline allow it?

## Sources

All accessed 2026-11-27. All primary unless marked.

- [49 CFR 571.213 (FMVSS 213), S5.5.2(n), S8](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-571/subpart-B/section-571.213)
  — primary (read via the eCFR API, current through 2026-11-24)
- [49 CFR 571.213b, S5.5.2(n)](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-571/subpart-B/section-571.213b) — primary
- [14 CFR 121.311](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-G/part-121/subpart-K/section-121.311) — primary
- [FAA AC 120-87C, Use of Child Restraint Systems on Aircraft](https://www.faa.gov/documentlibrary/media/advisory_circular/ac_120-87c.pdf)
  — primary. Dated 2015-09-24, listed "Active". No 120-87D was found.
- [FAA InFO 15013](https://www.faa.gov/sites/faa.gov/files/other_visit/aviation_industry/airline_operators/airline_safety/InFO15013.pdf) — primary
- [FAA, About Child Restraint Systems](https://www.faa.gov/travelers/fly_children/about-child-restraint-systems)
  — primary, page updated 2026-11-06
- [FAA, Child Safety in Flight](https://www.faa.gov/travelers/kids-corner) — primary
- [FAA child safety seat tips (PDF)](https://www.faa.gov/travelers/fly_children/child_safety_seat_tips) — primary
- [FAA final rule 80 FR 58575 (2015), seat dimension disclosure](https://www.federalregister.gov/documents/2015/09/30/2015-24720/disclosure-of-seat-dimensions-to-facilitate-use-of-child-safety-seats-on-airplanes-during) — primary
- [UPPAbaby Mesa V3 US manual, rev. 251226, p. 47](https://back.prod.uppababy.com/media/eb/4b/cc/1767623777/US-EN_1003-MSA_MesaV3Manual_251226.pdf) — primary (manufacturer)
- [Chicco KeyFit Max manual, pp. 82-85](https://www.chiccousa.com/on/demandware.static/-/Sites-Chicco-Library/default/dw5fa7ba15/manuals/car-seats/Chicco-KeyFit-Max-Infant-Car-Seat-Manual.pdf) — primary (manufacturer)

## Findings

**The label.** FMVSS 213 S5.5.2(n): a seat certified for aircraft "shall be
labeled with the statement 'This Restraint is Certified for Use in Motor
Vehicles and Aircraft'", in red lettering. 14 CFR 121.311(b)(2)(ii)(B)
requires that label, plus the general FMVSS conformance label, for a US seat
to be used on board. FMVSS 213b, which replaces 213 for seats made on or
after 2026-12-05, keeps the same aircraft label wording. If the label is
worn, a manufacturer letter or the owner's manual is acceptable proof
(AC 120-87C para 12b).

**Own seat.** Lap infants under 2 are legal (121.311(b)(1)). But the FAA
says "The safest place for your child under the age of two on a U.S.
airplane is in an approved child restraint system (CRS) … not in your lap",
and "Purchasing a ticket for your child under two is the only way to
guarantee that your child can be secured in a CRS". Airlines may, but need
not, let an unticketed child use an empty seat (AC 120-87C para 10d).

**The airline must allow it if a seat is bought.** 121.311(c)(2): no airline
may prohibit a ticketed child from using an approved, properly secured CRS.
AC 120-87C para 10f: if it does not fit one seat, the airline "has the
responsibility to accommodate the CRS in another seat in the same class of
service."

**Placement.** FAA tip sheet: "Car seats generally must be installed in a
window seat, cannot be placed in an exit row, and must not block an escape
path". It must be on a forward-facing aircraft seat (121.311(b)(2)(iii)(A)).
"CRSs should not be placed in an aisle seat" (AC 120-87C para 19a). If the
aircraft seat has an inflatable seat belt, the AC says to use a belt
extender. The UPPAbaby Mesa V3 manual instead says inflatable belts "are not
compatible", so the seat's own manual decides.

**Without the base.** FAA InFO 15013: if a rear-facing carrier has a belt
path and the right label, "it does not need to be used with the detachable
base on aircraft"; with no belt path, it must use the base. Manufacturers'
instructions govern, and they differ:

- UPPAbaby Mesa V3: "DO NOT use base with aircraft installation. Only the
  carrier is certified for aircraft use." It is installed with the lap belt
  through the carrier.
- Chicco KeyFit Max: "This Child Restraint is certified for use on
  aircraft." The aircraft steps route the lap belt through the carrier's own
  belt guide. The manual does not state a ban on the base outright.

**Width.** In its 2015 rule, the FAA restated its earlier advice that "a CRS
with a maximum width of 16 inches should fit in most airplane seats". The
original FAA page is gone, and current FAA consumer pages do not repeat the
figure. Airlines must publish the narrowest and widest seat width (between
the armrests) for each aircraft type and class (121.311(k)). A seat too wide
for rigid armrests can be moved to a seat with movable armrests (AC 120-87C
para 10f(1)).

**Not allowed for a newborn.** Belly belts, vests and harnesses that attach
the child to the parent, and booster seats are banned during taxi, takeoff
and landing (121.311(c)(1); AC 120-87C para 15d). The one approved harness,
CARES, is only for children of 22-44 lb.

## Confidence

**High** for the regulation text, the AC and the FAA pages, all read
directly. Only two manufacturers' manuals were checked. Every other infant
seat needs its own manual read before its aircraft install method is
recorded. The 16 in width figure is **medium**: it is the FAA's own words,
but from 2015, and it is no longer on a current page.

An FAA report from November 2025 on CRS fit in aircraft seats (DOT/FAA/AM-25/54)
could not be downloaded. A search summary (secondary, unverified) says
width was the main fit problem.

## Candidate impact

- `specs.faa_approved: true` on a car seat means the seat carries the red
  "Certified for Use in Motor Vehicles and Aircraft" label, confirmed in the
  manufacturer's manual or label image.
- The schema gains two car seat specs: `aircraft_install`
  (e.g. "carrier only, no base") and `carrier_width_in`, so the widest point
  of the carrier can be compared with the 16 in guide and airline seat widths.
- No candidates yet, so nothing else changes.

## Open questions

- For each candidate: its aircraft install method (base or no base), its
  carrier width, and whether inflatable seat belts are allowed. All from
  the manual.
- Delta and American publish seat widths for each aircraft type. Look these
  up once a seat is shortlisted, and note regional jets in particular.
