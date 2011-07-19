class NodeVisitor:
  def visit(self, node):
    try:
      return getattr(self, 'visit_' + node.__class__.__name__)(node)
    except AttributeError:
      pass
    for child in node.iter_child_nodes():
      self.visit(child)


