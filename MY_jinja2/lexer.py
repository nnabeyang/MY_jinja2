import operator
TOKEN_NAME = 'name'
TOKEN_DATA = 'data'
TOKEN_INITIAL = 'initial'
TOKEN_EOF = 'eof'
class Token(tuple):
  type, value = (property(operator.itemgetter(x)) for x in range(2))
  def __new__(cls, type, value):
    return tuple.__new__(cls, (type, value))
class TokenStream:
  def __init__(self, iter_tokens):
    self._next = iter(iter_tokens).next
    self.current = Token(TOKEN_INITIAL, '')
    next(self)
  def __nonzero__(self):
    return self.current.type is not TOKEN_EOF
  def next(self):
    token = self.current
    if token.type is not TOKEN_EOF:
      try:
        self.current = self._next()
      except StopIteration:
        self.current = Token(TOKEN_EOF, '')
    return token
import re
class Lexer:
  @classmethod
  def tokenize(cls, source):
    regex = re.compile('(.+)', re.M| re.S)
    while 1:
      m = regex.match(source)
      yield Token(TOKEN_DATA, m.group())
      if len(source) <= m.end():
        break
