#!/usr/bin/env python2.6
import unittest
from test import test_support
from MY_jinja2.runtime import Context
class ContextTests(unittest.TestCase):
  def test_blocks(self):
    def block_foo(ctxt):
      yield u'...'
    blocks = {'foo': block_foo}
    context = Context(blocks)
    self.assertEqual('...', ''.join(context.blocks['foo'][0](context)))
  def test_resolve(self):
    context = Context({}, {'foo': 1, 'bar': 2})
    self.assertEqual(1, context.resolve('foo'))
    self.assertEqual(2, context.resolve('bar'))
    self.assertEqual(None, context.resolve('no-such-key'))

if __name__ == '__main__':
  test_support.run_unittest(ContextTests)
