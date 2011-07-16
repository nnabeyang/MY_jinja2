#!/usr/bin/env python2.6
import unittest
from test import test_support
from MY_jinja2 import nodes, compiler
from MY_jinja2.lexer import *
from MY_jinja2.parser import *
class ParserTests(unittest.TestCase):
  def test_parser_parse(self):
    tokens = [
      Token('data', 'hello, '),
      Token('data', 'world')
      ]
    node = Parser.parse(TokenStream(tokens))
    generator = compiler.CodeGenerator()
    generator.visit_Template(node)
    self.assertEqual("""\
def root(dic):
  yield u'hello, '
  yield u'world'\
""", generator.get_code())
   
if __name__ == '__main__':
  test_support.run_unittest(ParserTests)
