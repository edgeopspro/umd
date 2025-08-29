proc = None

def pre(ctx, input):
  def get(obj, props):
    results = list(map(lambda prop: obj[prop] if prop in obj else None, props))
    return None if len(list(filter(lambda result: result is None, results))) > 0 else results

  use = get(ctx.config['use']['bin'], [ 'root', 'paths' ])
  if use:
    bin, paths = use
    use = get(input, [
      'covers',
      'db',
      'template source',
      'template target',
      'cache',
      'media'
    ])
    if use:
      covers, db, tmplsrc, tmpltrg, cache, media = use
      data, gen, meta = paths
      return {
        'covers': f'{bin}/{meta}/{covers}',
        'db':  f'{bin}/{data}/{db}',
        'template source': f'{bin}/{meta}/{tmplsrc}',
        'template target': f'{bin}/{gen}/{tmpltrg}',
        'cache': f'{bin}/{gen}/{cache}',
        'media': f'{bin}/{gen}/{media}',
      }
    raise Exception('invalid input')
  raise Exception('invalid config')

def post(ctx, data):
  input, log, output = data
  pass
