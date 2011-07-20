#!/usr/bin/env python2.6
import unittest
from test import test_support
import MY_jinja2
import jinja2
class APITests(unittest.TestCase):  
  def test_from_string_data(self):
    env = self.MODULE.Environment()
    tmpl = env.from_string('hello, world')
    self.assertEqual('hello, world', tmpl.render())
  def test_from_string_var(self):
    env = self.MODULE.Environment()
    tmpl = env.from_string('{{greeting}}')
    self.assertEqual('hello', tmpl.render(greeting='hello'))
    self.assertEqual('hi', tmpl.render(greeting='hi'))
  def test_from_string_var_data(self):
    env = self.MODULE.Environment()
    tmpl = env.from_string('hello, {{someone}}!!')
    self.assertEqual('hello, world!!', tmpl.render(someone='world'))
    self.assertEqual('hello, nabeyang!!', tmpl.render(someone='nabeyang'))



class API_jinja2Tests(APITests):
  MODULE = jinja2
class API_MY_jinja2Tests(APITests):
  MODULE = MY_jinja2
if __name__ == '__main__':
  test_support.run_unittest(API_jinja2Tests, API_MY_jinja2Tests)
