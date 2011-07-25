import itertools
class Impossible(Exception):
  pass
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
  def find_all(self, node_type):
    for node in self.iter_child_nodes():
      if(isinstance(node, node_type)):
        yield node
      for n in node.find_all(node_type):
        yield n
  def as_const(self):
    raise Impossible(repr(self))
class Template(Node):
  fields = ('body',)
class TemplateData(Node):
  fields = ('data',)
  def as_const(self):
    return self.data
class Output(Node):
  fields = ('nodes',)
class Name(Node):
  fields = ('name', 'ctxt')
class For(Node):
  fields = ('target', 'iter', 'body')
class If(Node):
  fields = ('test', 'body')
class Block(Node):
  fields = ('name', 'body')
class Const(Node):
  fields = ('value',)
  def as_const(self):
    return self.value
class Assign(Node):
  fields = ('target', 'node')
class Getattr(Node):
  fields = ('node', 'attr', 'ctxt')
