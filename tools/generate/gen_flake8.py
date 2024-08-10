from generate import task
import os
import textwrap

output = ".flake8"
yapfignore = ".yapfignore"

@task(output)
def gen_flake8(dirname):
    with open(os.path.join(dirname, yapfignore), "rt") as f:
        ignore = f.read()
    result = textwrap.dedent(
    """
    [flake8]
    count: true
    statistics: true
    max-line-length: 120
    """
    )
    result += "exclude:\n"
    result += textwrap.indent(",\n".join(ignore.splitlines()), "    ")
    return result
