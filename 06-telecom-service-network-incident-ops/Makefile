PYTHON ?= python3

.PHONY: test smoke etl package setup evidence

# setup: create .venv, install requirements.txt, run pytest -q (see scripts/bootstrap.sh).
# On Windows without make, run scripts/bootstrap.ps1 instead.
setup:
	PYTHON=$(PYTHON) bash scripts/bootstrap.sh

test:
	$(PYTHON) -m pytest -q

smoke:
	$(PYTHON) scripts/sanity_check.py

etl:
	$(PYTHON) etl/run_daily_batch.py --sample

# evidence: run every pipeline stage and write evidence/ (see scripts/evidence.sh and docs/07-cicd/).
# On Windows without make, run scripts/evidence.ps1 instead. Both write the same 14 files.
evidence:
	PYTHON=$(PYTHON) bash scripts/evidence.sh all
