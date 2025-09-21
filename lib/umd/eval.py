import json

from contextlib import redirect_stdout
from io import StringIO
from os import remove
from tempfile import TemporaryFile

from lib.umd.fs import write

def code(value, payload={}, prefix=None, postfix=None):
  if not prefix:
    prefix = [ f"input = json.loads('{json.dumps(payload)}')" ]
  prog = format(value, prefix=prefix, postfix=postfix)
  with StringIO() as instance:
    with redirect_stdout(instance):
      exec(prog)
    raw = instance.getvalue()
    try:
      output = json.loads(raw)
    except json.decoder.JSONDecodeError:
      output = raw
  return output

def format(code, prefix=[], postfix=None):
  nl = '\n'
  inject = prefix
  lines = code if isinstance(code, list) else code.split(nl)
  if len(lines) > 0:
    index = 0
    ident = 0
    while ident == 0 and index < len(lines):
      for c in lines[index]:
        if len(lines[index]) > 0:
          if c == ' ':
            ident += 1
          else:
            break
      index += 1
    lines = list(map(lambda line: line[ident:], lines))
  inject += lines
  if not postfix:
    postfix = [ 'print(json.dumps(output) if output else "null")' ]
  inject += postfix
  return nl.join(inject)

def run(code, payload={}, postfix=[]):
  io = TemporaryFile()
  io.close()
  write(io.name, payload)
  prog = format(code, prefix=[
    'import json',
    'with open(io.name, "r", encoding="utf-8") as file:',
    '  raw = file.read()',
    '  try:',
    '    input = json.loads(raw)',
    '  except json.decoder.JSONDecodeError:',
    '    input = raw'
  ], postfix=postfix)
  with StringIO() as instance:
    with redirect_stdout(instance):
      exec(prog)
      remove(io.name)
    raw = instance.getvalue()
    try:
      output = json.loads(raw)
    except json.decoder.JSONDecodeError:
      #ctx.run.warn(f'cannot handle eval output as object - value is returned as string')
      output = raw
    return output