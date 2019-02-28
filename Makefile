.PHONY: test

test:
	python -m unittest discover

local-run:
	python ./app.py
