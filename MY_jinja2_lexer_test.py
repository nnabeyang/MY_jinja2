#!/usr/bin/env python2.6
import unittest
from test import test_support
from MY_jinja2.lexer import *

class TokenTests(unittest.TestCase):
  def test_Token(self):
    data = u'hello, world'
    token = Token(TOKEN_DATA, data)
    self.assertEqual(TOKEN_DATA, token.type)
    self.assertEqual(data, token.value)
  def test_Tokens(self):
    token1 = Token(TOKEN_DATA, 'hello')
    token2 = Token(TOKEN_NAME, 'world')
    self.assertEqual(TOKEN_DATA, token1.type)
    self.assertEqual('hello', token1.value)    
    self.assertEqual(TOKEN_NAME, token2.type)
    self.assertEqual('world', token2.value) 
  def test_Token_is_readonly(self):
    data = u'hello, world'
    token = Token('data', data)
    def f_value(token):
      token.value = 'value'
    def f_type(token):
      token.type = 'type'
    self.assertRaises(AttributeError, f_value, token)
    self.assertRaises(AttributeError, f_type, token)
  def test_TokenStream(self):
    tokens = [
      Token(TOKEN_DATA, 'hello'),
      Token(TOKEN_NAME, 'world')
      ]
    stream = TokenStream(tokens)
    self.assertEqual(Token(TOKEN_DATA, 'hello'), next(stream))
    self.assertEqual(Token(TOKEN_NAME, 'world'), next(stream))
    self.assertEqual(Token(TOKEN_EOF, ''), next(stream))
    self.assertEqual(Token(TOKEN_EOF, ''), next(stream))
  def test_TokenStream_nonzero(self):
   tokens = [
      Token(TOKEN_DATA, 'hello'),
      Token(TOKEN_NAME, 'world')
      ]
   result = []
   stream = TokenStream(tokens)
   while stream:
     result.append(next(stream))
   self.assertEqual(tokens, result)
class LexerTests(unittest.TestCase):
  def test_tokenize_data(self):
    generator = Lexer.tokenize("hello, world")
    result = []
    for token in generator:
      result.append(token)
    expect = [Token(TOKEN_DATA, 'hello, world'), ]
    self.assertEqual(expect, result)
  def test_tokenize_var(self):
    generator = Lexer.tokenize('{{greeting}}')
    result = []
    for token in generator:
      result.append(token)
    expect = [
      Token('variable_begin', '{{'),
      Token('name', 'greeting'),
      Token('variable_end', '}}'),
    ]
    self.assertEqual(expect, result)
  def test_tokenize_var_and_data(self):
    generator = Lexer.tokenize('hello, {{greeting}}!!')
    result = []
    for token in generator:
      result.append(token)
    expect = [
      Token('data', 'hello, '),
      Token('variable_begin', '{{'),
      Token('name', 'greeting'),
      Token('variable_end', '}}'),
      Token('data', '!!'),
    ]
    self.assertEqual(expect, result)
  def test_tokenize_for_statement(self):
    generator = Lexer.tokenize('{% for item in seq %}{{item}}{% endfor %}')
    result = []
    for token in generator:
      result.append(token)
    expect = [
      Token('block_begin', u'{%'),
      Token('name', 'for'),
      Token('name', 'item'),
      Token('name', 'in'),
      Token('name', 'seq'),
      Token('block_end', u'%}'),
      Token('variable_begin', u'{{'),
      Token('name', 'item'),
      Token('variable_end', u'}}'),
      Token('block_begin', u'{%'),
      Token('name', 'endfor'),
      Token('block_end', u'%}')
    ]
    self.assertEqual(expect, result)


if __name__ == '__main__':
  test_support.run_unittest(TokenTests, LexerTests)
