#!/usr/bin/env python2.6
import unittest
from test import test_support
from MY_jinja2 import nodes, compiler, Template
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
    code = self.generator.get_code()
    tpl = Template.from_code(code)
    self.assertEqual(self.data, tpl.render())
  def test_TemplateNode_from_multi_nodes(self):
    data = ('<html>\n',
             '<head><title>hello, world</title></head>\n',
             '<body>hello, world</body>\n',
             '</html>\n'
	     )
    _nodes = []
    _nodes.append(nodes.Output(nodes.TemplateData(data[0])))
    _nodes.append(nodes.Output(nodes.TemplateData(data[1])))
    _nodes.append(nodes.Output(nodes.TemplateData(data[2])))
    _nodes.append(nodes.Output(nodes.TemplateData(data[3])))
    self.generator.visit_Template(nodes.Template(_nodes))
    code = self.generator.get_code()
    #print code
    tpl = Template.from_code(code)
    self.assertEqual(''.join(data), tpl.render())
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
    code = self.generator.get_code()
    #print code
    tpl = Template.from_code(code)
    self.assertEqual('hello', tpl.render(greeting='hello'))
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
    #print code
    tpl = Template.from_code(code)
    self.assertEqual('one, two, three', tpl.render(seq=['one, ', 'two, ', 'three']))
  def test_visit_For_with_data(self):
    node = nodes.Template([
             nodes.For(
               nodes.Name('lang', 'store'),
	       nodes.Name('langs', 'load'),
	       [
	         nodes.Output(nodes.TemplateData(u'hello, ')),
	         nodes.Output(nodes.Name('lang', 'load')),
		 nodes.Output(nodes.TemplateData(u'\n'))
	       ]
	      )
	   ])
    self.generator.visit(node)
    code = self.generator.get_code()
    tpl = MY_jinja2.Template.from_code(code)
    self.assertEquals("""\
hello, Python
hello, Ruby
hello, Perl
""", tpl.render(langs=['Python', 'Ruby', 'Perl']))
  def test_node_find_all(self):
    body = []
    for i in range(7):
      body.append(nodes.Block('%d' % i, [nodes.Output([nodes.TemplateData(u'...')])]))
    body.append(
      nodes.For(
               nodes.Name('lang', 'store'),
	       nodes.Name('langs', 'load'),
	       [
	         nodes.Output(nodes.TemplateData(u'hello, ')),
	         nodes.Output(nodes.Name('lang', 'load')),
	         nodes.Block('foo', [nodes.Output([nodes.TemplateData(u'...')])])
	       ]
	      ))
    node = nodes.Template(body)
    expect = []
    for i in range(7):
      expect.append(nodes.Block('%d' % i, [nodes.Output([nodes.TemplateData(u'...')])]))
    expect.append(nodes.Block('foo', [nodes.Output([nodes.TemplateData(u'...')])]))
    self.assertEqual(expect,  list(node.find_all(nodes.Block)))

if __name__ == '__main__':
  test_support.run_unittest(NodeTests)
