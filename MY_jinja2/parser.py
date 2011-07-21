from MY_jinja2 import nodes
from MY_jinja2.lexer import TOKEN_DATA, TOKEN_NAME, TOKEN_VARIABLE_BEGIN, TOKEN_VARIABLE_END
class Parser:
  @staticmethod
  def parse_for(stream):
    assert('for' == next(stream).value)
    target = nodes.Name(next(stream).value, 'store')
    assert('in' == next(stream).value)
    iter = nodes.Name(next(stream).value, 'load')
    assert('block_end' == next(stream).type)
    body = Parser.subparse(stream, 'endfor')
    return nodes.For(target, iter, body)
  @staticmethod
  def subparse(stream, end_token=None):
    body = []
    while stream:
      token = next(stream)
      if 'data' == token.type:
        data = nodes.TemplateData(token.value)
        body.append(nodes.Output(data))
      elif 'variable_begin' == token.type:
        token = next(stream)
	assert(TOKEN_NAME == token.type)
	body.append(nodes.Output(nodes.Name(token.value, 'load')))
	assert(TOKEN_VARIABLE_END == next(stream).type)
      elif 'block_begin' == token.type:
	if end_token is not None and end_token == next(stream).value:
	  return body
	body.append(Parser.parse_for(stream))
        assert('block_end', stream.current.type)
        next(stream)
      else:
        raise Exception(stream.current)
      if end_token is not None and end_token == stream.current.type:
        return body
    return body
  @staticmethod
  def parse(stream):
    body = Parser.subparse(stream)
    return nodes.Template(body)
