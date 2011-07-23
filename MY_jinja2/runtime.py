class Context:
  def __init__(self, blocks, vars={}):
    self.blocks = dict((k, [v])for k, v in blocks.iteritems())
    self.vars = vars
  def resolve(self, key):
    if key in self.vars:
      return self.vars[key]
to_string = unicode
