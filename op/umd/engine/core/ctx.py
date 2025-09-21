from lib.umd.ctx import EngineContext
#from lib.umd.run import EngineRun
from lib.umd.tools.io_umd import imp

from op.umd.engine import toolkit
from op.umd.engine.core.run import Run

class Context(EngineContext):
  @staticmethod
  def load(config, mids=None, path=None, state=None):
    instance = Context(config if isinstance(config, dict) else {}, mids)
    if path:
      state = imp(instance, { 'path': path })
    if state:
      instance.state = state
      instance.run = instance.reg()
    return instance

  def __init__(self, config, mids):
    super().__init__(toolkit)
    self.config = config
    self.mids = mids

  def use(self, input, pipelines):
    proc = []
    for run in self.runs:
      if run:
        for id in pipelines:
          proc.append([run, lambda hooks=None: run.pipe(id, input, hooks=hooks)])
    return lambda handle: list(map(lambda args: handle(*args), proc))

  def reg(self):
    self.runs.append(Run(self, self.state))

# class Context(EngineContext):
#   @staticmethod
#   def load(conf, path=None, state=None):
#     instance = EngineContext(conf)
#     if path:
#       state = imp(instance, { 'path': path })
#     if state:
#       instance.state = state
#       #instance.reg()
    
#     return instance

#   def __init__(self, conf):
#     super().__init__(conf, toolkit)

  # def use(self, input, pipelines):
  #   proc = []
  #   for run in self.runs:
  #     if run:
  #       for id in pipelines:
  #         proc.append([run, lambda: run.pipe(id, input)])
  #   return lambda handle: list(map(lambda args: handle(*args), proc))

  # def reg(self):
  #   self.runs.append(Run(self, self.state))