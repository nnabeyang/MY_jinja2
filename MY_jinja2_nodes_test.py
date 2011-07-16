#!/usr/bin/env python2.6
import unittest
from test import test_support
from MY_jinja2 import nodes, compiler

class NodeTests(unittest.TestCase):
  def setUp(self):
    self.generator = compiler.CodeGenerator()
    self.data = '<html><body>hello, world<body></html>'
 
  def test_TemplateDataNode(self):
    node = nodes.TemplateData(self.data)
    self.generator.visit_TemplateData(node)
    self.assertEqual("u'%s'" % self.data, self.generator.get_code())
  def test_OutputNode(self):
    node = nodes.Output(nodes.TemplateData(self.data))
    self.generator.visit_Output(node)
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
    
if __name__ == '__main__':
  test_support.run_unittest(NodeTests)
