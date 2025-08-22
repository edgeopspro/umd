from lib.umd.parsers import json
from lib.umd.tools import io_raw

def exp(ctx, input):
  raw = stringify(ctx, input)
  if raw:
    return io_raw.exp(ctx, { 'data': raw })
  return False

def imp(ctx, input):
  raw = io_raw.imp(ctx, input)
  return parse(ctx, { 'data': raw })

def parse(ctx, input):
  return json.parse(ctx, input)

def stringify(ctx, input):
  return json.stringify(ctx, input)
