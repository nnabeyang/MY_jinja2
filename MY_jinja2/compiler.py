from MY_jinja2.visitor import NodeVisitor
import StringIO
from MY_jinja2 import nodes
class CodeGenerator(NodeVisitor):
  def __init__(self):
    self.is_first = True
    self.indent_level = 0
    self.stream = StringIO.StringIO()
  def get_code(self):
    return self.stream.getvalue()
  def indent(self):
    self.indent_level += 1
  def outdent(self):
    self.indent_level -= 1
  def pull_locals(self, node, frame):
    visitor = IdentifierVisitor(frame.identifiers)
    visitor.visit(node)
    for name in frame.identifiers.undeclared:
      self.stream.write("  l_%s = context.resolve('%s')\n" % (name, name))
  def visit_TemplateData(self, node, frame):
    self.stream.write(repr(unicode(node.data)))
  def visit_Output(self, node, frame):
    if not self.is_first:
      self.stream.write('\n')
    self.stream.write('  ' *self.indent_level)
    self.stream.write('yield ')
    self.visit(node.node, frame)
    self.is_first = False
  def visit_Template(self, node, frame):
    blocks = {}
    for block in node.find_all(nodes.Block):
      blocks[block.name] = block
    self.stream.write('from MY_jinja2.runtime import Context\n')
    self.stream.write('def root(context):\n')
    self.pull_locals(node, frame)
    self.indent()
    for child in node.body:
      self.visit(child, frame)
    self.outdent()
    for name, block in blocks.iteritems():
      if not self.is_first:
        self.stream.write('\n')
      self.stream.write('  ' *self.indent_level)
      self.stream.write('def block_%s(context):' % name)
      self.indent()
      block_frame = Frame()
      self.pull_locals(block, block_frame)
      for child in block.body:
        self.visit(child, block_frame)
      self.outdent()
    if not self.is_first:
      self.stream.write('\n')
    self.stream.write('  ' *self.indent_level)
    self.stream.write("blocks = {%s}" % ''.join(
      "'%s': block_%s" % (x, x) for x in blocks))
  def visit_Name(self, node, frame):
    if node.ctxt == 'load' and not frame.identifiers.is_declared(node.name):
      frame.identifiers.declared.add(node.name)
    self.stream.write('l_' + node.name)
  def visit_For(self, node, frame):
    if not self.is_first:
      self.stream.write('\n')
    self.stream.write('  ' *self.indent_level)
    self.stream.write('for ')
    self.visit(node.target, frame)
    self.stream.write(' in ')
    self.visit(node.iter, frame)
    self.stream.write(':')
    self.is_first = False
    self.indent()
    if isinstance(node.body, list):
      for stmt in node.body:
        self.visit(stmt, frame)
    else:
      self.visit(node.body, frame)
    self.outdent()
  def visit_If(self, node, frame):
    if not self.is_first:
      self.stream.write('\n')
    self.stream.write('  ' *self.indent_level)
    self.stream.write('if ')
    self.visit(node.test, frame)
    self.stream.write(':')
    self.is_first = False
    self.indent()
    if isinstance(node.body, list):
      for stmt in node.body:
        self.visit(stmt, frame)
    else:
      self.visit(node.body, frame)
    self.outdent()
  def visit_Block(self, node, frame):
    if not self.is_first:
      self.stream.write('\n')
    self.stream.write('  ' *self.indent_level)
    self.stream.write("for event in context.blocks['%s'][0](context):\n" % node.name)
    self.stream.write('  ' *(self.indent_level+1))
    self.stream.write("yield event")
    self.is_first = False
  def visit_Const(self, node, frame):
    if isinstance(node.value, float):
      self.stream.write(str(node.value))
    else:
      self.stream.write(repr(node.value))
class Frame:
  def __init__(self):
    self.identifiers = Identifiers()
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
