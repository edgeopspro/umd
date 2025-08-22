import ssl
from http.client import HTTPSConnection
from urllib.parse import urlencode

from lib.umd.tools.io_raw import exp, imp
from lib.umd.utils import sha512

def api(ctx, input):
  cache = input['cache'] if 'cache' in input else None
  config = input['config'] if 'config' in input else None
  format = input['format'] if 'format' in input else None
  headers = {}
  host = input['host'] if 'host' in input else None
  method = input['method'] if 'method' in input else 'GET'
  path = input['path'] if 'path' in input else None
  params = {}
  payload = input['payload'] if 'payload' in input else ''

  url = f'{host}://{path}'
  if config:
    args = False
    for handler in config:
      id = handler['id'] if 'id' in handler else None
      kind = handler['type'] if 'type' in handler else None
      if id:
        fallback = handler['value']
        resolved = ctx.run.resolve(fallback)
        value = resolved if resolved else fallback
        if kind == 'head':
          headers[id] = value
        elif kind == 'param':
          args = True
          params[id] = value
    if args:
      url += '?' + '&'.join(params)

  request = {
    'method': method,
    'url': path,
    'body': payload,
    'headers': headers,
    'params': urlencode(params)
  }

  source = None
  if cache:
    id = sha512(str(request))
    source = '/'.join([ cache, id ]).replace('//', '/')
    ctx.run.info(f'{method} {url} - searching cache with path "{source}"')
    response = imp(ctx, { 'path': source, 'format': format })
    if response:
      ctx.run.info(f'{method} {url} - found in cache')
      return response
  ctx.run.info(f'{method} {url} - prepare to fetch')
  connection = HTTPSConnection(host, context=ssl._create_unverified_context())
  connection.request(method, path, payload, headers)
  res = connection.getresponse()
  data = res.read()
  if format == 'binary':
    response = data
  else:
    response = data.decode('utf-8')
  if cache and source:
    if exp(ctx, { 'path': source, 'data': response, 'format': format }):
      ctx.run.info(f'{method} {url} - stored in cache ({source})')
  return response