#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

# Written by Cobalt <https://sinclair.gq> 2018
# Warning: This codewas left untouched for two years and only for some issues
# ligthly touched by Cobalt. The code is in dire need of refactoring
# Source: https://github.com/Chaostheorie/c-lang-parser
# Based on syntax of https://wiki.c-base.org/dokuwiki/c-lang
# c-base - Berlins crashed space station
import os
import ujson
import logging
from collections import OrderedDict


class CLangGrammarException(Exception):
    pass


class CLangParserException(Exception):
    pass


class CLangGrammarSet:
    log = logging.getLogger("CLangParser")

    def __init__(self, level, file=None, form_file=None,
                 ranking={"alien": 1, "member": 2, "core-member": 3},
                 use_form=True, form="polite"):
        if file is None:
            file = os.path.realpath(__file__)[:-11] + "parse_rules.json"
        if form_file is None:
            form_file = os.path.realpath(__file__)[:-11] + "forms.json"
        self.load_grammar(level, file, ranking)
        self.prepare_grammar()
        if use_form:
            self.load_form(form, form_file)
            self.prepare_form()

    def load_form(self, form, file):
        with open(file) as f:
            self.forms = ujson.load(f)
        return

    def prepare_form(self):
        return

    def load_grammar(self, level, file, ranking):
        try:
            with open(file) as f:
                self.raw = ujson.load(f)
        except ValueError:
            raise CLangGrammarException(f"Grammar set was not decodable")
        except FileNotFoundError:
            raise CLangGrammarException(f"Grammar file '{file}' was not found")
        try:
            if level not in ranking.keys():
                raise CLangGrammarException(f"Invalid Level '{level}'")
            else:
                self.level = level
                self.int_level = ranking[self.level]
        except TypeError:
            raise CLangGrammarException("Invalid rankings rule type")
        self.rankings = ranking

        return True

    def prepare_grammar(self):
        identifiers = {}
        self.rules = []
        for rule in self.raw:
            if rule["identifier"] == "":
                continue
            elif not self.rankings[rule["level"]] > self.int_level:
                if not rule["identifier"] in identifiers.keys():
                    self.rules.append(rule)
                    identifiers[rule["identifier"]] = [len(self.rules)-1,
                                                       self.rankings[
                                                       rule["level"]]]
                else:
                    if self.rankings[rule["level"]] > identifiers[rule["identifier"]][1]:
                        self.rules.pop(identifiers[rule["identifier"]][0])
                        self.rules.append(rule)
                        identifiers[rule["identifier"]] = [len(self.rules)-1,
                                                           self.rankings[
                                                           rule["level"]]]
        self.identifiers = {}

        # Update according to rules
        [self.identifiers.__setitem__(key, self.rules[value[0]])
         for key, value in identifiers.items()]

        # sort by identifier length
        unsorted = self.identifiers.copy()
        self.identifiers = OrderedDict()
        [self.identifiers.__setitem__(key, unsorted[key])
         for key in sorted(unsorted.keys(), key=len, reverse=True)]
        self.log.debug(f"identifiers: {self.identifiers}")

    def check_conditions(self, full, part, identifier):
        rule = self.identifiers[identifier]
        if rule["in_word"] and rule["at_beginning"] and rule["at_end"]:
            return True
        if rule["in_word"] and (full[(part-1)] == " " or
                                full[(part+1)] == " "):
            return False
        if rule["at_beginning"] and (full[(part-1)] != " " and not rule["at_end"]):
            return False
        if rule["at_end"] and (full[(part+1)] != " " and not rule["at_beginning"]):
            return False
        return True

    def get_identifier(self, iteration, full, checked=[]):
        identifiers = self.identifiers.copy()
        [identifiers.pop(rule) for rule in checked]
        for identifier, rule in identifiers.items():
            self.log.debug(f"text: {full[iteration]} identifier: {identifier}")
            if not rule["case-specific"] and \
              full[iteration].lower() == identifier[0].lower():
                if (length := len(identifier)) > 1:
                    for i in range(length):
                        if not identifier[i].lower() == full[iteration+i].lower():
                            checked.append(identifier)
                            return self.get_identifier(iteration, full, checked=checked)
                return rule
            elif rule["case-specific"] and full[iteration] == identifier:
                if (length := len(identifier)) > 1:
                    for i in range(length):
                        if not identifier[i] == full[iteration+i]:
                            checked.append(identifier)
                            return self.get_identifier(iteration, full, checked=checked)
                return rule
        return None

    def __getitem__(self, index):
        try:
            return self.identifiers[index]["replacement"]
        except KeyError:
            raise CLangParserException(f"'{key}' not in keys")

    def __setitem__(self, key, value):
        self.rukes[key] = value


class CLangParser:
    log = logging.getLogger("CLangParser")

    def __init__(self, text=None, level="alien", keep_result=True, parse=True,
                 rules=None, forms=None, grammar=None,
                 lower=False, upper=False):
        """Parser for c-lang advanced is meant for the c-lang advanced rules"""
        self.text = text
        self.keep_result = keep_result
        if self.keep_result:
            self.results = []
        self.lower = lower
        self.upper = upper
        if grammar is None:
            if rules is None:
                rules = os.path.abspath(__file__)[:-11] + "parse_rules.json"
            self.grammar = CLangGrammarSet(level, rules, forms)
        else:
            self.grammar = grammar
        if self.text is not None and parse is True:
            self.parse(self.text)

    def parse(self, text):
        self.text = list(text)
        i_pass_counter = 0
        i = 0
        while i != len(self.text)-1:
            if (identifier := self.grammar.get_identifier(i, self.text)) is not None:
                self.log.debug(f"replaced {self.text[i]} with {identifier['replacement']}")
                if (pass_counter := len(identifier["replacement"])) > 1:
                    i_pass_counter = pass_counter
                    for x in range(i_pass_counter):
                        self.text[i+x] = identifier["replacement"][x]
                else:
                    self.text[i] = identifier["replacement"]
            i += 1
        self.text = "".join(self.text)
        if self.lower:
            self.text = self.text.lower()
        elif self.upper:
            self.text = self.text.upper()
        if self.keep_result:
            self.results.append((text, self.text))  # type: tuple
        return self.text
