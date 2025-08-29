from lib.mesh.utils import utc

class EngineRun:
  def __init__(self, ctx, state):
    self.ctx = ctx
    self.data = None
    self.id = None
    self.input = None
    self.level = 0
    self.log = []
    self.output = {}
    self.pipeline = None
    self.posts = []
    self.state = state
   
  def __repr__(self):
    return str({
      'id': self.id,
      'ctx': self.ctx,
      'log': self.log,
      'data': self.data,
      'input': self.input,
      'output': self.output,
      'pipeline': self.pipeline
    })


class EngineRunLog:
  def __init__(self, msg, kind, level=0):
    self.kind = kind
    self.level = level
    self.msg = msg
    self.time = utc().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

  def __repr__(self):
    level = '..' * self.level
    return f'{level}{self.time} {self.kind} {self.msg}'

  def use(self):
    return [ str(self), self.kind, self.level, self.time, self.msg ]