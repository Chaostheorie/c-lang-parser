# Written by Cobalt <chaosth0rie@protonmail.com>
# Source: https://github.com/Chaostheorie/c-lang-parser
# Based on syntax of https://wiki.c-base.org/dokuwiki/c-lang
# c-base - Berlins crashed space station
import os
import json
from simplejson.errors import JSONDecodeError


class CLangGrammarException(Exception):
    pass


class CLangParserException(Exception):
    pass


class CLangGrammarSet:
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
            forms = json.load(f)
        return

    def prepare_form(self):
        return

    def load_grammar(self, level, file, ranking):
        try:
            with open(file) as f:
                self.raw = json.load(f)
        except JSONDecodeError:
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
            raise CLangGrammarException("Invalid rankings data type")
        self.rankings = ranking

        return True

    def prepare_grammar(self):
        identifiers = {}
        self.rules = []
        for rule in self.raw:
            if not self.rankings[rule["level"]] > self.int_level:
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
        [self.identifiers.__setitem__(key, self.rules[value[0]])
         for key, value in identifiers.items()]

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

    def __getitem__(self, index):
        try:
            return self.identifiers[index]["replacement"]
        except KeyError:
            raise CLangParserException(f"'{key}' not in keys")

    def __setitem__(self, key, value):
        self.rukes[key] = value


class CLangParser:
    def __init__(self, text=None, level="alien", keep_result=True, parse=True,
                 rules=None, forms=None, grammar=None, lower=True):
        """Parser for c-lang advanced is meant for the c-lang advanced rules"""
        self.text = text
        self.keep_result = keep_result
        if self.keep_result:
            self.results = []
        self.lower = lower
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
            i += 1
            if i_pass_counter != 0:
                i_pass_counter -= 1
            elif self.text[i] == "\\":
                i_pass_counter = self.text[i:].rfind(" ")+1
            elif self.text[i] in self.grammar.identifiers:
                replacement = self.grammar[self.text[i]]
                if len(replacement) > 1:
                    i_pass_counter = len(replacement)
                else:
                    i_pass_counter = 1
                if self.grammar.check_conditions(self.text, i, self.text[i]):
                    self.text[i] = replacement
        self.text = "".join(self.text)
        if self.lower:
            self.text = self.text.lower()
        if self.keep_result:
            self.results.append(self.text)
        return self.text
