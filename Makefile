.PHONY: install test run

install:
	pip install -r requirements.txt

test:
	pytest -q

run:
	python run.py
