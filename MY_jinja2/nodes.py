import itertools
class NodeType(type):
  def __new__(cls, name, bases, d):
    assert(len(bases) == 1)
    return type.__new__(cls, name, bases, d)
class Node(object):
  __metaclass__ = NodeType
  def __init__(self, *fields):
    assert len(self.fields) == len(fields)
    for key, value in itertools.izip(self.fields, fields):
      setattr(self, key, value)
  def __eq__(self, node):
    return type(self) is type(node) and \
      tuple(self.iter_fields()) == tuple(node.iter_fields())
  def __neq__(self, node):
    return not self.__eq__(node)
  def __repr__(self):
    return '%s(%s)' %(
      self.__class__.__name__,
      ', '.join('%s=%r' % (field, getattr(self, field, None))
        for field in self.fields)
      )
  def iter_fields(self):
    for field in self.fields:
      yield field, getattr(self, field)
  def iter_child_nodes(self):
    for field, item in self.iter_fields():
      if isinstance(item, Node):
        yield item
      elif isinstance(item, list):
        for item_elem in item:
	  yield item_elem
class Template(Node):
  fields = ('body',)
class TemplateData(Node):
  fields = ('data',)
class Output(Node):
  fields = ('node',)
class Name(Node):
  fields = ('name', 'ctxt')
