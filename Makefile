.PHONY: refrensh lint install clean report test coverage build upload

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

install:
	$(pyyhon) -m pip uninstall uel -y
	$(python) -m setup install

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