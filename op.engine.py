from json import dumps
from time import time

from lib.mesh.parsers.http import mid_json_in, mid_json_out
from op.umd.engine.run import http

def live(ctx, key):
  pass

def proc_http(ctx, state):
  def basic(ctx, run, go, log, output):
    ctx.log(f'starting run')
    go({ 'log': stream })
    log += run.log
    output.append(run.output)
    ctx.log(f'end of run ({run.id})')

  def stream(log, kind, level, time, msg):
    if kind == 'SYS':
      ctx.stream([ 'umd', key, 'log' ], lambda: log)

  ctx.log('process incoming http payload')
  log = []
  output = []
  result = None
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
          post(ctx, [ payload, log, output[-1] ])
  except Exception as error:
    result = dumps({ 'error': str(error) })
  finally:
    result = {}
    for item in output:
      if isinstance(item, dict):
        for key, value in item.items():
          result[key] = str(value) if isinstance(value, bytes) else value
    return {
      'log': log,
      'output': result
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