from lib.umd.eval import run

def run(ctx, input):
  key = 'value'
  code = input[key] if key in input else None
  if code:
    del input[key]
  return eval.run(code, input)