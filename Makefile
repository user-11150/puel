SOURCE=./src/uel
python=python

refrensh:
	make imports_flush & make clean
	
	make install

build:
	$(python) setup.py sdist

lint:
	mypy --config-file=mypy.ini

imports_flush:
	$(python) imports_flush.py $(SOURCE)/__init__.py $(SOURCE)

install:
	$(python) setup.py install

clean:
	rm -rf build
	rm -rf dist
	rm -rf .mypy_cache
	$(python) -m pip uninstall -y uel

report:
	$(python) report.py