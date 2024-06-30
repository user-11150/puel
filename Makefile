.PHONY: refrensh lint install clean report test coverage build upload docs-serve docs-build imports_flush

SOURCE=./src/uel
python=python

refrensh:
	make clean
	make install

build:
	python -m setup sdist

upload:
	twine upload dist/*

lint:
	mypy

format:
	yapf -ir ./src

install:
	$(python) -m pip uninstall uel -y
	$(python) -m setup install

clean:
	rm -rf build
	rm -rf dist
	rm -rf .mypy_cache
	$(python) -m pip uninstall -y uel

report:
	$(python) tools/report.py

coverage:
	coverage run -m unittest
	coverage html
	python -m http.server --directory htmlcov -b 127.0.0.1

test:
	$(python) -m unittest

docs-serve:
	mkdocs serve

docs-build:
	mkdocs build

imports_flush:
	python tools/imports_flush.py src/uel/__init__.py src/
