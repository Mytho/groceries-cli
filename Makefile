all: help

help:
	@echo 'check    -- check the code syntax'
	@echo 'clean    -- cleanup the environment'
	@echo 'install  -- install the command'
	@echo 'test     -- test entire codebase'
	@echo 'unittest -- run the unit tests'

check:
	flake8 --show-source setup.py groceries tests

clean:
	find . -name '__pycache__' -delete -o -name '*.pyc' -delete

install:
	pip install --force-reinstall --upgrade --editable .

test: check
	tox

unittest:
	coverage run --source groceries --module pytest tests --assert=plain
	coverage report --fail-under=100 --show-missing
