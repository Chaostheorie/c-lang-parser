# c-lang-parser

A python C-Lang parser for texts based on <https://wiki.c-base.org/dokuwiki/c-lang>

## Installation

A working Python (min. 3.8) instance with pip.

Debian:

`sudo apt install python3.8 python3.8-dev python3.8-pip`

Other (Mac OS X, Windows ...):

[Official Download](https://www.python.org/downloads/release/python-382/)

Install python libraries: `python3.8 -m pip install -r requirements.txt`

Now you should be able to use the Parser with the included `parse.py`.

Examples:

Command Line convert:

```
./parse.py convert kai --level=3 --forms=True

Input:
kai
Output:
cAi
```

File Convert:

```
./parse.py file-convert README.md REAMDE_converted.md --level=3 --forms=True

Input:
See README.md
Output:
See new file REAMDE_converted.md
```

## How to use

The intended use is to convert text, markdown or other types of not encoded (pdf, odf ...) files. Also the included `parse.py` is a simple to use tool to the `CLangParser` object. To make the experience good for all types of users the included levels. To properly take advantage of the levels you should determine in which category you sort yourself in you can take a look at `parse_rules.json` after you have took a look maybe try the levels out with `--level=int` (default: 1 mor with `--help`). Also <ou can take a look at `forms.json` to take a look at thefomrs and maybe try them out with `--forms=True` (default: False).

## Compile with cython3 and gcc

This is currently broken due to some cython3 problem with recognizing the args of `CLangParser.parse` as `object` and _`text`_.

You will need a working instance of `python3.8` including `python3.8-dev`, `python3.8-config` and `cython3` + preferably `gcc` (tested on 8.3.0). The compiled file will still need the `parse_rules.json` and `forms.json` in the same folder as the executed file.

First you need to compile the `parse.py`:

`cython3 -X language_level=3 --embed --cleanup 1 parse.py`

Then compile the generated `parse.c` to a program:

```
gcc parse.c --pipe -fPIC -fvisibility=hidden -O2 -W -Wall `python3.8-config --embed --libs --cflags --includes` -o parse
```

Now the `parse` executable is ready to use an can be e.g. put into /usr/bin

## Command line tool

`parse.py` is a click application built as convenience bind to `parser.CLangParser.parse` function and features e.g. a file converter. To control the level (alien (1), member (2), core-member(3)) the `--level` option is available.

Example usage:

`python3.8 parse.py file.convert foo.txt bar.txt --level=3`

## Development

The parser library contains the rules and forms (WIP) as JSON files. To modify the rules or add new ones just keep the syntax.

The parser library als contains the `CLangParser` and `CLangGrammarSet` with their respective Exceptions.

The used logger instance is `CLangParser` for both the `CLangParser` and `CLangGrammarSet`.
