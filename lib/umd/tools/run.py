from lib.umd.utils import uid

def pipeline(ctx, input):
  config = input['config']
  id = input['id'] if 'id' in input else None
  parent = ctx.run.pipeline.id
  if id and parent:
    max = 0
    values = {}
    for handler in config:
      if handler['type'] == 'var': 
        value = handler['value']
        resolved = ctx.run.resolve(value)
        value = resolved if resolved else value
        values[handler['id']] = { 
          'mult': isinstance(value, list),
          'value': value,
          'use': [ ]
        }
        if isinstance(value, list):
          count = len(value)
          if count > max:
            max = count
    iterations = [ None ] * max
    for key, handler in values.items():
      value = handler['value']
      if handler['mult']:
        count = max - len(value)
        if count > 0:
          handler['use'] = [ None ] * max
          for index, item in enumerate(value):
            handler['use'][index] = item
        else:
          handler['use'] = value
      else:
        handler['use'] = [ value ] * max
    pipeline = ctx.run.pipeline
    for index, _ in enumerate(iterations):
      iteration = {}
      for key, handler in values.items():
        iteration[key] = handler['use'][index]
      puid = uid()[0:6]
      prefix = f'iteration #{index + 1}:'
      ctx.run.info(f'{prefix} starting pipeline "{id}" (origin pipeline: "{parent}", execution level: {ctx.run.level + 1})')
      ctx.run.level += 1
      ctx.run.info(f'{prefix} reference id is "{puid}"')
      ctx.run.pipe(id, iteration, puid)
      ctx.run.level -= 1
      ctx.run.info(f'{prefix} completed pipeline "{id}" (current level: {ctx.run.level})')
    ctx.run.pipeline = pipeline