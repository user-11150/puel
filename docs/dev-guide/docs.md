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

* Don't use Latin abbreviations like "e.g." or "i.e." where English words will
    do, such as "for example" or "that is."
* Abbreviations should not be used extensively, and all abbreviations should
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
    
* Don't use any of symbol derived from the Latin words like "&" where english
    will do "and"

### Example is a good idea
In document, Many examples and No-examples. What you love? I think mostaudience like many examples

### Capitalization

#### Special words(english)
__Because these documents are typically accessed and modified by technical personnel, only special (unusual) spellings are described on this pack__

1. UEL: Capitalize in most cases
