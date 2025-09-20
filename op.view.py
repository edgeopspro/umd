from os import getcwd
from subprocess import PIPE, Popen
from sys import argv

cwd = getcwd().replace('\\', '/') + '/op/umd/view'
print(cwd)
try:
  cmd = [
    'npm',
    'run',
    argv[1] if len(argv) > 0 else 'dev'
  ]
  proc = Popen(cmd, stdout=PIPE, text=True, cwd=cwd, shell=True)
  for line in proc.stdout:
    print(line)
  proc.wait()
except SystemExit:
  pass
except KeyboardInterrupt:
  pass
finally:
  print('bye bye')