#!/usr/bin/env python2.6
import unittest
from test import test_support
from MY_jinja2 import nodes, compiler
from MY_jinja2.lexer import *
from MY_jinja2.parser import *
class CompilerTests(unittest.TestCase):
  def test_identifiers(self):
    identifiers = compiler.Identifiers()
    self.assertFalse(identifiers.is_declared('var_name'))
    identifiers.declared.add('var_name')
    self.assertTrue(identifiers.is_declared('var_name'))
  def test_nodevisitor_visit(self):
    class aVisitor(compiler.NodeVisitor):
      def __init__(self):
        self.log = []
      def visit_Name(self, node):
        self.log.append(node.name)
      def get_log(self):
        ret = ', '.join(self.log)
	self.log = []
	return ret
    visitor = aVisitor()
    visitor.visit(nodes.Name('var', 'load'))
    self.assertEqual('var', visitor.get_log())
    node = nodes.Template([nodes.Output(nodes.Name('var1', 'load')), nodes.Name('var2', 'load')])
    visitor.visit(node)
    self.assertEqual('var1, var2', visitor.get_log())
  def test_identifier_visitor(self):
    identifiers = compiler.Identifiers()

    self.assertFalse(identifiers.is_declared('var1'))
    self.assertFalse(identifiers.is_declared('var2'))
    
    visitor = compiler.IdentifierVisitor(identifiers)
    visitor.visit(nodes.Template([
      nodes.Output(nodes.Name('var1', 'store')),
      nodes.Name('var2', 'load')
      ]))

    self.assertTrue(identifiers.is_declared('var1'))
    self.assertFalse(identifiers.is_declared('var2'))

if __name__ == '__main__':
  test_support.run_unittest(CompilerTests)
