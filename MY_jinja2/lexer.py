import operator
TOKEN_VARIABLE_BEGIN = 'variable_begin'
TOKEN_VARIABLE_END = 'variable_end'
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
  @staticmethod
  def tokenize(source):
    c = lambda x: re.compile(x, re.M| re.S)
    e = re.escape
    rules ={
            'root': [
              # variable directive
	      (c(r'(.*?)(?:(?P<variable_begin>{{))'),
	       ('data', 'variable_begin')),
              #data
	      (c(r'(.+)'), 'data')
	      ],
	    'variable_begin': [
                (c(e('}}')), 'variable_end'),
		(c(r'(\b[a-zA-Z_][a-zA-Z0-9_]*\b)'), 'name')
	      ]
	    }
    stack = ['root']
    statetokens = rules[stack[-1]]
    pos = 0
    while 1:
      for regex, tokens in statetokens:
	m = regex.match(source, pos)
        if m is None:
	  continue
	if isinstance(tokens, tuple):
          for idx, token in enumerate(tokens):
	    data = m.group(idx +1)
	    if data == '':
	      continue
	    if token == 'data':
	      yield Token(token, data)
	    elif token == 'variable_begin':
	      for key, value in m.groupdict().iteritems():
	        if value is not None:
		  yield Token(key, value)
	          stack.append(key)
	          break
	      else:
	        raise RuntimeError('no match')
	else:
	  if tokens in ('data', 'name', 'variable_end'):
            yield Token(tokens, m.group())
	    if tokens == 'variable_end':
	      stack.pop()
	  else:
	    raise RuntimeError('unknown token')
	statetokens = rules[stack[-1]]
	pos = m.end()
	break
      else:
        if len(source) <= pos:
          break
