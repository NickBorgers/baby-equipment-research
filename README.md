# Baby equipment

Research and decisions on baby gear, done the same way as Nick's other design
repos: every claim is sourced, every decision is recorded, and every unknown
is tracked. It starts with three categories: a **stroller**, a **car seat**,
and a **standalone sleep bassinet**.

**Status: scaffolded, not researched.** No candidates are recorded yet. The
backlog in [`research/open-questions.md`](research/open-questions.md) lists
what to find out first: the household facts (cars, trunk, doorways, bedroom
space, budget, due date), the shape decisions (above all, infant car seat +
travel system vs. a convertible seat from birth), and the safety standards
to source.

## Categories

| Category | What it covers |
| --- | --- |
| [stroller](categories/stroller/) | The stroller, including a frame that carries an infant car seat |
| [car-seat](categories/car-seat/) | Infant (bucket) seat or convertible seat for the newborn period |
| [bassinet](categories/bassinet/) | A standalone or bedside sleep bassinet — not a stroller attachment |

## Repository layout

```
AGENTS.md          How to work in this repo. Read it before changing anything.
README.md          This file.

candidates/
  schema.yaml      The candidate schema, read by the validator and the skills.
  items/*.yaml     The products under consideration, one file per category.
household/household.yaml   The cars, the house, the bed, the budget.

decisions/         Architecture decision records. 0000 is the template.
research/
  open-questions.md  The live backlog of everything unknown.
  TEMPLATE.md        The form for a research note.
  notes/             One note per question answered, with sources and dates.

categories/*/      A thin index per category: decisions, candidates, open questions.

tools/
  repo.py          Loading helpers shared by everything under tools/.
  candidates.py    Validates the candidates and renders the generated docs.
  fit.py           The compatibility and fit checks.
  figures.py       Catches superseded figures left in hand-written prose.
tests/             Tests for the data and the checks.

docs/              GENERATED. Do not edit. `make docs` rebuilds these.
  COMPARISON.md    Side-by-side table for each category.
  FIT.md           Compatibility and fit results.
```

## Running it

Open the folder in the devcontainer and everything is installed. Start it
with `dcr` (or `dcs` to reuse a running container) so the shell profile,
agent CLIs and credentials get injected from `~/code/util`; this repo's
`devcontainer.json` deliberately mounts no host config of its own. Then:

```sh
make check    # validate the data, confirm docs are current, run the tests
make docs     # regenerate docs/ after editing any YAML
make fit      # print the compatibility + fit report without writing anything
```

Without a devcontainer: `pip install -r requirements.txt` on Python 3.12,
then the same commands. CI runs `make check` on every push.

## What the fit check does

`tools/fit.py` answers questions like these:

- Does this infant car seat click onto this stroller, directly or with an
  adapter? (This is a "travel system".)
- Does the folded stroller fit in the trunk, through the door, and in its
  storage spot?
- Is the car seat narrow enough for the back seat? (A rough screen only.)
- Does the bassinet fit beside the bed, and match the bed's height?

Each answer is **fits**, **does not fit**, or **insufficient data**.

## Why the tooling exists

The candidates and household facts are data, not prose. Numbers live in
YAML; `make docs` renders them. Editing `docs/` by hand does nothing except
fail the next `make check`.

The fit check refuses to guess. An unknown reads *insufficient data*, never
*fits*, because a stroller whose folded size was never checked "probably
fits" right up until it does not go in the trunk. The report's last section
lists exactly which measurements would turn each unknown into an answer.
