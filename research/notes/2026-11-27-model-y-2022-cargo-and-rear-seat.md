---
question: What are the 2022 Tesla Model Y's usable trunk, frunk and rear-seat dimensions, and where are its LATCH anchors?
date: 2026-11-27
category: general
confidence: medium
candidates: []
---

# 2022 Tesla Model Y: cargo space, rear seat, LATCH

## Question

How big is the usable rear trunk, under-floor well and frunk of a 2022
(pre-2025-refresh) Model Y, in inches? How wide is the rear seat, and which
positions have LATCH anchors? These are needed for the stroller trunk check
and the car seat back-seat check.

## Sources

All accessed 2026-11-27.

- Tesla Model Y Owner's Manual, software 2022.40, North America — primary
  (manufacturer). tesla.com returned 403, so a third-party-hosted copy of
  Tesla's PDF was used:
  [PDF copy](https://s7abe6bda7f063e33.jimcontent.com/download/version/1670926725/module/13256642149/name/Tesla%20Model%20Y%20'21%20Owner's%20Manual.pdf).
  Official current version (2020-2024 Model Y):
  [tesla.com manual](https://www.tesla.com/ownersmanual/2020_2024_modely/en_us/Owners_Manual.pdf)
- [xautoworld, Tesla Raj tape-measure review, 2020-03-16](https://xautoworld.com/news/model-y-measuring-tape-review/)
  — independent measurement (2020 Model Y Performance)
- [Tesmanian blog, 2020-04-11](https://www.tesmanian.com/blogs/tesmanian-blog/tesla-model-y-interior-trunk-trunk-well-frunk-and-other-measurements)
  — independent measurement (2020 Model Y Performance). Its labels are in
  diagrams. What each one measures was read from the arrows, not the text.
- Tesla Motors Club forum posts — anecdotal owner measurements:
  [dog cage thread, 2021](https://teslamotorsclub.com/tmc/threads/dog-cage-in-model-y.221329/),
  [box height thread, 2022](https://teslamotorsclub.com/tmc/threads/how-tall-a-box-will-fit-in-a-y.259740/),
  [cargo vs Outback, 2020](https://teslamotorsclub.com/tmc/threads/my-new-tesla-model-y-has-30-more-usable-cargo-space-than-my-2018-subaru-outback.199034/),
  [frunk organizer, 2021](https://teslamotorsclub.com/tmc/threads/nice-frunk-trunk-organizer-option.234487/)
- [IIHS LATCH rating, Model Y 2022](https://www.iihs.org/ratings/vehicle/tesla/model-y-4-door-suv/2022)
  — independent testing
- [Cars.com Car Seat Check, 2021 Model Y, 2022-02-02](https://www.cars.com/articles/how-do-car-seats-fit-in-a-2021-tesla-model-y-436721/)
  — independent testing

## Findings

**Tesla publishes no cargo dimensions in inches**, only volumes. From the
2022.40 manual (5-seat): frunk 4.1 cu ft; behind the second row 30.2 cu ft;
second row folded 72.1 cu ft.

**Rear trunk, seats up: independent measurements** (all on 2020-21 cars of
the same pre-refresh body; listed as reported, not averaged):

| Measurement | Values reported |
| --- | --- |
| Floor length | 40 (TMC) / 42.5 (Tesmanian) / 43 (Tesla Raj) / 43.5 (TMC) in |
| Width, narrowest or unspecified | 35.75 (TMC) / 37 (Tesla Raj, Tesmanian) / 37.5 (TMC) in |
| Hatch opening height, center | 27 / 27.25 / 27.6 in |
| Hatch opening height, edges | 25.5 in |
| Floor to top of rear seat (about cargo-cover height) | 19 in (TMC, "±5%") |

One owner's 36 × 22.5 × 25 in dog crate did **not** fit behind the rear
seats. The liftgate lip and the reclined seatbacks cost space, so a box
check against these figures is generous.

**Under-floor well (sub-trunk)**, from the Tesmanian diagram: bottom about
23.6 × 13.8 in, top opening about 31.5 × 18.5 in. Depth is about 13.8 in, or
15-16 in by a TMC owner's estimate. The well floor is partitioned, not flat.
Manual load limit: 88 lb in the lower tub.

**Frunk:** about 28 × 14 × 11 in (owner tape measure, June 2021 build). The
Tesmanian diagram gives a 27.6 × 13.8 in floor and a 35.8 × 16.9 in top
opening.

**Rear seat (manual, 5-seat):** shoulder room 54 in, hip room 50.6 in. Tesla
gives no width per seating position. The only figure is Tesla Raj's 18 in for
each outboard seat and 12 in for the center seat (one source).

**LATCH (manual pp. 37-38):** "Lower LATCH anchors are provided in the
second row outboard seats." "In the second row, install LATCH child safety
seats in the outboard seating positions only. Use only a seat belt retained
seat in the center position." The center seat has a top tether anchor. Do
not use the lower anchors once child plus seat weigh more than 65 lb. IIHS
rates LATCH ease of use "Acceptable" (2020-25).

**Car seat fit testing (Cars.com, 2021 Model Y):** a Chicco KeyFit 30
infant seat got an A and "fit easily behind the front passenger seat". A
Graco Contender rear-facing convertible "just barely fit". Three car seats
across: no.

## Confidence

**Medium.** The cargo volumes and LATCH facts are primary (Tesla's manual,
read from a hosted copy of the 2022.40 PDF). The inch measurements are all
independent, from 2020-21 cars, and disagree by 2-3 in. No source measured a
2022 car specifically, though the body is the same. The per-seat width
(18 in) is **low**: one source.

## Candidate impact

- `household.yaml` `vehicles[0].trunk_in` = **[40, 35.75, 19]**: the
  smallest reported floor length, width, and floor-to-seat-top height. These
  are deliberately conservative. They are a stand-in for a tape measure, not
  a substitute, and get replaced when the car is measured.
- `vehicles[0].frunk_in` = **[27.6, 13.8, 11]**: the smaller floor figures
  and the owner-measured depth.
- `vehicles[0].rear_seat_width_in` stays **null**. One 2020 YouTuber
  measurement is not enough to screen car seats against. The LATCH facts go
  in the vehicle's `notes`.

## Open questions

- Tape-measure our car (item 3): floor length, width between the wheel
  wells, height to the cargo cover, the hatch opening, and the sub-trunk.
- Rear-seat width at each outboard position (item 4).
