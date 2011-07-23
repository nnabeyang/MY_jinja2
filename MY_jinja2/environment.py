from MY_jinja2.runtime import Context
class Template(object):
  @classmethod
  def from_code(cls, code):
    tpl = object.__new__(cls)
    namespace = {}
    exec code in namespace
    tpl.render_func = namespace['root']
    tpl.blocks = namespace['blocks']
    return tpl
  def render(self, *args, **kwargs):
    dic = dict(*args, **kwargs)
    context = Context(self.blocks, dic)
    return ''.join(self.render_func(context))
from MY_jinja2 import lexer, parser, compiler
class Environment:
  @classmethod
  def from_string(cls, source):
    tokens = lexer.Lexer.tokenize(source)
    stream = lexer.TokenStream(tokens)
    node = parser.Parser.parse(stream)
    generator = compiler.CodeGenerator()
    frame = compiler.Frame()
    generator.visit(node, frame)
    return Template.from_code(generator.get_code())

