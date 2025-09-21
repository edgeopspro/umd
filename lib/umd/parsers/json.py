from json import dumps, loads

def parse(ctx, input):
  if 'data' in input:
    return loads(input['data'])
  return None

def stringify(ctx, input):
  if 'data' in input:
    return dumps(input['data'])
  return None