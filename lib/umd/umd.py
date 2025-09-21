class UMDSection:
  def __init__(self, source, path, parents):
    self.content = source.text if source.text else ''
    self.children = list(map(lambda node: UMDSection(node, None, None), source.findall('*')))
    self.parents = list(map(lambda node: UMDSection(node, None, None), parents)) if parents else None
    self.path = path
    self.props = source.attrib
    self.type = source.tag
    self.value = self.content.strip()

  def __repr__(self):
    def format(collection):
      return list(map(lambda section: section.type, collection)) if collection else []

    return str({ 
      'content': self.content,
      'children': format(self.children),
      'parents': format(self.parents),
      'path': self.path,
      'props': self.props,
      'type': self.type,
      'value': self.value
    })


class UMDState:
  def __init__(self, models=None, pipelines=None):
    self.models = models if isinstance(models, dict) else {}
    self.pipelines = pipelines if isinstance(pipelines, dict) else {}

  def __repr__(self):
    return str({
      'models': self.models,
      'pipelines': self.pipelines
    })


class UMDCommandState:
  def __init__(self, path, id=None, input=None):
    self.id = id
    self.input = input
    self.path = path

  def __repr__(self):
    return str({
      'path': self.path,
      'id': self.id,
      'input': self.input
    })

class UMDPipelineState:
  def __init__(self, id):
    self.id = id
    self.commands = []
    self.use = {}
    self.vars = {}

  def __repr__(self):
    return str({
      'id': self.id,
      'cmds': self.commands,
      'use': self.use,
      'vars': self.vars
    })

class UMDUseState:
  def __init__(self, path, id=None, load=None):
    self.id = id
    self.load = load
    self.path = path

  def __repr__(self):
    return str({
      'path': self.path,
      'id': self.id,
      'load': self.load
    })