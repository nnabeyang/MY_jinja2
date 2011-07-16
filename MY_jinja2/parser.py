from MY_jinja2 import nodes
from MY_jinja2.lexer import TOKEN_DATA
class Parser:
  @classmethod
  def parse(cls, stream):
    body = []
    while stream:
      token = next(stream)
      assert(TOKEN_DATA == token.type)
      data = nodes.TemplateData(token.value)
      body.append(nodes.Output(data))
    return nodes.Template(body)
