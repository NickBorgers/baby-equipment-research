---
question: Do three leading infant seats fit a 2022 Model Y, and does its rear footwell suit a load leg?
date: 2026-11-27
category: car-seat
confidence: low
candidates: []
---

# Model Y fit for three leading infant seats, and the load leg

## Question

Is there an independent fit test, or several agreeing owner reports, for
the Peg Perego Primo Viaggio or the UPPAbaby Mesa V3 in a 2020-2023 (pre-refresh)
Model Y? Can the Primo Viaggio Nido's load leg be used in the second-row
footwell? Is a per-seat rear cushion width published? The KeyFit 30 already
has a Cars.com test
([survey](2026-11-27-infant-car-seat-market-survey.md)).

## Sources

All read 2026-11-27. tesla.com (owner's manuals and Child Safety Seats
pages) and edmunds.com returned 403. Reddit and web.archive.org could not
be reached. So the Tesla quotes come from third-party copies of the manual
and from Tesla's service site.

- [Tesla Model Y Owner's Manual, software 2022.16, Japan edition, p.41 (ManualsLib copy)](https://www.manualslib.com/manual/2602707/Tesla-Y-2019.html?page=41)
  — primary (copy hosted by a third party), accessed 2026-11-27
- Tesla service manual,
  [Carpet - Rear (Remove and Replace)](https://service.tesla.com/docs/ModelY/ServiceManual/en-us/GUID-1BCE9B7D-7057-4D91-B5AF-F1C3A106AAD1.html)
  and
  [Carpet - Interior Complete](https://service.tesla.com/docs/ModelY/ServiceManual/en-us/GUID-88684476-C1AC-4021-BC70-46A071AEB18A.html)
  — primary, accessed 2026-11-27
- [Tesla Model Y underseat storage tray](https://shop.tesla.com/product/model-y-underseat-storage-tray)
  — primary, accessed 2026-11-27
- [Peg Perego Primo Viaggio 4-35 Lounge base owner's manual, FIUS2001I312](https://cdn.shopify.com/s/files/1/2691/4518/files/Primo_Viaggio_4-35_Lounge_Owners_Manual_-_Infant_Car_Seat_Base.pdf)
  — primary, but an older base than the current Nido; accessed 2026-11-27
- [The Car Seat Lady, load leg page](https://thecarseatlady.com/loadleg/)
  — independent (child passenger safety technician), undated, accessed 2026-11-27
- [Tesla Motors Club, "Rear facing infant car seat, Model Y", 2021](https://teslamotorsclub.com/tmc/threads/rear-facing-infant-car-seat-model-y.223565/)
  — anecdotal, accessed 2026-11-27

## Findings

### Fit tests

- **No independent fit test** was found for the Primo Viaggio or the Mesa
  (any version) in a Model Y. Cars.com tested only the KeyFit 30. IIHS
  rates LATCH hardware, not seat fit. The Car Seats for the Littles and
  The Car Seat Lady sites have no Model Y review.
- **Mesa: one owner report.** On Tesla Motors Club, 2021-07-28, a poster
  with a Mesa (version not stated) rear-facing behind the passenger seat
  wrote: "I'm comfortable enough in the passenger seat with the car seat
  behind me." No height or seat position was given.
- **Primo Viaggio: nothing** for a Model Y.
- No source gives how much front legroom is left with any of the three
  seats installed.

### Load leg

- **Tesla allows support legs, per one pre-refresh manual.** The 2022.16
  Japan edition, p.41: "All passenger seats Model Y support the use of a
  child restraint system with a safety leg." No US edition was readable.
  The US 2022.40 manual read earlier says nothing about support legs.
  Search snippets show similar "Safety Leg" wording on Tesla's Australia
  and Taiwan pages, but those pages could not be opened. So the model year
  they cover is unknown.
- **No sign of a hollow floor or storage bin in the second-row
  footwell.** Tesla's service steps for removing the rear carpet list only
  clips, the floor mat and the carpet. They mention no lid or opening
  panel. Tesla's underseat tray is a loose bin under the front seats. It is
  not a floor compartment. This is an absence of evidence, not a
  statement from Tesla.
- **Peg Perego's rule** (Lounge base manual, older than the current Nido
  base): p.6, "If your vehicle has a floor panel that is designed to
  fold/open, please check your Owner's Vehicle Manual to see if a load leg
  is allowed." p.5, "Do not use the load leg if the adjustable foot is not
  in contact with the vehicle floor" and "The car seat is certified for
  use with and without the load leg."
- Hollow floors are the usual reason a load leg is not allowed. The Car
  Seat Lady's example is minivans with Stow 'n Go seats. She does not
  mention Tesla.

### Rear seat width

- Tesla publishes no per-seat cushion width. The only figure remains the
  single 2020 measurement of about 18 in per outboard seat (low
  confidence; see the
  [Model Y note](2026-11-27-model-y-2022-cargo-and-rear-seat.md)).
- Rear hip room 50.6 in and rear shoulder room 54.0 in (5-seat), already
  in that note.

## Confidence

- **Low** for fit. There is no independent test for the Primo Viaggio or
  the Mesa. There is one forum post for the Mesa.
- **Medium** for the load leg being allowed. The Tesla wording is primary
  and clear, but it is the Japan edition of the same car. No US edition was
  readable. The "no floor compartment" finding rests on what the service
  manual does not mention.
- **High** for the Peg Perego wording, but it is from an older base manual.
  The current Nido base manual could not be fetched.

## Candidate impact

- No candidates exist yet.
- A load leg is fine in our car. Tesla's manual for the same pre-refresh
  car allows support legs. Nick confirmed on 2026-11-27 that the floor is a
  solid plate over the battery.
- `household.yaml` `rear_seat_width_in` stays `null`. Nick needs to measure
  it (open question 4).

## Open questions

- Confirm the support-leg wording in a North American Model Y manual.
  Read tesla.com in a browser.
- Read the current Primo Viaggio Nido base manual for its floor-panel
  wording.
- A test install of each shortlisted seat in our car would settle fit and
  front legroom. Many baby stores allow this.
- Tape-measure the outboard rear seat (open question 4).
