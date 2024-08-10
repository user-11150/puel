.PHONY: refresh lint install clean report test coverage build upload docs-serve docs-build release gen

SOURCE=./src/uel
python=python

CODE_DIRECTORYS=./src /tools/

refresh:
	make gen
	make format
	make install
	make lint

gen:
	python tools/gen.py ./

release:
	python tools/release.py

build:
	python -m build

upload:
	twine upload dist/*

lint:
	flake8 src/ || true
	mypy || true

format:
	yapf -ir $(CODE_DIRECTORYS)

install:
	$(python) -m pip install .

clean:
	rm -rf build
	rm -rf dist
	rm -rf site
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
