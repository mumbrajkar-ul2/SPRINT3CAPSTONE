PYTHON ?= python3

.PHONY: test smoke etl package setup evidence security

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

# security: run only the security stage. This is stage 6 of `make evidence`.
# It runs `pytest -m security`, writes evidence/junit-security.xml, and fails on a skipped test (S05-13, SB-10).
# `opa` must be on the PATH, or the two Python-versus-Rego tests skip and the stage fails.
# On Windows without make, run: powershell -ExecutionPolicy Bypass -File scripts\evidence.ps1 -Stage security
security:
	PYTHON=$(PYTHON) bash scripts/evidence.sh security
