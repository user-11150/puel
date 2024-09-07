from __future__ import annotations

from mkdocs.structure.pages import Page
from mkdocs.exceptions import MkDocsException

import logging

logger = logging.getLogger('mkdocs')

FILE_MAX_SIZE = 1024 * 180
LINE_MAX_SIZE = 90

def on_page_markdown(markdown, page: Page, **kwargs):
    file = page.file.src_path
    logger.info("Checking %s" % file)
    if len(markdown) > FILE_MAX_SIZE:
        logger.error('%s is too long' % file)
    for lineno, line in enumerate(start=1, iterable=markdown.splitlines()):
        if len(line) > LINE_MAX_SIZE:
            logger.error(f'{file}:{lineno} is too long')
