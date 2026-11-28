# Working in this repo

[`README.md`](README.md) describes the project and maps the directories. Read it
first; this file only covers how to work here.

This is a **research repo**, not a software project. The deliverable is a set
of decisions good enough to buy baby gear from. Most of the work is research:
finding real specs, safety facts and prices, and writing down where they came
from.

## The rules

**1. Research before data.** A number, pro, con or safety claim that lands in
`candidates/items/*.yaml` should have a note under `research/notes/` saying
where it came from, with a URL and the date read. No note, no number.

Model memory is not a source. Nick trusts an agent's reasoning, not what a
language model remembers about products, prices, standards or companies.
Every fact must come from a source read during the work. Memory may
suggest where to look. It never fills a gap. These rules also apply:

- A search snippet is not a read. Open the page, or label the fact
  "snippet only" with low confidence.
- A summary from another agent or a chat is retail/anecdotal. Re-read
  each fact at its source before it goes in a note.
- When you turn a `researcher` report into a note, add no fact that the
  report does not source.

Use the `researcher` agent (`.claude/agents/researcher.md`) for lookups.
It carries these rules.

**2. Unknown is `null`, never a pass.** A `null` means "not researched yet".
The fit check reports it as *insufficient data*, never as *fits*. Never fill a
`null` with a plausible guess to make a check pass — that is exactly the
mistake the tooling exists to prevent. If a guess is genuinely useful, write
it in a research note with `confidence: low` and say so in the item's `notes`.

**3. Decisions go in `decisions/`.** Anything that shapes what gets bought
gets an ADR. Never edit an accepted ADR to say something different: write a
new one, mark the old `superseded-by-NNNN`, and repoint the affected
candidates. `make check` fails if a candidate still points at a superseded
ADR.

**4. Never hand-edit `docs/`.** Those files are generated. Edit the YAML, run
`make docs`, commit both.

**4a. Every candidate has a product page.** `make docs` writes one to
`docs/products/<id>.md` from the item's YAML. The page links the notes
named in the item's `research_notes` list. When you add or change a
candidate, list every note behind it there. When a new note affects a
candidate, add the note's filename to that list. Then run `make docs`. A
`summary` field (2-4 plain sentences) goes at the top of the page. Leave it
out until the research supports one.

**5. Run `make check` before you finish.** It lints, validates the data,
confirms the generated docs are current, and runs the tests. If it fails, the
work is not done.

**6. Record what you could not answer.** Anything you hit and could not
resolve goes in [`research/open-questions.md`](research/open-questions.md).
That file is the backlog; an unknown that is not written there gets
rediscovered the expensive way.

**7. Do not reopen settled decisions casually.** Once an ADR is accepted, it
was made deliberately, after comparing real alternatives. Arguing with one
needs a real reason (new evidence such as a recall or a new model year, not a
stylistic preference) and gets raised with Nick rather than reversed
unilaterally.

**8. Judge how a product is used, not only what it is.** Specs, safety
claims and compatibility say what a product is. They do not say whether it
is easy to use correctly every day. Before you recommend or select a
product, research usability for every candidate you put forward and for
the ones it beats. Use the "What to judge" list in its category README and
the method under "Usability research" below. This applies to any
recommendation, including one made in chat or in a summary, not only to an
ADR. A shortlist built from specs alone is a shortlist, not a
recommendation.

**9. Every recommendation lists what was not researched.** End each
recommendation with a short list of:

- the "What to judge" rows it did not cover, and
- any evidence that came from a different model year or variant than the
  one you would buy.

Name each gap, even when it seems minor. Nick decides whether a gap
matters. An unstated gap reads as "checked".

## Usability research

Usability evidence comes from people who used the product by hand. These
rules say how to find it and weigh it.

