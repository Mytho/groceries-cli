all: help

help:
	@echo 'clean     -- cleanup the environment'
	@echo 'install   -- install the command'

clean:
	find . -name '__pycache__' -delete -o -name '*.pyc' -delete

install:
	pip install --editable .
