#!/usr/bin/env python2.6
import unittest
from test import test_support
from environment import TemplateTests, EnvironmentTests
from nodes import NodeTests
from lexer import TokenTests
from parser import ParserTests
from compiler import CompilerTests
from runtime import ContextTests
from jinja2_api_test import FromString_jinja2Tests, FromString_MY_jinja2Tests
if __name__ == '__main__':
  test_support.run_unittest(TemplateTests,EnvironmentTests,
  NodeTests, TokenTests, ParserTests, CompilerTests,
  ContextTests,
  FromString_jinja2Tests, FromString_MY_jinja2Tests)
