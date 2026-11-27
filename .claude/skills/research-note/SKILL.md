---
name: research-note
description: Capture a research finding for the baby-equipment project into research/notes/ with sources, dates and confidence, then update the open-questions backlog and say what it changes in the candidates. Use whenever you have looked something up about a stroller, car seat, bassinet, a safety standard, a recall or a compatibility chart — before touching candidates/items/*.yaml or household/household.yaml.
---

# Writing a research note

Research comes before the data changes. A spec, pro, con or safety claim in
the candidates with no note behind it is a claim nobody can check later.

## Steps

1. **Narrow the question.** One note answers one question. If what you found
   answers three, write three notes.

2. **Copy the form.** Copy `research/TEMPLATE.md` to
   `research/notes/YYYY-MM-DD-kebab-topic.md`. Use today's real date. Fill
   in the front matter:

   ```yaml
   ---
   question: What are the folded dimensions of the 2026 Example Stroller?
   date: 2026-11-27
   category: stroller         # stroller | car-seat | bassinet | general
   confidence: high
   candidates: [example-stroller-2026]
   ---
   ```

3. **Cite everything, with dates.** Give a URL and the date accessed for
   every claim. Label each source as primary (NHTSA, CPSC, a standard, the
   manufacturer), independent testing, or retail/anecdotal. Don't blur them
   together.

4. **Keep units, model year and origin attached to numbers.** "22 in folded"
   is half a fact. "22 × 18 × 9 in folded, 2026 model, manufacturer spec
   sheet" is a fact.

5. **Set confidence honestly.**
   - `high`: primary source, or measured here
   - `medium`: independent testing, or several retail sources that agree
   - `low`: one review or forum post, an inference, or a different model year

6. **Say what it changes.** The Candidate impact section names the exact
   fields in `candidates/items/*.yaml` or `household/household.yaml` that this
   note justifies changing. Write it even if the answer is "nothing yet".

7. **Update the backlog.** In `research/open-questions.md`, check the box on
   the question you answered and link the note. Add any new questions the
   research raised.

8. **Then change the data** using the `candidate-update` skill, and run
   `make check`.

## What not to do

- Do not fill a `null` with a plausible-looking guess. `null` means "not
  researched yet", and the fit check depends on that meaning.
- Do not write a note with no sources. That is an opinion. Opinions belong
  in an ADR's rationale, labeled as opinions.
- Do not answer a question Nick should answer. Car models, measurements,
  budget, due date and how the gear will be used are his to supply. Ask;
  do not assume.
- Do not record a safety claim from a retailer or a review alone. Standards,
  recalls, expiry and safe-sleep claims need a primary source.
- Do not treat a manufacturer's spec and a reviewer's measurement as the
  same kind of number. Folded sizes and weights often differ between them.
