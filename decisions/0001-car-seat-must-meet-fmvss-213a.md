---
id: "0001"
title: Car seat must be certified to the FMVSS 213a side-impact standard
status: accepted
date: 2026-11-27
category: car-seat
candidates: []
summary: >-
  Every car seat must have its maker's claim, in a primary source, that it
  is certified to [FMVSS 213a](https://www.ecfr.gov/current/title-49/part-571/section-571.213a), the federal side-impact test. The unit
  we buy must carry that certification too. NHTSA says side impacts [rank
  almost equal to frontal crashes](https://www.govinfo.gov/content/pkg/FR-2022-06-30/html/2022-13658.htm)
  as a cause of child deaths and serious injuries, and [seats made before the rule can still be sold
  without it](../research/notes/2026-11-27-fmvss-213a-status-and-infant-seats.md).
if_yours_differs:
  - >-
    If you accept seats without a 213a claim, many more seats qualify,
    including the rotating infant seats ruled out in
    [0003](0003-no-rotation-now-buy-for-the-long-run.md).
  - >-
    Many seats advertise their own ["side impact tested"](../research/notes/2026-11-27-fmvss-213a-status-and-infant-seats.md) claims. These
    are not the [federal test](https://www.ecfr.gov/current/title-49/part-571/section-571.213a).
---

# 0001 — Car seat must be certified to the FMVSS 213a side-impact standard

## Context

[FMVSS 213](https://www.ecfr.gov/current/title-49/part-571/section-571.213) is the US federal standard for child car seats. Its
long-standing crash test is a frontal impact. [NHTSA](https://www.govinfo.gov/content/pkg/FR-2022-06-30/html/2022-13658.htm) has added a
side-impact requirement, [FMVSS 213a](https://www.ecfr.gov/current/title-49/part-571/section-571.213a). Seats made after its compliance
date must meet it. Seats made before that date can still be sold without
meeting it, so a seat on a shelf may or may not be certified
([note](../research/notes/2026-11-27-fmvss-213a-status-and-infant-seats.md)).

The exact compliance date, and what the label or manual says on a certified
seat, are not yet sourced in this repo
([open question 14](../research/open-questions.md)). The compliance
date may be very close to now. If so, few seats may have been tested and
labeled yet.

## Decision

Only consider car seats whose manufacturer states, in a primary source,
that the seat is certified to FMVSS 213a. The specific unit we buy must
carry that certification too: check its manufacture date and its label.

## Rationale

Nick's requirement (2026-11-27): "For the car seat I would like to be
looking for FMVSS 213a". In
[NHTSA's words](https://www.govinfo.gov/content/pkg/FR-2022-06-30/html/2022-13658.htm),
side impacts "rank almost equal to frontal crashes as a source of occupant
fatalities and serious injuries to children ages 0 to 12 years". In the
rule's data, 25 percent of deaths among restrained children in the rear
seat were in side crashes (31 percent were frontal). The data come from
older studies, not current crash rates. [213a](https://www.ecfr.gov/current/title-49/part-571/section-571.213a) is the federal test for them. Buying a seat made before the rule, just
as it takes effect, would mean buying to an older standard than the one in
force.

## Alternatives considered

- **Accept any FMVSS 213 seat and treat side-impact testing as a bonus.**
  Rejected: this is the case the requirement exists to avoid.
- **Rely on manufacturers' own side-impact claims made before 213a.** Many
  seats have advertised in-house "side impact tested" claims for years
  ([note](../research/notes/2026-11-27-fmvss-213a-status-and-infant-seats.md)).
  These are not the federal test. They are not a substitute, but they can be
  noted as a con or pro with low weight.

## Consequences

- Each car seat candidate records "FMVSS 213a" in `safety.standards` only
  when a primary source says so. `docs/COMPARISON.md` shows a 213a column:
  `yes` when recorded, `?` otherwise. A `?` means "not found yet", not "fails".
- The choice may be small at first, and stock in stores may be older units
  made before the rule. The purchase has to check the specific unit.
- **If no suitable certified seat is available in time, raise it with Nick.
  Do not quietly relax this.** Nick expected this might happen
  ("we may be in a situation where the testing simply hasn't occurred").
  Any fallback gets its own ADR that supersedes this one, or amends it.
- This applies to the seat used in the car and on the plane alike.

## Open questions

- [`research/open-questions.md`](../research/open-questions.md) item 14: the 213a compliance date
  and what a certified label looks like, from NHTSA.
- Item 23: which infant seats are certified to 213a now, and how to verify
  a specific unit.
