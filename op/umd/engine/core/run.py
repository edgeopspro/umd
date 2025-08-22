from copy import deepcopy

from lib.umd.run import EngineRun, EngineRunLog
from lib.umd import path
from lib.umd import utils

class Run(EngineRun):
  def __init__(self, ctx, state):
    super().__init__(ctx, state)
    self.hooks = {}
    self.resolver = {
      'cmd': lambda: self.data if self.data else None,
      'input': self.input,
      'log': self.log,
      'model': self.state.models,
      'pipe': self.state.pipelines,
      'output': self.output,
      'use': self.ctx.instances,
      'var': lambda : self.pipeline.vars if self.pipeline else None
    }

  def logger(self, msg, kind):
    if msg:
      value = lambda: EngineRunLog(msg, kind, self.level)
      self.log.append(value)
      hook = self.hooks['log'] if 'log' in self.hooks else None
      if callable(hook):
        hook(value)

  def err(self, msg):
    self.logger(msg, 'ERR')

  def info(self, msg):
    self.logger(msg, 'INF')

  def warn(self, msg):
    self.logger(msg, 'WRN')

  def update(self, id, data):
    self.output[id] = data

  def resolve(self, value, uid=None):
    if isinstance(value, list) and len(value) > 0:
      origin = value[0]
      if isinstance(origin, str):
        if origin in self.resolver:
          handler = self.resolver[origin]
          if callable(handler):
            data = handler()
          else:
            data = handler
          result = path.resolve(data, value[1:])
          if not result and uid:
            value[0] = uid
            use = '/'.join(value)
            if use in self.output:
              return self.output[use]
            else:
              return value
          return result
    return None

  def pipe(self, id, input, uid=None, hooks=None):
    def resolve(input):
      for key, value in input.items():
        resolved = self.resolve(value, uid)          
        input[key] = resolved if resolved else value
      return input

    self.ctx.run = self
    if isinstance(hooks, dict):
      self.hooks = hooks
    if self.level == 0:
      self.id = utils.uid()[0:12]
      self.info(f'starting run {self.id}')
    if isinstance(input, dict):
      self.input = deepcopy(input)
      if uid:
        self.input['uid'] = uid
      self.info(f'using input {self.input}')
      if id in self.state.pipelines:
        self.info(f'using pipeline with id "{id}"')
        self.pipeline = pipeline = deepcopy(self.state.pipelines[id])
        for key, value in self.input.items():
          if key in pipeline.vars:
            pipeline.vars[key] = value
        for key, value in pipeline.vars.items():
          if callable(value):
            pipeline.vars[key] = value(self.input)
        for id, handler in pipeline.use.items():
          self.info(f'loading resource "{id}"')
          valid = False
          if handler.load:
            tool = self.ctx.toolkit.resolve(handler.load)
            if callable(tool):
              try:
                self.info(f'loading tool found for "{id}" with path {handler.load}')
                valid = True
                self.data = resolve({ 'path': handler.path })
                print('-------', handler.path, self.data, self.ctx)
                self.ctx.instances[id] = tool(self.ctx, self.data)
                self.info(f'resource "{id}" load completed')
              except Exception as error:
                self.err(error)
          if not valid:
            self.warn(f'resource "{id}" has invalid "load" property')
        for cmd in pipeline.commands:
          postfix = ''
          if cmd.id:
            postfix = f' ({cmd.id})'
          self.info(f'starting command for path {cmd.path}' + postfix)
          tool = self.ctx.toolkit.resolve(cmd.path)
          if callable(tool):
            try:
              self.info(f'using command tool {cmd.path}')
              self.data = resolve(cmd.input)
              output = tool(self.ctx, self.data)
              if cmd.id:
                kind = type(output).__name__
                if kind == 'NoneType':
                  kind = None
                if uid:
                  cmd.id = f'{uid}/{cmd.id}'
                self.info(f'updating output of type "{kind}" with id "{cmd.id}"')
                self.update(cmd.id, output)
              self.info(f'command with path {cmd.path} completed' + postfix)
            except Exception as error:
              self.err(error)
          else:
            self.warn(f'command path {cmd.path} is not valid')
      else:
        self.warn(f'pipeline with id {id} does not exists in current state')
    else:
      self.warn(f'input "{self.input}" must be an object')
    if self.level == 0:
      self.info(f'stopping run {self.id}')
      for action in self.posts:
        if callable(action):
          action()
      self.info(f'post actions completed for run {self.id}')