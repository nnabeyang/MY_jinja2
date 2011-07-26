class Context:
  def __init__(self, blocks, vars={}):
    self.blocks = dict((k, [v])for k, v in blocks.iteritems())
    self.vars = vars
  def resolve(self, key):
    if key in self.vars:
      return self.vars[key]
  def getattr(self, obj, key):
    try:
      return getattr(obj, key)
    except:
      pass
    return obj[key]

to_string = unicode
