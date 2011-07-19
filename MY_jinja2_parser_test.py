#!/usr/bin/env python2.6
import unittest
from test import test_support
from MY_jinja2 import nodes, compiler
from MY_jinja2.lexer import *
from MY_jinja2.parser import *
class ParserTests(unittest.TestCase):
  def test_parser_data_parse(self):
    tokens = [
      Token(TOKEN_DATA, 'hello, '),
      Token(TOKEN_DATA, 'world')
      ]
    node = Parser.parse(TokenStream(tokens))
    self.assertEqual(
    nodes.Template([
      nodes.Output(nodes.TemplateData('hello, ')),
      nodes.Output(nodes.TemplateData('world'))
      ]), node)
  def test_parser_var_parse(self):
    tokens = [
      Token(TOKEN_VARIABLE_BEGIN, ''),
      Token(TOKEN_NAME, 'world'),
      Token(TOKEN_VARIABLE_END, ''),
      ]
    node = Parser.parse(TokenStream(tokens))
    self.assertEqual(nodes.Template([nodes.Output(nodes.Name('world', 'load')),]), node)
if __name__ == '__main__':
  test_support.run_unittest(ParserTests)
