#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
__author__ = "Cobalt"
__doc__ = "cli tool for the c-alng-parser libary"

import logging
import sys
from os import path
from parser import CLangParser

# set logging levels
if "-d" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

# Asks which level should be used
levels = {1: "alien", 2: "member", 3: "core-member"}
number = None
while number not in levels.keys():
    print("".join([f"{levels[i+1]} [{i+1}] " for i in range(len(levels))]))
    try:
        number = int(input("Level: "))
    except ValueError:
        print("That wasn't a valid integer")

level = levels[number]

# Asks which mode should be used
modes = {1: "line", 2: "file-converter"}
number = None
while number not in modes.keys():
    print("".join([f"{modes[i+1]} [{i+1}] " for i in range(len(modes))]))
    try:
        number = int(input("Mode: "))
    except ValueError:
        print("That wasn't a valid integer")

mode = modes[number]

# Load parser
parser = CLangParser(level=level, lower=False)

if mode == "line":
    inp = input("Source: ")
    print(parser.parse(inp))
elif mode == "file-converter":
    while True:
        if path.exists((source := input("Source Path: "))):
            print(f"Selected {source} as source")
            break
        else:
            print(f"Path {source} doesn't exist")
    output = input("output path: ")
    with open(source) as f:
        with open(output, "w+") as o:
            o.write(parser.parse(f.read()))
