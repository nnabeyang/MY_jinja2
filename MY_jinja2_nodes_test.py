#!/usr/bin/env python2.6
import unittest
from test import test_support
from MY_jinja2 import nodes, compiler
import MY_jinja2
class NodeTests(unittest.TestCase):
  def setUp(self):
    self.generator = compiler.CodeGenerator()
    self.data = '<html><body>hello, world<body></html>'
  def test_TemplateDataNode(self):
    node = nodes.TemplateData(self.data)
    self.assertEqual("TemplateData(data='%s')" % self.data, repr(node))
    self.assertEqual(node, nodes.TemplateData(self.data))
    self.generator.visit_TemplateData(node)
    self.assertEqual("u'%s'" % self.data, self.generator.get_code())
  def test_OutputNode(self):
    node = nodes.Output(nodes.TemplateData(self.data))
    self.generator.visit_Output(node)
    self.assertEqual("Output(node=TemplateData(data='%s'))" % self.data, repr(node))
    self.assertEqual(node, nodes.Output(nodes.TemplateData(self.data)))
    self.assertEqual("yield u'%s'" % self.data, self.generator.get_code())
  def test_TemplateNode_from_one_node(self):
    node = nodes.Template([nodes.Output(nodes.TemplateData(self.data))])
    self.generator.visit_Template(node)
    self.assertEqual("""\
def root(dic):
  yield u'%s'\
""" % self.data
    , self.generator.get_code())
  def test_TemplateNode_from_multi_nodes(self):
    data = ('<html>',
             '<head><title>hello, world</title></head>',
             '<body>hello, world</body>',
             '</html>'
	     )
    _nodes = []
    _nodes.append(nodes.Output(nodes.TemplateData(data[0])))
    _nodes.append(nodes.Output(nodes.TemplateData(data[1])))
    _nodes.append(nodes.Output(nodes.TemplateData(data[2])))
    _nodes.append(nodes.Output(nodes.TemplateData(data[3])))
    self.generator.visit_Template(nodes.Template(_nodes))
    expect = """\
def root(dic):
  yield u'%s'
  yield u'%s'
  yield u'%s'
  yield u'%s'\
""" % data
    self.assertEqual(expect, self.generator.get_code())
  def test_Node_iter_fields(self):
    node = nodes.Name('var', 'load')
    expect =[
      ('name', 'var'),
      ('ctxt', 'load')
    ]
    result = []
    for it in node.iter_fields():
      result.append(it)
    self.assertEqual(expect, result)
  def test_OutputNode_iter_child_nodes(self):
    name = nodes.Name('var', 'load')
    node = nodes.Output(name)
    result = []
    for it in node.iter_child_nodes():
      result.append(it)
    self.assertEqual([name], result)
  def test_Template_iter_child_nodes(self):
    node1 = nodes.Output(nodes.Name('var1', 'load'))
    node2 = nodes.Output(nodes.Name('var2', 'load'))
    node = nodes.Template([node1, node2])
    result = []
    for it in node.iter_child_nodes():
      result.append(it)
    self.assertEquals([node1, node2], result)
  def test_visit_Name(self):
    self.assertFalse(self.generator.identifiers.is_declared('greeting'))
    _nodes = []
    _nodes.append(nodes.Output(nodes.Name('greeting', 'load')))
    self.generator.visit(nodes.Template(_nodes))
    self.assertTrue(self.generator.identifiers.is_declared('greeting'))
    expect = """\
def root(dic):
  l_greeting = dic['greeting']
  yield l_greeting\
"""
    self.assertEqual(expect, self.generator.get_code())    
    tmpl = MY_jinja2.Template.from_code(expect)
    self.assertEqual('hello', tmpl.render(greeting='hello'))
  def test_visit_For(self):
    node = nodes.Template([
             nodes.For(
	       nodes.Name('item', 'store'),
	       nodes.Name('seq', 'load'),
	       nodes.Output(nodes.Name('item', 'load'))
	    )
	  ])
    self.generator.visit(node)
    code = self.generator.get_code()
    self.assertEqual("""\
def root(dic):
  l_seq = dic['seq']
  for l_item in l_seq:
    yield l_item\
""", code)
    tpl = MY_jinja2.Template.from_code(code)
    self.assertEqual('one, two, three', tpl.render(seq=['one, ', 'two, ', 'three']))
if __name__ == '__main__':
  test_support.run_unittest(NodeTests)
