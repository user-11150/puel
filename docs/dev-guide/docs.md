# Documentation

## Table of contents
[TOC]

## Abstract

UEL has substantial documentation, The markup used for the UEL documentation is
Markdown,

## Build the documentation
To build the documentation, follow the steps in one of the sections below.

1. Install CPython
2. Install build requirements
    ```bash
    python -m pip install -r requirements/requirements-dev.txt
    ```
3. Build the documentation
    
    === "By mkdocs"
        ```
        python -m mkdocs build
        ```
    === "By Makefile"
        In fact, it now is "python mkdocs build", too
        
        ```bash
        make docs-build
        ```

## Style Guide

This page describes the linguistic style guide for our documentation.

### Use simple language in documentation
Avoid esoteric phrasing where possible. Our audience is world-wide and may
not be native English speakers. For example, Chinese peoples, Japanese peoples,
Korean peoples, They are not native English speakers.

1. Don't use Latin abbreviations like "e.g." or "i.e." where English words will
    do, such as "for example" or "that is."
2. Abbreviations should not be used extensively, and all abbreviations should
    be clearly indicated
    
    For example.
    
    === "bad"
        ```markdown
        I18n is good
        ```
    === "Use full spelling"
        ```markdown
        Internationalization is good
        ```
    === "Use footnote"
        ```markdown
        I18n[^1] is good
        
          [^1]: Internationalization
        ```

### Affirmative tone
The documentation focuses on affirmatively stating what the language does and
how to use it effectively.

Except for certain security or segfault risks, the docs should avoid wording
along the lines of “feature x is dangerous” or “experts only”. These kinds of
value judgments belong in external blogs and wikis, not in the core documentation.
