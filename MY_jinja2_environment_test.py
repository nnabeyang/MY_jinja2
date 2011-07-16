#!/usr/bin/env python2.6
import unittest
from test import test_support
import MY_jinja2
class TemplateTests(unittest.TestCase):
  def test_template_from_code(self):
    code = """\
#from MY_jinja2.runtime import to_string
def root(dic):
    l_seq = dic['seq']
    for l_item in l_seq:
        yield unicode(l_item)
"""
    tmpl = MY_jinja2.Template.from_code(code)
    self.assertEqual("0123456789", tmpl.render(seq = range(10)))
  def test_template_from_node(self):
    data = '<html><body>hello, world</body></html>'
    nodes = MY_jinja2.nodes
    node = nodes.Template([nodes.Output(nodes.TemplateData(data))])
    generator = MY_jinja2.CodeGenerator()
    generator.visit_Template(node)
    tmpl = MY_jinja2.Template.from_code(generator.get_code())
    self.assertEqual(data, tmpl.render())
  def test_template_from_node(self):
    data = (
           '<html>\n',
           '<head><title>hello, world</title></head>\n',
           '<body>hello, world</body>\n',
           '</html>\n'
           )
    nodes = MY_jinja2.nodes
    _nodes = []
    for i in data:
      _nodes.append(nodes.Output(nodes.TemplateData(i)))
    node = nodes.Template(_nodes)
    generator = MY_jinja2.CodeGenerator()
    generator.visit_Template(node)
    tmpl = MY_jinja2.Template.from_code(generator.get_code())
    self.assertEqual(''.join(data), tmpl.render())
  def test_template_from_tokens(self):
    Token = MY_jinja2.lexer.Token
    tokens = [
      Token('data', 'hello, '),
      Token('data', 'world')
      ]
    stream = MY_jinja2.lexer.TokenStream(tokens)
    node = MY_jinja2.parser.Parser.parse(stream)
    generator = MY_jinja2.CodeGenerator()
    generator.visit_Template(node)
    tmpl = MY_jinja2.Template.from_code(generator.get_code())
    self.assertEqual('hello, world', tmpl.render())
  def test_template_from_string(self):
    tokens = MY_jinja2.lexer.Lexer.tokenize('hello, world')
    stream = MY_jinja2.lexer.TokenStream(tokens)
    node = MY_jinja2.parser.Parser.parse(stream)
    generator = MY_jinja2.CodeGenerator()
    generator.visit_Template(node)
    tmpl = MY_jinja2.Template.from_code(generator.get_code())
    self.assertEqual('hello, world', tmpl.render())
class EnvironmentTests(unittest.TestCase):
  def test_environment_from_string(self):
    tmpl = MY_jinja2.Environment.from_string('hello, world')
    self.assertEqual('hello, world', tmpl.render())
if __name__ == '__main__':
  test_support.run_unittest(TemplateTests, EnvironmentTests)
