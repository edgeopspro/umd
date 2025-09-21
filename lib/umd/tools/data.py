from copy import deepcopy

from lib.umd.eval import code, run

def map(ctx, input):
  def format(model, target, warn=False):
    if isinstance(model, list) and len(model) > 0:
      proto = model[0]
      if isinstance(proto, dict) and isinstance(target, list):
        for item in target:
          format(list(proto.values())[0], item)
      elif warn:
        ctx.run.warn(f'"mismatch between model and target')
    elif isinstance(model, dict):
      for key, value in model.items():
        if isinstance(target, list):
          target = target[0]
        if key in target:
          if callable(model[key]):
            target[key] = model[key](target[key])
          else:
            format(model[key], target[key])
        elif warn:
          ctx.run.warn(f'"{key} present in model but not in target')

  def resolve(source, segments, paths, target, format=None):
    if len(segments) > 0:
      segment = segments[0]
      next = source[segment] if isinstance(source, dict) and segment in source else source if isinstance(source, list) else None
      if isinstance(next, list):
        insert = len(target) == 0
        for index, item in enumerate(next):
          value = resolve(item, segments[1:], paths[1:], [], format)
          if not format:
            if insert:
              target.append(value)
            elif value:
              target[index] = { **target[index], **value }
      else:
        path = paths[0]
        if format:
          source[path] = format(next)
        else:
          value = { path: format(next) if callable(format) else next }
          return value
        
  model = deepcopy(input['model']) if 'model' in input else None
  output = {} if isinstance(model, dict) else []
  use = {}
  for config in input['config']:
    if config['type'] == 'use':
      key = list(config)[0]
      value = ctx.run.resolve(config[key])
      use[key] = value
  for config in input['config']:
    exp = config['content']
    kind = config['type']
    if kind == 'copy':
      source = config['source'] if 'source' in config else None
      target = config['target'] if 'target' in config else None
      if isinstance(source, list) and isinstance(target, list):
        if model:
          nextmod = model
          nextout = output
          while len(target) > len(source):
            path = target.pop(0)
            if path in nextmod:
              if not path in nextout:
                nextout[path] = {} if isinstance(nextmod[path], dict) else []
              nextout = nextout[path]
              nextmod = nextmod[path]
        resolve(use, source, target, nextout)
    elif kind == 'eval':
      if exp:
        output = run(exp, payload={ 'data': output, 'use': use })
    elif kind == 'format':
      path = config['path'] if 'path' in config else None
      if path:
        output = use[path.pop(0)]
        resolve(output, path, path, output, lambda value: code(exp, payload={ 'value': value }))
  if model:
    format(model, output, True)
  return output