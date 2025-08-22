import xml.etree.ElementTree as XML

from lib.umd.tools import io_raw

def exp(ctx, input):
  raw = stringify(ctx, input)
  if raw:
    return io_raw.exp(ctx, { 'value': raw })
  return False


def imp(ctx, input):
  raw = io_raw.imp(ctx, input)
  return parse(ctx, { 'value': raw })


def parse(ctx, input):
  if 'value' in input:
    return XML.fromstring(input['value'])
  return None


def stringify(ctx, input):
  if 'path' in input and 'value' in input:
    try:
      XML.ElementTree(input['value']).write(input['path'], encoding='utf8')
      return True
    except Exception:
      return False
  return False