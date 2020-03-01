# c-lang-parser
A python C-Lang parser for texts based on https://wiki.c-base.org/dokuwiki/c-lang


## installation

A working Python (min. 3.8) instance with pip.

Debian:

`sudo apt install python3 python3-dev python3-pip`

Other (Mac OS X, Windows ...):

[Official Download](https://www.python.org/downloads/release/python-382/)



Install python libraries:
`python3.8 -m pip install -r requirements.txt`


## command line tool

`parse.py` is a click application built as convenience bind to `parser.CLangParser.parse` function and features e.g. a file converter. To control the level (alien (1), member (2), core-member(3)) the `--level` option is available.

Example usage:

`python3.8 parse.py file.convert foo.txt bar.txt --level=3`


## development

The parser library contains the rules and forms (WIP) as JSON files. To modify the rules or add new ones just keep the syntax.

The parser library als contains the `CLangParser` and `CLangGrammarSet` with their respective Exceptions.
