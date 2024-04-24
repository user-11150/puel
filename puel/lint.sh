main="main.py"

mypy ${main} --config-file=mypy.ini
pylint ${main}

