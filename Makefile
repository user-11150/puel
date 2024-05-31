refrensh: clean install

build:
	python setup.py sdist

lint:
	mypy --config-file=mypy.ini

install:
	python setup.py install

clean:
	rm -rf build
	rm -rf dist
	rm -rf .mypy_cache
	python -m pip uninstall -y uel

report:
	python report.py
