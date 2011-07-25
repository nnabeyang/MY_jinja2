from MY_jinja2 import nodes
from MY_jinja2.lexer import TOKEN_DATA, TOKEN_NAME, TOKEN_VARIABLE_BEGIN, TOKEN_VARIABLE_END
class Parser:
  def parse_statement(self, stream):
    name = next(stream).value
    return getattr(self, 'parse_' + name)(stream)
  def parse_for(self, stream):
    target = nodes.Name(next(stream).value, 'store')
    assert('in' == next(stream).value)
    iter = nodes.Name(next(stream).value, 'load')
    assert('block_end' == next(stream).type)
    body = self.subparse(stream, 'endfor')
    return nodes.For(target, iter, body)
  def parse_if(self, stream):
    test = nodes.Const(next(stream).value in ('true', 'True'))
    assert('block_end' == next(stream).type)
    body = self.subparse(stream, 'endif')
    return nodes.If(test, body)
  def subparse(self, stream, end_token=None):
    body = []
    data_buffer = []
    def flush_data():
      if data_buffer:
        body.append(nodes.Output(data_buffer[:]))
        del data_buffer[:]
    while stream:
      token = next(stream)
      if 'data' == token.type:
        data = nodes.TemplateData(token.value)
        data_buffer.append(data)
      elif 'variable_begin' == token.type:
        token = next(stream)
	assert(TOKEN_NAME == token.type)
	node = nodes.Name(token.value, 'load')
	token = next(stream)
	if 'dot' == token.type:
	  token = next(stream)
	  assert(TOKEN_NAME == token.type)
	  node = nodes.Getattr(
	           node,
	           token.value,
                   'load'
		 )
	  token = next(stream)
	data_buffer.append(node)
	assert(TOKEN_VARIABLE_END == token.type)
      elif 'block_begin' == token.type:
	flush_data()
	if end_token is not None and end_token == next(stream).value:
	  return body
	body.append(self.parse_statement(stream))
        #assert('block_end', stream.current.type)
        next(stream)
      else:
        raise Exception(stream.current)
    flush_data()
    return body
  @staticmethod
  def parse(stream):
    body = Parser().subparse(stream)
    return nodes.Template(body)
