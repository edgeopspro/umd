from lib.umd.fs import copy, read, write
from lib.umd.parsers.json import parse, stringify

handlers = {
  'exp': {
    'json': stringify
  },
  'imp': {
    'json': parse
  }
}

def bin(ctx, input):
  format = input['format'] if 'format' in input else None
  return format == 'binary'


def copy(ctx, input):
  format = input['format'] if 'format' in input else None
  kind = input['type'] if 'type' in input else 'file'
  source = input['source'] if 'source' in input else None
  target = input['target'] if 'target' in input else None
  value = input['content'] if 'content' in input else None
  if source:
    return copy(source, target, kind)
  if value:
    return exp(ctx, { 'path': target, 'data': value, 'format': format })
  return False


def exp(ctx, input):
  try:
    path = input['path'] if 'path' in input else None
    if path:
      use = translate(ctx, { **input, 'method': 'exp' })
      write(path, use['data'], bin(ctx, input))
      return True
  except Exception:
    return False
  return False


def imp(ctx, input):
  try:
    path = input['path'] if 'path' in input else None
    if path:
      data = read(path, bin(ctx, input))
      use = translate(ctx, { **input, 'data': data, 'method': 'imp' })
      return use['data']
  except Exception as error:
    ctx.run.err(error)
    return None
  return None


def translate(ctx, input):
  data = input['data'] if 'data' in input else None
  format = input['format'] if 'format' in input else None
  method = input['method'] if 'method' in input else None

  binary = bin(ctx, input)
  if method in handlers and format in handlers[method]:
    handler = handlers[method][format]
    if callable(handler):
      data = handler(ctx, { 'data': data })
    elif not data:
      data = ''
  
  return {
    'binary': binary,
    'data': data
  }