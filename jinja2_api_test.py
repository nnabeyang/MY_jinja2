#!/usr/bin/env python2.6
import unittest
from test import test_support
import MY_jinja2
import jinja2
class APITests(unittest.TestCase):  
  def test_from_data(self):
    env = self.MODULE.Environment()
    tmpl = env.from_string('hello, world')
    self.assertEqual('hello, world', tmpl.render())
class API_jinja2Tests(APITests):
  MODULE = jinja2
class API_MY_jinja2Tests(APITests):
  MODULE = MY_jinja2
if __name__ == '__main__':
  test_support.run_unittest(API_jinja2Tests, API_MY_jinja2Tests)
