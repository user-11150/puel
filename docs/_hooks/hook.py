from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files
from mkdocs.config.defaults import MkDocsConfig

import math
import re

from html.parser import HTMLParser


class Readtime:
    def __init__(self, words_per_minute):
        self.words_per_minute = words_per_minute
    
    class ReadtimeParser(HTMLParser):
    
        # Initialize parser
        def __init__(self):
            super().__init__(convert_charrefs = True)
    
            # Keep track of text and images
            self.text   = []
            self.images = 0
    
        # Collect images
        def handle_starttag(self, tag, attrs):
            if tag == "img":
                self.images += 1
    
        # Collect text
        def handle_data(self, data):
            self.text.append(data)
    
    def readtime(self, html: str):
        parser = self.ReadtimeParser()
        parser.feed(html)
        parser.close()
    
        # Extract words from text and compute readtime in seconds
        words = len(re.split(r"\W+", "".join(parser.text)))
        seconds = math.ceil(words / self.words_per_minute * 60)
    
        # Account for additional images
        delta = 12
        for _ in range(parser.images):
            seconds += delta
            if delta > 3: delta -= 1
    
        # Return readtime in minutes
        return math.ceil(seconds / 60)


def readtime(html):
    readtime_element_styles = "float: right"
    return f"<small style='{readtime_element_styles}'>{Readtime(75).readtime(html)} min read</small>"

def on_page_content(html, *, page, config, files):
    return f"{readtime(html)}\n\n{html}"
