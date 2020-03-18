#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import click
from parser import CLangParser


@click.group()
@click.option("--level", default=1, type=int,
              help="Level of parsing 1: alien, 2: member, 3: core-member")
@click.option("--forms", default=False, type=bool, help="To use forms or not")
def parse(level, forms):
    return


@parse.command()
@click.argument("input", type=click.File("r"), nargs=-1)
@click.argument("output", type=click.File("w+"))
@click.option("--level", default=1, type=int,
              help="Level of parsing 1: alien, 2: member, 3: core-member")
@click.option("--forms", default=False, type=bool, help="To use forms or not")
def file_convert(input, output, level, forms):
    """
    INPUT OUTPUT [--level] [--forms]
    """
    levels = {1: "alien", 2: "member", 3: "core-member"}
    parser = CLangParser(level=levels[level], forms=forms)
    output.write(parser.parse(input[0].read()))
    print("Done")


@parse.command()
@click.argument("input")
@click.option("--level", default=1, type=int,
              help="Level of parsing 1: alien, 2: member, 3: core-member")
@click.option("--forms", default=False, type=bool, help="To use forms or not")
def convert(input, level, forms):
    """
    INPUT [--level] [--forms]
    """
    levels = {1: "alien", 2: "member", 3: "core-member"}
    parser = CLangParser(level=levels[level], forms=forms)
    print(parser.parse(input))


if __name__ == "__main__":
    parse()
