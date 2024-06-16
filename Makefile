.PHONY: refrensh lint install clean report test coverage build

SOURCE=./src/uel
python=python

refrensh:
	make clean
	make install

build:
	python -m build

lint:
	mypy

install:
	$(python) -m pip install .

clean:
	rm -rf build
	rm -rf dist
	rm -rf .mypy_cache
	$(python) -m pip uninstall -y uel

report:
	$(python) report.py

coverage:
	coverage run -m unittest
	coverage html
	python -m http.server --directory htmlcov -b 127.0.0.1

test:
	$(python) -m unittest