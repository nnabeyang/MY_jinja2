from MY_jinja2 import nodes
from MY_jinja2.lexer import TOKEN_DATA, TOKEN_NAME, TOKEN_VARIABLE_BEGIN, TOKEN_VARIABLE_END
class Parser:
  @staticmethod
  def parse(stream):
    body = []
    while stream:
      token = next(stream)
      if TOKEN_DATA == token.type:
        data = nodes.TemplateData(token.value)
        body.append(nodes.Output(data))
      elif TOKEN_VARIABLE_BEGIN == token.type:
        token = next(stream)
	assert(TOKEN_NAME == token.type)
	body.append(nodes.Output(nodes.Name(token.value, 'load')))
	assert(TOKEN_VARIABLE_END == next(stream).type)
      else:
        raise(Exception)

    return nodes.Template(body)
