---
name: candidate-update
description: Add, change or retire a product in the baby-equipment project's candidates — candidates/items/*.yaml — following the schema and the status lifecycle, then regenerate docs (including its product page) and validate. Use whenever a product, price, spec, pro/con, safety fact, recall or car seat compatibility changes, and whenever docs/COMPARISON.md, docs/FIT.md or a page in docs/products/ looks out of date.
---

# Changing the candidates

The candidates are data. `candidates/items/*.yaml` is the source, and the
files in `docs/` are generated from it. **Editing `docs/` by hand does
nothing** except make `make check` fail.

## Where a candidate lives

There is one file per category: `stroller.yaml`, `car-seat.yaml`, and
`bassinet.yaml`. The `category` field inside the item must match the file,
and must be one of the categories in `candidates/schema.yaml`.

## The item shape

`candidates/schema.yaml` is the authority. Read it rather than trusting this
summary.

```yaml
- id: example-stroller-2026     # kebab-case, unique across every file
  name: Example Stroller (2026)
  category: stroller
  status: candidate             # see the lifecycle below
  summary: >-                   # optional; 2-4 plain sentences, top of the product page
    Leave this out until the research supports a summary.
  brand: Example
  price_usd: null               # null = not researched yet
  vendor_url: null
  decision: null                # ADR id, quoted, e.g. "0002"; the file must exist
  specs:                        # fields per category — see spec_fields in the schema
    weight_lb: null
    folded_in: null             # [l, w, h] in any order
    open_width_in: null
    one_hand_fold: null
  safety:
    standards: []               # e.g. "ASTM F833", from a primary source
    recalls: []                 # each: {date: YYYY-MM-DD, url: ..., summary: ...}
    checked_on: null            # date the CPSC/NHTSA recall search was run
  compat:                       # strollers only
    accepts_car_seats: []       # car-seat ids that click on directly
    needs_adapter: {}           # {car-seat-id: "Adapter product name"}
    incompatible: []            # confirmed: no adapter exists
  pros:                         # each cites its source with a Markdown link
    - Folds with one hand ([BabyGearLab](https://www.babygearlab.com/...)).
  cons:
    - Basket is small ([specs note](../../research/notes/2026-11-27-example-stroller-specs.md)).
  notes: |                      # a Markdown bullet list, one fact per bullet
    - What a future reader needs to know, with a link to its source.
    - What is still unknown ([open questions](../../research/open-questions.md)).
  research_notes:               # filenames in research/notes/; each must exist
    - 2026-11-27-example-stroller-specs.md
```

**Every pro, con, `summary` and `notes` field links its source**
(AGENTS.md rule 1a). The text renders in `docs/products/<id>.md`, so
relative links start `../../`. Take each URL from the research note's
Sources section; never invent one. Link the note itself when the claim is
the note's synthesis or has no URL. `make check` fails on an entry with no
link. The `...` URLs above are placeholders, not real sources.

## Status lifecycle

The statuses run `candidate` → `shortlisted` → `selected` → `ordered` →
`owned`. There is also `rejected`.

- `candidate`: on the list, not researched in depth.
- `shortlisted`: passes the hard gates (the accepted ADRs), and its specs
  are researched. Usability may not be judged yet, so a shortlisted item
  is not a recommendation (AGENTS.md rule 8).
- `selected`: decided. Before setting it, run the "What to judge" check in
  `adr-write` step 4, with or without an ADR. It usually has an ADR, so use
  the `adr-write` skill alongside this one.
- `rejected`: kept on the record so nobody researches it again. Say why in
  `notes`. Rejected items are left out of the cost rollup and the fit checks.

## Rules that matter

- **`null` means "not researched yet".** Never fill a `null` with a
  plausible guess to make a fit check pass. A null makes the matching check
  read *insufficient data*, and that is correct behavior.
- **A spec you have not looked up stays `null` or is left out.** Both read
  as unknown. Do not write `0` or `false` for "unknown".
- **Compat records manufacturer facts only.** A car seat that a stroller's
  `compat` does not list is *unknown*, not incompatible. Put a seat in
  `incompatible` only when a source says no adapter exists. Every id in
  `compat` must be a car-seat candidate in this repo. Add the seat first.
- **Every recall needs a URL and a date.** The validator enforces this.
- **FMVSS 213a goes in `safety.standards` only from a primary source.**
  Decision 0001 requires it for car seats. The comparison table shows `yes`
  when it is recorded and `?` otherwise.
- **A claim needs a note.** Use the `research-note` skill first, then bring
  the claim here. Each pro and con should trace to a note.
- **List the notes in `research_notes`.** Give the filename only, not the
  path. Every note behind the item goes there, not only the newest. The
  product page links them. Validation fails if a file does not exist.
- **A summary is optional.** Write 2-4 plain sentences only from what the
  notes say. With no `summary`, the page shows none. Do not invent one.
- **Start a con with "Misuse risk:"** when it is one. The product page lists
  those cons first.
- **Say which model year.** Put it in `name` when it matters.

## Finish the job

```sh
make docs     # regenerate docs/: COMPARISON.md, FIT.md, products/
make check    # validate, confirm docs are current, run tests
```

Open `docs/products/<id>.md` and read it once. It is what Nick reads first.
Check that it shows the change and links the right notes.

Commit the YAML and the regenerated `docs/` together. When you retire an id,
`make docs` deletes its old page.

## When validation fails

The error names the file and the item id. Common errors:

- *duplicate id*: ids must be unique across every file, not just within one.
- *unknown spec*: that spec belongs to a different category. Check
  `spec_fields`.
- *compat names `x`, which is not a car-seat id*: add the seat candidate
  first, or fix the id.
- *needs a url*: a recall without a source.
- *decision NNNN is superseded-by-...*: repoint the item at the replacement.
- *research_notes names `x`, not in research/notes/*: fix the filename, or
  write the note first.
- *should be the filename only*: drop the `research/notes/` prefix.
- *generated docs are out of date*: run `make docs`.
