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
  def __repr__(self):
    return '%s(%r, %r)' %(self.__class__.__name__,
                      self.type, self.value)
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
    g = Lexer.tokeniter(source)
    for type, value in g:
      if type == 'whitespace':
        continue
      else:
        yield Token(type, value)
  @staticmethod
  def tokeniter(source):
    c = lambda x: re.compile(x, re.M| re.S)
    e = re.escape
    root_tag_rules = [('variable', '{{'),
                      ('block', '{%')
		   ]
    rules ={
            'root': [
              # variable directive
	      (c(r'(.*?)(?:(?P<variable_begin>{{)|(?P<block_begin>{%))'),
	       ('data', 'variable_begin')),
              #data
	      (c(r'(.+)'), 'data')
	      ],
	    # variable
	    'variable_begin': [
                (c(e('}}')), 'variable_end'),
		(c(r'(\b[a-zA-Z_][a-zA-Z0-9_]*\b)'), 'name')
	      ],
	    # block
	    'block_begin': [
                (c(e('%}')), 'block_end'),
	        (c(r'(\b[a-zA-Z_][a-zA-Z0-9_]*\b)'), 'name'),
	        (re.compile(r'\s+', re.U), 'whitespace')
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
	      yield token, data
	    elif token == 'variable_begin':
	      for key, value in m.groupdict().iteritems():
	        if value is not None:
		  yield key, value
	          stack.append(key)
	          break
	      else:
	        raise RuntimeError('no match')
	else:
	  if tokens in ('data', 'name', 'variable_end', 'block_end', 'whitespace'):
            yield tokens, m.group()
	    if tokens in ('variable_end', 'block_end'):
	      stack.pop()
	  else:
	    raise RuntimeError('%r is unknown token' % tokens)

	statetokens = rules[stack[-1]]
	pos = m.end()
	break
      else:
        if len(source) <= pos:
          break
	raise RuntimeError('unexpected char %s' % source[pos])
