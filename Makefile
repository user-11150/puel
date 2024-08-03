.PHONY: refresh lint install clean report test coverage build upload docs-serve docs-build release gen

SOURCE=./src/uel
python=python

refresh:
	make gen
	make install

gen:
	python tools/gen.py ./

release:
	python tools/release.py

build:
	python -m setup build
	python -m setup sdist
	python -m setup bdist_wheel
	python -m setup bdist_egg

upload:
	twine upload dist/*

lint:
	flake8 src/ tools/ --count --statistics --exclude src/uel/executing || true
	mypy || true

format:
	yapf -ir ./src /tools/

install:
	$(python) -m pip uninstall uel -y
	$(python) -m setup install

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