- **Misuse risk is a safety issue.** A feature that is hard to set
  correctly can cancel its own crash benefit. Examples: a recline
  indicator that cannot be trusted, or a "locked" indicator that shows
  locked when the part is not. Start such a con with "Misuse risk:". A
  review can support a misuse-risk con. It cannot support a standard,
  recall, expiry or safe-sleep claim (see "Safety claims need a primary
  source" below).
- **Use the right sources, in this order:**
  1. NHTSA ease-of-use ratings, for car seats. Not yet verified as
     available or readable; see open question 26.
  2. Hands-on reviews by child passenger safety technicians (CPSTs). The
     best ones test with real babies or weighted dolls at several ages.
  3. Lab reviews with a published scoring method. Each lab scores
     differently, so never compare scores across labs.
  4. Owner reports and forums.

  Retailer write-ups are not hands-on reviews, even when they sound like
  them. Confidence levels are under "Reviews are medium confidence at best"
  below.
- **Match the review to the version you would buy.** Reviews often test an
  older model year or variant. Record which version each review tested. A
  finding from a different version is low confidence until a newer review
  repeats it. Look for retests.
- **Follow shared parts across variants.** Variants often share a base,
  frame or insert. A problem in a shared part carries over. To answer "does
  variant X fix it?", go part by part, and say which parts are shared.
- **Check where each feature works.** A feature may work in one mode only,
  for example in the stroller but not in the car. Say where it works.
- **Record numbers as the product is used.** Makers often quote weight
  without the canopy or inserts. Record the measured, as-used figure with
  its source. Never let the maker's lighter figure decide a comparison.
- **Write down where the maker disagrees with its manual.** A maker may
  tell a reviewer something its manual does not say. The manual is what a
  tired parent reads.
- **Alternatives a review suggests must pass the hard gates first.** A
  review's "better" picks are not candidates until they pass the accepted
  ADRs. For example, the Nuna PIPA RX has no 213a claim, so it fails 0001
  ([survey](research/notes/2026-11-27-infant-car-seat-market-survey.md)).
  If a suggested product was never surveyed, add it to
  `research/open-questions.md` to check against the gates.

## Rules specific to baby gear

- **Safety claims need a primary source.** Standards met, recalls, car seat
  expiry and crash-replacement rules, and safe-sleep claims come from NHTSA,
  CPSC, the published standard, AAP, or the manufacturer's own manual. A
  retailer listing or a review is not enough for a safety claim.
- **Recalls are dated.** Record the date the recall databases were searched
  in `safety.checked_on`. A recall check from months ago is not a current
  one. Every recall entry needs a URL.
- **Model years matter.** Strollers and car seats change between model years
  (weight, fold, compatibility, even the standard they meet). Say which model
  year a spec is for.
- **Reviews are medium confidence at best.** Independent lab testing is
  medium. User reviews and forums are low unless several agree.
- **Household facts are the household's to supply.** Car models, trunk and
  doorway measurements, bedroom space and budget belong to Nick.
  Ask; do not assume. They live in `household/household.yaml`, and every
  `null` there has an entry in the backlog.
- **Keep private details out of the repo.** The due date and similar
  personal facts are not recorded anywhere here, by Nick's choice. They are
  not needed; do not ask for them or add fields for them.
- **Compatibility comes from the manufacturer.** Car seat ↔ stroller
  compatibility and adapters go in a stroller's `compat` block only when a
  manufacturer's chart or manual says so. "Not listed" means unknown, not
  incompatible.

## Where things go

| You have | It goes in |
| --- | --- |
| A finding, with sources | `research/notes/YYYY-MM-DD-topic.md` |
| A question you could not answer | `research/open-questions.md` |
| A choice that shapes what we buy | a new ADR in `decisions/` |
| A product, a price, a spec, a pro or con | the right file in `candidates/items/` |
| The notes behind a product | that item's `research_notes` list |
| Which car seats click onto which stroller | that stroller's `compat` block |
| A fact about the cars, the house or the budget | `household/household.yaml` |

## Skills

Four project skills in `.claude/skills/` encode the workflows above:
`research-note`, `adr-write`, `candidate-update`, `fit-check`. They carry the
details — numbering, front matter, the schema, the fit method — so they do
not have to be remembered.

## Context worth carrying

- **Three categories to start:** stroller, car seat, and a *standalone sleep*
  bassinet (not a stroller bassinet attachment). More categories (carrier,
  high chair, monitor) can be added: add the category and its `spec_fields`
  in `candidates/schema.yaml`, a `candidates/items/<category>.yaml`, and a
  `categories/<category>/README.md`.
- **Car seats must be certified to FMVSS 213a** (side impact) — see
  [0001](decisions/0001-car-seat-must-meet-fmvss-213a.md). If that leaves
  nothing suitable, raise it with Nick; do not relax it quietly.
- **We buy for a 2022 Model Y, and we fly.** A 2026 Model Y L may come
  later but does not drive choices now.
- **Infant seat first, then the stroller that takes it** — see
  [0002](decisions/0002-infant-car-seat-that-clicks-onto-the-stroller.md).
  Pick the car seat before the stroller. A stroller must accept the chosen
  seat according to a manufacturer's chart. Products Nick mentions as
  examples (e.g. UPPAbaby Minu V3 + Aria V2) are reference points, not
  preferences: shortlist from the criteria, not from them.
- This repo was bootstrapped on 2026-11-27 from the structure of Nick's
  `interior-led-lighting` design repo. It starts empty: no candidates have
  been researched yet.
