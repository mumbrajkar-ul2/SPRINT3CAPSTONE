PYTHON ?= python3

.PHONY: test smoke etl package

test:
	$(PYTHON) -m pytest -q

smoke:
	$(PYTHON) scripts/sanity_check.py

etl:
	$(PYTHON) etl/run_daily_batch.py --sample
