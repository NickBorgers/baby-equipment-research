.PHONY: all check docs test lint fit

# `make` on its own regenerates the docs and then verifies everything.
all: docs check

## check: validate the data, confirm the generated docs are current, run tests
check: lint
	python tools/candidates.py --check
	pytest -q

## docs: regenerate docs/COMPARISON.md and docs/FIT.md from the YAML
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
