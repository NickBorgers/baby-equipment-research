# Material for MkDocs prints an end-of-life banner on every build.
export NO_MKDOCS_2_WARNING := 1

.PHONY: all check docs test lint fit site serve

# `make` on its own regenerates the docs and then verifies everything.
all: docs check

## check: validate the data, confirm the generated docs are current, run tests
check: lint
	python tools/candidates.py --check
	pytest -q
	$(MAKE) site

## docs: regenerate docs/ (COMPARISON.md, FIT.md, products/) from the YAML
docs:
	python tools/candidates.py

## test: run the test suite only
test:
	pytest -q

## lint: style check the Python under tools/ and tests/
lint:
	ruff check tools tests

## fit: print the compatibility + fit report without writing anything
fit:
	python tools/fit.py

## site: build the GitHub Pages site into build/site/ (fails on broken links)
site:
	python tools/site.py
	mkdocs build --quiet -f build/mkdocs.yml

## serve: preview the site at http://localhost:8000, rebuilding on change
serve:
	python tools/site.py
	mkdocs serve -f build/mkdocs.yml -a 0.0.0.0:8000
