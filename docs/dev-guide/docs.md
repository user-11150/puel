# Documentation

## Table of contents
[TOC]

## Abstract

UEL has substantial documentation, The markup used for the UEL documentation is
Markdown

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
some black man, Korean peoples, They are not native English speakers.

1. Don't use Latin abbreviations like "e.g." or "i.e." where English words will
    do, such as "for example" or "that is."
2. Abbreviations should not be used extensively, and all abbreviations should
    be clearly indicated
    
    For example.
    
    === ":fontawesome-regular-thumbs-down: bad"
        ```markdown
        I18n is good
        ```
    === ":fontawesome-regular-thumbs-up: Use full spelling"
        ```markdown
        Internationalization is good
        ```
    === ":fontawesome-regular-thumbs-up: Use footnote"
        ```markdown
        I18n[^1] is good
        
          [^1]: Internationalization
        ```
    
3. Don't use too long words. for example.
    
    "Pneumonoultramicroscopicsilicovolcanoconiosis"
    
4. Use many kinds of emoji.
    
    Use emoji to make documents easier to read

### Affirmative tone
The documentation focuses on affirmatively stating what the language does and
how to use it effectively.

Except for certain security or segfault risks, the docs should avoid wording
along the lines of “feature x is dangerous” or “experts only”. These kinds of
value judgments belong in external blogs and wikis, not in the core documentation.

For example.

=== "Bad example"
    ```markdown
    The "force" in "git push" is danger, never use it
    ```
=== "Good example"
    ```markdown
    If you encounter a conflict when pushing, you can pull it first.
    ```

### Example is a good idea
In document, Many examples and No-examples. What you love? I think mostaudience like many examples

### Capitalization

#### Special words(english)
__Because these documents are typically accessed and modified by technical personnel, only special (unusual) spellings are described on this pack__

1. UEL: Capitalize in most cases
