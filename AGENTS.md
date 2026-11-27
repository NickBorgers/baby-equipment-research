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
- **The car seat decision comes first.** Whether to use an infant seat as a
  travel system (open question 9) decides whether stroller ↔ car seat
  compatibility matters at all.
- This repo was bootstrapped on 2026-11-27 from the structure of Nick's
  `interior-led-lighting` design repo. It starts empty: no candidates have
  been researched yet.
