import json

from datetime import datetime, timedelta
from time import gmtime, struct_time

from lib.umd.umd import UMDState, UMDCommandState, UMDPipelineState, UMDUseState
from lib.umd import eval

class BaseParser:
  def __init__(self, ctx, section, state):
    self.ctx = ctx
    self.section = section
    self.state = state

  def contextify(self):
    if self.section.parents and len(self.section.parents) > 0:
      parent = self.section.parents[0]
      id = parent.props['id'] if 'id' in parent.props else None
      if id:
        return self.state.pipelines[id] if id in self.state.pipelines else None
    return None

  def resolve(self, value):
    if value and value[0] == '[' and value[-1] == ']':
      return value[1:-1].split('/')
    return value


class CommandParser(BaseParser):
  def match(self, path):
    return path == 'umd/pipeline/cmd'

  def parse(self):
    def format(section):
      data = {
        **section.props,
        'config': list(map(lambda child: format(child), section.children)),
        'content': section.content,
        'type': section.type,
        'value': section.value
      }
      for key, value in data.items():
        if key in data and data[key]:
          data[key] = self.resolve(value)
      return data

    state = self.contextify()
    if state and 'path' in self.section.props:
      id = self.section.props['id'] if 'id' in self.section.props else None
      input = None
      for child in self.section.children:
        if child.type == 'input':
          input = format(child)
          break
      path = self.resolve(self.section.props['path'])
      state.commands.append(UMDCommandState(path, id, input))


class ModelParser(BaseParser):
  def __init__(self, ctx, section, state):
    super().__init__(ctx, section, state)
    self.types = {
      #'date': lambda value: datetime.strptime(value, '%d/%m/%y'),
      'date': lambda value: value.date(),
      'datetime': lambda value: datetime.fromisoformat(value),
      'float': lambda value: float(value),
      'int': lambda value: int(value),
      'str': lambda value: str(value),
      'time': lambda value: gmtime(value)
      #'time': lambda value: time.strptime(value, '%H:%M:%S')
    }

  def match(self, path):
    return path == 'umd/setup/model'

  def parse(self):
    result = {}
    if self.section.children and len(self.section.children) > 0:
      self.scan(self.section.children[0], result)
    self.state.models[self.section.props['id']] = result

  def scan(self, section, result):
    prop = section.type
    if prop:
      current = result
      for key, value in section.props.items():
        if key == 'type':
          if value == 'obj':
            result[prop] = {}
            current = result[prop]
          elif value == 'arr':
            result[prop] = []
            current = {}
            result[prop].append(current)
          else:
            result[prop] = self.types[value] if value in self.types else self.types['str']
      if section.children:
        for child in section.children:
          self.scan(child, current)


class PipelineParser(BaseParser):
  def match(self, path):
    return path == 'umd/pipeline'

  def parse(self):
    id = self.section.props['id'] if 'id' in self.section.props else None
    if id:
      self.state.pipelines[id] = UMDPipelineState(id)


class UseParser(BaseParser):
  def match(self, path):
    return path == 'umd/pipeline/use'

  def parse(self):
    state = self.contextify()
    if state and 'path' in self.section.props:
      id = self.section.props['id'] if 'id' in self.section.props else None
      load = None
      if 'load' in self.section.props:
        load = self.resolve(self.section.props['load'])
      path = self.resolve(self.section.props['path'])
      state.use[id] = UMDUseState(path, id, load, self.section.props)


class VarParser(BaseParser):
  def match(self, path):
    return path == 'umd/pipeline/var'

  def parse(self):
    state = self.contextify()
    section = self.section
    if state and 'id' in section.props:
      id = section.props['id']
      handler = section.props['eval'] if 'eval' in section.props else None
      if handler:
        value = lambda payload: eval.code(f'output = {handler}', payload=payload)
      else:
        value = self.resolve(section.props['value'] if 'value' in section.props else section.value)
      state.vars[id] = value
    


handlers = [
  ModelParser,
  PipelineParser,
  CommandParser,
  UseParser,
  VarParser
]

def load(ctx, sections):
  state = UMDState()
  for section in sections:
    for handler in handlers:
      parser = handler(ctx, section, state)
      if parser.match(section.path):
        parser.parse()
  return state