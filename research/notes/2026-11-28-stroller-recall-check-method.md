---
question: How do we search CPSC recalls for a stroller so safety.checked_on means the same thing every time, and what does the search find for the current candidates?
date: 2026-11-28
category: stroller
confidence: medium
candidates: [uppababy-minu-v3, uppababy-kona, uppababy-cruz-v3, uppababy-vista-v3, uppababy-ridge-v2, mockingbird-travel-stroller, zoe-tour-v3, mockingbird-single-3]
---

# CPSC recall check for strollers: method and first results

## Question

Open question 17, CPSC side. What search makes a stroller's
`safety.checked_on` repeatable? And what does it find on 2026-11-28 for
the eight stroller candidates?

## Sources

- [CPSC Recalls API information](https://www.cpsc.gov/Recalls/CPSC-Recalls-Application-Program-Interface-API-Information)
  and the [Programmer's Guide v1.3](https://www.cpsc.gov/s3fs-public/RecallRetrievalWebServicesProgrammersGuide20171031.pdf)
  (2017-10-31) — primary, read 2026-11-28 by a `researcher` run.
- [CPSC Recalls API](https://www.saferproducts.gov/RestWebServices/Recall?format=json)
  — primary. Queried by the researcher and again by the main session,
  2026-11-28, with curl and a browser User-Agent.
- [cpsc.gov Recalls listing](https://www.cpsc.gov/Recalls) — primary, read
  with Firecrawl 2026-11-28 by the main session. curl gets 403.
- [CPSC recall 26-568, Joolz Aer2 adapters](https://www.cpsc.gov/Recalls/2026/Joolz-Recalls-Aer2-Car-Seat-Adapters-for-Strollers-Due-to-Risk-of-Serious-Injury-from-Fall-Hazard)
  — primary, read by the researcher.
- [NHTSA recall flat file](https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL_POST_2010.zip)
  — primary, read by the researcher.
- [SaferProducts.gov report 4843681](https://www.saferproducts.gov/PublicSearch/Result?id=4843681&handler=Detail)
  — retail/anecdotal (consumer report, published by CPSC, not verified),
  read by the researcher.
- [Health Canada recalls, "uppababy"](https://recalls-rappels.canada.ca/en/search/site?search_api_fulltext=uppababy)
  — primary, read by the researcher.

## Findings

### How the API behaves

The guide says the service does "a case insensitive search for any or all
of the following fields using a wildcard search". In practice:

- `Manufacturer=UPPAbaby` returns **0**. UPPAbaby is recorded as
  **Importer** ("Monahan Products LLC, d/b/a UPPAbaby"). `Importer=`,
  `RecallTitle=`, `ProductName=` and `RecallDescription=` return its 3
  recalls.
- `ProductType=Strollers` returns 111 but misses the 2022 Ridge recall
  and the 2026 Joolz adapter recall, whose type field is blank.
- `ProductModel=` is blank in UPPAbaby records.
- Short brand words match unrelated text: "Zoe" matches "Zoeller",
  "Zoetop" and "Flowers By Zoe"; model words like "Cruz" and "Kona" match
  bicycle makers. Filter hits by reading the title.
- The API lags the website. On 2026-11-28 its newest recall was dated
  2026-11-19; cpsc.gov listed recalls dated 2026-11-25.
- One record (26569) carries a Joolz title with another firm's
  description, so read the recall page for any hit that matters.

### Who holds adapter recalls

Stroller-side car seat adapter recalls are at CPSC: Joolz Aer2 (26-568,
2026-06-18), Thule Sleek (2020), Joovy (2013), Bugaboo (2011). NHTSA's
flat file has car seats sold in travel systems, but no stroller adapter.
Inference: a travel system needs both searches. No primary page states
the split in words.

### The method

1. API, brand. Query the brand in `RecallTitle`, `RecallDescription`,
   `ProductName`, `Manufacturer`, `Importer` and `Distributor`, and take
   the union by `RecallNumber`:
   ```
   UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
   for f in RecallTitle RecallDescription ProductName Manufacturer Importer Distributor; do
     curl -sL -m 120 -A "$UA" "https://www.saferproducts.gov/RestWebServices/Recall?format=json&$f=<Brand>"
   done
   ```
2. API, model. Repeat with `RecallTitle`, `RecallDescription` and
   `ProductName` for each model word, and keep hits that name the brand.
3. Recent gap. Read https://www.cpsc.gov/Recalls with Firecrawl and check
   every listing newer than the API's newest `RecallDate`.
4. Car seat side. Run the NHTSA flat-file search for the paired seat (see
   the [market survey](2026-11-27-infant-car-seat-market-survey.md)).
5. Record the date, the API's newest `RecallDate`, and each hit's number
   and URL. Incident reports are anecdotal and go in notes, not
   `recalls`.

### Results, 2026-11-28

Brands queried: UPPAbaby, Mockingbird, Zoe. Models: Minu, Vista, Cruz,
Kona, Ridge. API newest `RecallDate`: 2026-11-19. cpsc.gov listings dated
2026-11-19 to 2026-11-25: none is a stroller or stroller accessory.

| No. | Date | Brand | What | Current candidate affected? |
| --- | --- | --- | --- | --- |
| [15-196](https://www.cpsc.gov/Recalls/2015/UPPAbaby-Recalls-Strollers-and-RumbleSeats) | 2015-07-23 | UPPAbaby | 2015 Cruz, 2015 Vista and RumbleSeat bumper bar foam, choking hazard | no (2015 models) |
| [21-158](https://www.cpsc.gov/Recalls/2021/UPPAbaby-Recalls-Adapters-Included-with-RumbleSeats-Due-to-Child-Fall-Hazard) | 2021-06-30 | UPPAbaby | RumbleSeat adapters made Sept 2014 to July 2019 can detach | no |
| [22-215](https://www.cpsc.gov/Recalls/2022/UPPAbaby-Recalls-RIDGE-Jogging-Strollers-Due-to-Fingertip-Amputation-Hazard-One-Injury-to-Child-Reported) | 2022-09-01 | UPPAbaby | Ridge (V1) rear disc brake openings, fingertip amputation | no; Ridge V2 not named |
| [23-042](https://www.cpsc.gov/Recalls/2023/Mockingbird-Recalls-Single-to-Double-Strollers-Due-to-Fall-Hazard) | 2022-11-10 | Mockingbird | Single-to-Double, lots 20091-22602: "The lower side of the stroller frame can crack"; about 149,000 units; frame reinforcement kit | no (older lots); same maker as two candidates |
| [23-161](https://www.cpsc.gov/Recalls/2023/Mockingbird-Expands-Recall-to-Include-Single-Strollers-Due-to-Fall-Hazard) | 2023-03-17 | Mockingbird | Single, lots 18322-22278, 23174 and 23175: same frame crack; about 25,390 units | no (older lots; inference that the 3.0 is outside them, from lot numbers only) |

No Zoe stroller recall was found. The "Zoe" hits were unrelated firms.

Health Canada lists one UPPAbaby consumer recall: the same Ridge recall.

### Also found: one incident report (anecdotal)

SaferProducts.gov report published 2024-08-19: a Minu **V2** with
UPPAbaby adapter clips for a Mesa released the car seat going downhill;
"the entire car seat … unclipped from the stroller base and … landed upside
down on the pavement". The 3-month-old was not injured; UPPAbaby replaced
the items. One unverified report, on the older Minu, with a different
seat. It bears on open question 28 and on lifting the carrier to check
the latch (ADR 0004).

## Confidence

- **High** for each recall listed (API, CSV and recall pages agree).
- **Medium** that the API search is complete: results depend on the
  field, the API lags the website, and one record is mislabelled. Step 3
  covers the lag.
- **Medium** for the CPSC/NHTSA split for adapters (inferred from
  records).
- **Low** for the incident report.

## Candidate impact

For all eight stroller candidates: `safety.checked_on: "2026-11-28"`,
`recalls: []`. None of the recalls names a current model. Add the
method's note to each item's `research_notes`. On both Mockingbird items,
add a con about the 2022-23 frame-crack recalls of earlier Mockingbird
strollers. On `uppababy-minu-v3`, note the single Minu V2 adapter release
report.

## Open questions

- Is the API-plus-website search accepted as equal to CPSC's own
  per-product lookup? The same question is open for NHTSA's flat file.
- Is the Mockingbird Single 3.0 a redesigned frame, or the same frame with
  the reinforcement? Ask Mockingbird or read its 3.0 pages.
