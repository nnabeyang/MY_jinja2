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
      elif 'block_begin' == token.type:
	assert('for' == next(stream).value)
	for_target = next(stream)
	assert('in' == next(stream).value)
	for_iter = next(stream)
	assert('block_end' == next(stream).type)
	assert('variable_begin' == next(stream).type)
	for_body = next(stream)
	assert('variable_end' == next(stream).type)

	assert('block_begin' == next(stream).type)
	assert('endfor' == next(stream).value)
	assert('block_end' == next(stream).type)
	body.append(nodes.For(
	  nodes.Name(for_target.value, 'store'),
	  nodes.Name(for_iter.value, 'load'),
	  nodes.Output(nodes.Name(for_body.value, 'load'))
	  )
        )
      else:
        raise Exception()
    return nodes.Template(body)
