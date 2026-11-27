---
question: Does NHTSA still publish car seat Ease-of-Use ratings, how are they scored, and what are the ratings for the infant seats under consideration?
date: 2026-11-27
category: car-seat
confidence: high
candidates: []
---

# NHTSA Ease-of-Use ratings for the infant seats

## Question

Open question 26. Does NHTSA still publish its car seat Ease-of-Use
ratings? Can they be read for the seats that pass decision 0001 (UPPAbaby
Mesa V3 and Aria V2, Chicco KeyFit 30 ClearTex and KeyFit Max, Joie Rue and
Mint Latch, Peg Perego Primo Viaggio variants) and the Romer Juni? Is the
rated seat the version we would buy?

## Sources

All read 2026-11-27 by a `researcher` run.

- [NHTSA childSeats API, ratings](https://api.nhtsa.gov/childSeats?dataSet=ratings&max=100&offset=0)
  (and `offset=100`), plus single records such as
  `https://api.nhtsa.gov/childSeats/860937` — primary. Live: 130 rated
  records for seats made 2020-03-03 to 2026-03-01. It answered only with a
  full Chrome User-Agent.
- [NHTSA "Car Seat Ease-of-Use Ratings" page, Wayback snapshot 2026-10-30](http://web.archive.org/web/20261030054729/https://www.nhtsa.gov/car-seats-and-booster-seats/car-seat-ease-use-ratings) — primary, archived copy
- [NHTSA Ease-of-Use FAQ, May 2023, archived](https://web.archive.org/web/20260503032653id_/https://www.nhtsa.gov/sites/nhtsa.gov/files/2023-05/Ease-of-Use_FAQs_051123_v4_tag.pdf) — primary, archived copy
- [NHTSA Ease-of-Use Conditions of Use, 2023-05, archived](https://web.archive.org/web/20260328192935id_/https://www.nhtsa.gov/sites/nhtsa.gov/files/2023-05/Ease-of-Use-Ad-Guidelines_051123-v2-tag.pdf) — primary, archived copy
- [Federal Register 73 FR 6261, 2008-02-01, rating program final decision](https://www.federalregister.gov/documents/2008/02/01/08-451/consumer-information-rating-program-for-child-restraint-systems) — primary
- [Federal Register 2026-16735, 2026-08-17, NCAP notice](https://www.federalregister.gov/documents/2026/08/17/2026-16735/new-car-assessment-program-ncap-removal-of-dynamic-rollover-resistance-test-and-side-air-bag) — primary
- [Chicco KeyFit 30 ClearTex – Slate, item 00087002040070](https://www.chiccousa.com/shop-our-products/car-seats/infant/keyfit-30-cleartex-infant-car-seat---slate/00087002040070.html) — primary (maker)
- [Safe Ride News, study of NHTSA's ratings, 2023-10](https://www.saferidenews.com/2023/10/study-nhtsa-eou/) — independent (child passenger safety newsletter)

www.nhtsa.gov pages, one.nhtsa.gov and safercar.gov returned 403.
data.transportation.gov holds only links to a retired page (data last
updated 2018-12-17).

## Findings

### The program is current

- NHTSA's feed has ratings for seats made as late as 2026-03-01 (a Chicco
  KeyFit 30), and several made in late 2025.
- The feed has no rating-year or model-year field, only the manufacture
  date of the seat NHTSA evaluated.
- Every record has `"active": false`, which NHTSA does not explain.
- The 2026-08-17 notice: "the Agency is updating its Child Restraint System
  (CRS) Ease-of-Use rating program with proposed implementation in the
  fourth quarter of 2028".

### How it is scored

- Four categories per mode: Evaluation of Labels, Evaluation of
  Instructions, Securing the Child, Vehicle Installation Features. Each gets
  stars, plus an overall rating.
- "5 Stars = Excellent … 3 Stars = Average … 1 Star = Poor".
- **It is not a safety rating.** FAQ: "The ratings represent each child
  restraint's individual category rating as well as its overall rating for
  ease of use, not safety."
- The 2008 decision kept a weighted average adopted from ICBC, with break
  points "5 stars = Result >= 2.60 … 1 star = Result < 1.70." The
  per-question weights are printed as images and were not read.
- Re-ratings apply "only to seats manufactured on or after the re-rated
  seat's date of manufacture." The manufacture date matters.

### Ratings for our seats (rear-facing infant mode)

Stars are Overall / Securing the Child / Labels / Vehicle Installation /
Instructions.

| Seat | NHTSA record | Made | Stars | Same version? |
| --- | --- | --- | --- | --- |
| Chicco KeyFit 30 ClearTex | "Chicco KeyFit 30", 87002040070 | 2026-03-01 | **3** / 3 / **1** / 5 / 5 | **Yes.** Chicco lists item 00087002040070 as the KeyFit 30 ClearTex in Slate. |
| Joie Rue | "Joie Rue", I2320AASHA900 | 2024-08-09 | **4** / 3 / 5 / 4 / 5 | Name and limits match |
| Joie Mint Latch | "Joie Mint", C2304BAEVG900 | 2025-06-11 | **4** / 3 / 5 / 5 / 5 | Likely. The record's 9.0 lb weight and LATCH use fit the baseless Mint Latch (inference). |
| UPPAbaby Mesa V3 | not found; "Mesa V2", 1002-MSA-US-ALC | 2024-05-20 | V2: **5** / 5 / 5 / 5 / 5 | **No, older version** |
| UPPAbaby Aria V2 | not found | | | |
| Chicco KeyFit Max | not found | | | |
| Peg Perego Primo Viaggio (any) | not found; only Peg Perego boosters are rated | | | |
| Romer Juni | not found | | | |

NHTSA's notes, quoted:

- **KeyFit 30 ClearTex**, Labels 1 star: "Additional sizing info is
  missing. Must read text in order to route vehicle seatbelt properly.
  There is no indication of correct harness slot height given on the
  labeling. The labels do not contain LATCH preparation illustrations. The
  labels may not explain the use of the LATCH. The labels do not remind the
  user to tighten the LATCH." Securing the Child, 3 stars: "The harness
  must be rethreaded to adjust height for the child's growth as well as for
  reassembly after cleaning." Vehicle Installation: "There is no label
  showing where to put the car seat's carry handle during travel in the
  vehicle."
- **Joie Rue**, Securing the Child, 3 stars: "The harness chest clip is not
  labeled with instructions for proper placement. The harness must be
  rethreaded to adjust for the child's growth. Loose pieces are generated
  when adjusting for child growth." Instructions: "The manual cannot be
  accessed while the car seat is installed".
- **Joie Mint**, Securing the Child, 3 stars: "The harness must be
  rethreaded to adjust height for the child's growth as well as for
  reassembly after cleaning, and loose parts may be generated during these
  processes." Vehicle Installation: "A printed/molded line is present on
  the restraint that must be leveled to the ground."
- **Mesa V2**, Securing the Child, 5 stars: "The CRS was not set for the
  youngest mode when removed from the packaging." Instructions: "The
  illustration is small and in a sideview, making it unclear." The record
  gives the height range as "Up to 49.0\"", against "up to 32" in the mode
  line, which looks like a data-entry error.

## Confidence

- **High** that the program is current, and for the categories, star
  meanings and the four ratings found (NHTSA's own feed, matching the
  single-record copy).
- **High** that the KeyFit 30 rating is the ClearTex we would buy (maker's
  item number). **Medium** that "Joie Mint" is the Mint Latch.
- **Medium-high** for the scoring method: the 2008 decision is explicit,
  but changes since then are unknown.
- **Medium** that the missing seats are not in today's feed. **Low** that
  they were never rated: the feed covers only seats made from 2020, and
  older ratings (for example the Primo Viaggio 4-35, whose photo is on
  static.nhtsa.gov) may exist outside it.

## Candidate impact

Nothing yet: no seat is shortlisted. For any shortlisted seat:

- Record the NHTSA overall and category stars with the manufacture date
  rated, citing this note.
- The KeyFit 30 ClearTex's 1-star Labels rating supports a con starting
  "Misuse risk:" (no harness slot height label, no LATCH illustrations).
  It is a usability rating from a primary source, not a safety rating.
- The Rue's and Mint's 3-star Securing the Child supports the rethread
  harness con already found in their usability notes.
- For the Mesa V3, cite the V2 rating only as an older version.

## Open questions

- Ratings for seats made before 2020 are not in the feed. Next places: the
  regulations.gov docket NHTSA-2006-25344, and Wayback copies of the
  retired `nhtsa.gov/nhtsa_eou/info.jsp?type=all` page.
- A full `childSeats?dataSet=all` download failed partway with HTTP 500.
  A retry should save each page and retry on errors.
- Confirm "Joie Mint" C2304BAEVG900 is the Mint Latch.
