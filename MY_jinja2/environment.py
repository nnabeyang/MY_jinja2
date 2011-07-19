class Template(object):
  @classmethod
  def from_code(cls, code):
    tpl = object.__new__(cls)
    namespace = {}
    exec code in namespace
    tpl.render_func = namespace['root']
    return tpl
  def render(self, *args, **kwargs):
    dic = dict(*args, **kwargs)
    return ''.join(self.render_func(dic))
from MY_jinja2 import lexer, parser, compiler
class Environment:
  @classmethod
  def from_string(cls, source):
    tokens = lexer.Lexer.tokenize(source)
    stream = lexer.TokenStream(tokens)
    node = parser.Parser.parse(stream)
    generator = compiler.CodeGenerator()
    generator.visit(node)
    return Template.from_code(generator.get_code())

