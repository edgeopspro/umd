# from op.umd.engine.run import http

# http(
#   [ ],
#   [ 
  
#   ],
#   'op.engine.config.json'
# )

from json import dumps
from time import time

from lib.mesh.parsers.http import mid_json_in, mid_json_out
from op.umd.engine.run import http

def live(ctx, key):
  pass

def proc_http(ctx, state):
  def basic(ctx, run, go, log, output):
    ctx.log(f'starting run with id {run.id}')
    go({
      'log': lambda value: ctx.stream([ 'umd', key, 'log' ], value)
    })
    log += list(map(lambda eval: str(eval()), run.log))
    output = { **output, **run.output }
    ctx.log(f'end of run ({run.id})')

  ctx.log('process incoming http payload')
  log = []
  output = {}
  try:
    payload, heads, info = state
    entry = heads['UMD-ENTRY'] if 'UMD-ENTRY' in heads else None
    pipe = heads['UMD-PIPE'] if 'UMD-PIPE' in heads else None
    if entry and pipe:
      key = f'umd_{entry}'
      if key in ctx.services:
        context = ctx.services[key]
        pre = None
        proc = basic
        post = None
        if context.mids:
          pre, proc, post = context.mids
        if pre:
          payload = pre(ctx, payload)
        context.use(payload, [ pipe ])(lambda run, go: basic(ctx, run, go, log, output))
        if post:
          post(ctx, [ payload, log, output ])
  except Exception as error:
    output = dumps({ 'error': str(error) })
  finally:
    ctx.log(output)
    return {
      'log': log,
      'output': output
    }

def start(ctx):
  ctx.log(f'getting ready')
  tcp = ctx.services['tcp']
  ctx.log(f'operator is ready (using port {tcp.port})')
  return True


def stop(ctx):
  ctx.log('bye bye')
  # do some cleanup maybe
  
http(
  [ start, live, stop ],
  [ 
    mid_json_in,
    proc_http,
    mid_json_out
  ],
  'op.engine.config.json'
)