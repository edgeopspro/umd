from os import getcwd, listdir
from subprocess import PIPE, Popen
from sys import argv
import xml.etree.ElementTree as XML

from lib.umd.tools import io_xml

def apply():
  ctx = {}
  postfix = '.xml'
  source = f'{cwd}/engine/umds'
  target = f'{cwd}/view/public/umd{postfix}'
  paths = listdir(source)
  umd = XML.Element('umd')
  for path in paths:
    if path.endswith(postfix):
      handler = io_xml.imp(ctx, { 'path': f'{source}/{path}' })
      for node in handler.findall('*'):
        if node.tag == 'pipeline':
          node.set('path', path)
        umd.append(node)
  io_xml.exp(ctx, { 'path': target, 'value': umd })

def run():
  try:
    cmd = [
      'npm',
      'run',
      argv[1] if len(argv) > 0 else 'dev'
    ]
    proc = Popen(cmd, stdout=PIPE, text=True, cwd=f'{cwd}/view', shell=True)
    for line in proc.stdout:
      print(line)
    proc.wait()
  except SystemExit:
    pass
  except KeyboardInterrupt:
    pass

cwd = getcwd().replace('\\', '/') + '/op/umd'
apply()
run()