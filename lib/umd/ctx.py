class EngineContext():
  def __init__(self, toolkit):
    self.instances = {}
    self.run = None
    self.runs = []
    self.state = None
    self.toolkit = toolkit

  def __repr__(self):
    return str({
      'instances': self.instances,
      'state': self.state,
      'toolkit': self.toolkit
    })