#!/usr/bin/env python2.6
import unittest
from test import test_support
import MY_jinja2
import jinja2
class FromStringTests(unittest.TestCase):
  def test_data(self):
    env = self.MODULE.Environment()
    tmpl = env.from_string('hello, world')
    self.assertEqual('hello, world', tmpl.render())
  def test_var(self):
    env = self.MODULE.Environment()
    tmpl = env.from_string('{{greeting}}')
    self.assertEqual('hello', tmpl.render(greeting='hello'))
    self.assertEqual('hi', tmpl.render(greeting='hi'))
  def test_var_data(self):
    env = self.MODULE.Environment()
    tmpl = env.from_string('hello, {{someone}}!!')
    self.assertEqual('hello, world!!', tmpl.render(someone='world'))
    self.assertEqual('hello, nabeyang!!', tmpl.render(someone='nabeyang'))
  def test_for_statement(self):
    env = self.MODULE.Environment()
    tmpl = env.from_string('{% for item in seq %}{{item}}{% endfor %}')
    self.assertEqual('one, two, three', tmpl.render(seq=['one, ', 'two, ', 'three']))
  def test_for_statement_with_data(self):
    env = self.MODULE.Environment()
    data = """\
{% for lang in langs %}hello, {{lang}}
{% endfor %}\
"""
    tmpl = env.from_string(data)
    self.assertEqual("""\
hello, Python
hello, Ruby
hello, Perl
""", tmpl.render(langs=['Python', 'Ruby', 'Perl']))

class FromString_jinja2Tests(FromStringTests):
  MODULE = jinja2
class FromString_MY_jinja2Tests(FromStringTests):
  MODULE = MY_jinja2
if __name__ == '__main__':
  test_support.run_unittest(FromString_jinja2Tests, FromString_MY_jinja2Tests)
