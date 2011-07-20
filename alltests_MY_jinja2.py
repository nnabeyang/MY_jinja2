#!/usr/bin/env python2.6
import unittest
from test import test_support
from MY_jinja2_environment_test import TemplateTests, EnvironmentTests
from MY_jinja2_nodes_test import NodeTests
from MY_jinja2_lexer_test import TokenTests
from MY_jinja2_parser_test import ParserTests
from MY_jinja2_compiler_test import CompilerTests
from jinja2_api_test import FromString_jinja2Tests, FromString_MY_jinja2Tests
if __name__ == '__main__':
  test_support.run_unittest(TemplateTests,EnvironmentTests,
  NodeTests, TokenTests, ParserTests, CompilerTests,
  FromString_jinja2Tests, FromString_MY_jinja2Tests)
