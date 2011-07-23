from MY_jinja2.visitor import NodeVisitor
import StringIO
class CodeGenerator(NodeVisitor):
  def __init__(self):
    self.is_first = True
    self.indent_level = 0
    self.stream = StringIO.StringIO()
    self.identifiers = Identifiers()
  def get_code(self):
    return self.stream.getvalue()
  def indent(self):
    self.indent_level += 1
  def outdent(self):
    self.indent_level -= 1
  def pull_locals(self, node):
    visitor = IdentifierVisitor(self.identifiers)
    visitor.visit(node)
    for name in self.identifiers.undeclared:
      self.stream.write("  l_%s = context.resolve('%s')\n" % (name, name))
  def visit_TemplateData(self, node):
    self.stream.write(repr(unicode(node.data)))
  def visit_Output(self, node):
    if not self.is_first:
      self.stream.write('\n')
    self.stream.write('  ' *self.indent_level)
    self.stream.write('yield ')
    self.visit(node.node)
    self.is_first = False
  def visit_Template(self, node):
    self.stream.write('from MY_jinja2.runtime import Context\n')
    self.stream.write('def root(context):\n')
    self.indent()
    self.pull_locals(node)
    for child in node.body:
      self.visit(child)
    self.outdent()

    if not self.is_first:
      self.stream.write('\n')
    self.stream.write('  ' *self.indent_level)
    self.stream.write('blocks = {}')
  def visit_Name(self, node):
    if node.ctxt == 'load' and not self.identifiers.is_declared(node.name):
      self.identifiers.declared.add(node.name)
    self.stream.write('l_' + node.name)
  def visit_For(self, node):
    if not self.is_first:
      self.stream.write('\n')
    self.stream.write('  ' *self.indent_level)
    self.stream.write('for ')
    self.visit(node.target)
    self.stream.write(' in ')
    self.visit(node.iter)
    self.stream.write(':')
    self.is_first = False
    self.indent()
    if isinstance(node.body, list):
      for stmt in node.body:
        self.visit(stmt)
    else:
      self.visit(node.body)
    self.outdent()
class Identifiers:
  def __init__(self):
    self.declared = set()
    self.undeclared = set()
  def is_declared(self, name):
    if name in self.declared:
      return True
    return False
class IdentifierVisitor(NodeVisitor):
  def __init__(self, identifiers):
    self.identifiers = identifiers
  def visit_Name(self, node):
    if node.ctxt == 'load' and not self.identifiers.is_declared(node.name):
      self.identifiers.undeclared.add(node.name)
    elif node.ctxt == 'store':
      self.identifiers.declared.add(node.name)
