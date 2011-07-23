class NodeVisitor:
  def visit(self, node, *args):
    try:
      return getattr(self, 'visit_' + node.__class__.__name__)(node, *args)
    except AttributeError:
      pass
    for child in node.iter_child_nodes():
      self.visit(child, *args)
