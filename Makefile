PYTHON ?= python

.PHONY: install pipeline app test lint export
install:
	$(PYTHON) -m pip install -r requirements.txt
pipeline:
	$(PYTHON) scripts/10_run_full_pipeline.py
app:
	$(PYTHON) -m streamlit run app/streamlit_app.py
test:
	$(PYTHON) -m pytest
lint:
	$(PYTHON) -m ruff check .
export:
	$(PYTHON) scripts/09_export_powerbi.py

