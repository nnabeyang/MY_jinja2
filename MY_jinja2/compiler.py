import StringIO
class CodeGenerator:
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
  def visit_TemplateData(self, node):
    self.stream.write(repr(unicode(node.data)))
  def visit_Output(self, node):
    if not self.is_first:
      self.stream.write('\n')
    self.stream.write('  ' *self.indent_level)
    self.stream.write('yield ')
    self.visit_TemplateData(node.node)
    self.is_first = False
  def visit_Template(self, node):
    self.stream.write('def root(dic):\n')
    self.indent()
    for child in node.body:
      self.visit_Output(child)
    self.outdent()
  visit = visit_Template
