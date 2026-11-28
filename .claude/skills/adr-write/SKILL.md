---
name: adr-write
description: Record or supersede a decision for the baby-equipment project as a numbered ADR in decisions/, with correct front matter and linked candidates. Use when a choice shapes what gets bought — travel system vs. convertible car seat, which stroller, which bassinet, buy vs. rent, used vs. new — or when an earlier decision is being replaced.
---

# Writing an ADR

An ADR records **what** was decided and **why**. The evidence lives in
`research/notes/`, and the ADR links to it.

Write an ADR when the choice shapes what gets bought, or rules other options
out. Example: choosing an infant car seat narrows which strollers work as a
travel system. Skip it for reversible details; those go in the candidate's
`notes`.

## Writing a new decision

1. **Allocate the next number.** Look in `decisions/` and take the next
   unused four-digit id. Numbers are never reused, even for abandoned drafts.

2. **Copy `decisions/0000-template.md`** to `decisions/NNNN-kebab-title.md`.

3. **Fill in the front matter exactly.** Tools read it, and `make check`
   validates it:

   ```yaml
   ---
   id: "0001"                 # quoted, matches the filename, four digits
   title: Infant car seat as part of a travel system
   status: proposed           # proposed | accepted | superseded-by-NNNN
   date: 2026-11-27
   category: car-seat         # a category in candidates/schema.yaml, or "general"
   candidates: []             # candidate ids this decision selects or rules out
   summary: >-                # required once accepted; shown on the public site
     2-4 plain sentences: what we chose and the main reasons.
   if_yours_differs:          # required once accepted; shown on the public site
     - >-
       When another choice would suit another family, and why.
   ---
   ```

   `summary` and `if_yours_differs` are for readers outside the household.
   The site's home page shows them for every accepted ADR (AGENTS.md rule
   4b). Restate only what the ADR body and its notes already source. Write
   `if_yours_differs` from the Alternatives considered section: for each
   alternative, say which family it would suit.

4. **If the ADR selects a product, check the evidence first.** Go through
   the "What to judge" list in the category README. Each row needs a
   research note behind it, or a line in the ADR's Open questions naming it
   as a gap that Nick accepted. Usability counts: a pick made on specs alone
   is not ready for an ADR (AGENTS.md rules 8 and 9). If a row is missing,
   research it or ask Nick before writing the ADR.

5. **Write the body.** It has these sections: Context, Decision, Rationale,
   Alternatives considered, Consequences, Open questions. People often skip
   two of these, and they are the two most useful later:
   - **Alternatives considered**: say why each one lost.
   - **Consequences**: what this commits us to. Include what it rules out
     in other categories.

6. **Point the candidates at it.** Set `decision: "0001"` on each affected
   candidate in `candidates/items/*.yaml`. Then run `make docs` and
   `make check`.

## Superseding a decision

Never edit an accepted ADR to say something different. Doing so erases the
reason we changed course.

1. Write the new ADR as above. In its Context, explain what changed (a
   recall, a new model year, a household change).
2. Set the old ADR's status to `superseded-by-NNNN`. Leave its body alone.
3. Repoint every candidate that referenced the old ADR to the new one.
4. `make check` fails while any candidate still points at a superseded ADR.
   That failure means the repo caught a half-finished change. Fix the
   candidates, not the check.

## Status meanings

- `proposed`: written down, not committed to. Safe to argue with.
- `accepted`: what we are buying to.
- `superseded-by-NNNN`: replaced, kept for the history.

Reversing an accepted ADR needs real new evidence, not a stylistic
preference. Raise it with Nick rather than rewriting it yourself (see
AGENTS.md rule 7).
