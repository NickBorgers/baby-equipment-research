---
id: "0001"
title: Car seat must be certified to the FMVSS 213a side-impact standard
status: accepted
date: 2026-11-27
category: car-seat
candidates: []
---

# 0001 — Car seat must be certified to the FMVSS 213a side-impact standard

## Context

FMVSS 213 is the US federal standard for child car seats. Its long-standing
crash test is a frontal impact. NHTSA has added a side-impact requirement,
FMVSS 213a. Seats made after its compliance date must meet it. Seats made
before that date can still be sold without meeting it, so a seat on a shelf
may or may not be certified.

The exact compliance date, and what the label or manual says on a certified
seat, are not yet sourced in this repo (open question 14). The compliance
date may be very close to now. If so, few seats may have been tested and
labeled yet.

## Decision

Only consider car seats whose manufacturer states, in a primary source,
that the seat is certified to FMVSS 213a. The specific unit we buy must
carry that certification too: check its manufacture date and its label.

## Rationale

Nick's requirement (2026-11-27): "For the car seat I would like to be
looking for FMVSS 213a". Side impacts are a common, serious crash type, and
213a is the federal test for them. Buying a seat made before the rule, just
as it takes effect, would mean buying to an older standard than the one in
force.

## Alternatives considered

- **Accept any FMVSS 213 seat and treat side-impact testing as a bonus.**
  Rejected: this is the case the requirement exists to avoid.
- **Rely on manufacturers' own side-impact claims made before 213a.** Many
  seats have advertised in-house "side impact tested" claims for years.
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

- `research/open-questions.md` item 14: the 213a compliance date and what
  a certified label looks like, from NHTSA.
- Item 23: which infant seats are certified to 213a now, and how to verify
  a specific unit.
