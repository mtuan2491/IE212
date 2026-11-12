PYTHON ?= python
TASK ?= DEMO
BASE ?= main
export IE212_PYTHON := $(PYTHON)

.PHONY: doctor task-input task-output test merge-check
doctor:
	$(PYTHON) scripts/bootstrap/doctor.py
task-input:
	$(PYTHON) scripts/tasks/check_input.py $(TASK)
task-output:
	$(PYTHON) scripts/tasks/check_output.py $(TASK)
test:
	bash scripts/ci/run_tests.sh
merge-check:
	bash scripts/ci/validate_merge.sh $(BASE) $(TASK)
