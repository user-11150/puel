.PHONY: refrensh dev build lint install clean report test

SOURCE=./src/uel
python=python

refrensh:
	make clean
	make install

dev:
	$(python) -m pip uninstall -y uel
	make install

build:
	$(python) setup.py build

lint:
	mypy --config-file=mypy.ini

install:
	$(python) setup.py install

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


