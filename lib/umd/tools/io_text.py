from lib.umd.fs import read

tokens = [ '\n', '{{', '}}', '{{{', '}}}' ]

def format(ctx, input):
  def arr(template, items, path):
    results = []
    for item in items:
      results.append(obj(template, item, path))
    return tokens[0].join(results)

  def obj(template, item, path):
    for key, value in item.items():
      next = path + [ key ]
      if isinstance(value, list):
        exp = token(next, index=3)
        length = len(exp)
        start = 0
        while start > -1:
          start = template.find(exp)
          if start > -1:
            stop = template.find(exp, start + length)
            if stop > -1:
              template = template[0:start] + arr(template[start + length:stop], value, []) + template[stop + length:]
            else:
              start = -1
      elif isinstance(value, dict):
        template = obj(template, value, next)
      else:
        template = render(template, next, value)
    return template

  def render(template, path, value):
    return template.replace(token(path), str(value))

  def token(path, index=1):
    key = '.'.join(path)
    return f'{tokens[index]}{key}{tokens[index + 1]}'
  
  if 'config' in input:
    config = input['config']
    template = None
    if 'source' in input:
      template = read(input['source'])
    elif 'template' in input:
      template = input['template']
    if config and template:
      for handler in config:
        if handler['type'] == 'use':
          key = list(handler)[0]
          value = ctx.run.resolve(handler[key])
          if isinstance(value, dict):
            template = obj(template, value, [ key ])
          else:
            template = render(template, [ key ], value)
      
      return template
  return None