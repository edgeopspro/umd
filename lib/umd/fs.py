import json
import os
import shutil

use = {
  'encoding': 'utf-8'
}

def copy(source, target, kind='file'):
  if source and target:
    try:
      if kind == 'dir':
        shutil.copytree(source, target)
        return True
      elif kind == 'file':
        shutil.copy2(source, target)
        return True
    except Exception:
      return False
  return False

def read(path, binary=False):
  try:
    if os.path.exists(path):
      if binary:
        with open(path, 'rb') as file:
          return file.read()
      else:
        with open(path, 'r', encoding=use['encoding']) as file:
          return file.read()
    return None
  except Exception:
    return None

def write(path, value, binary=False):
  try:
    if isinstance(value, dict) or isinstance(value, list):
      data = json.dumps(value, ensure_ascii=False)
    else:
      data = value if binary else str(value) 
    if binary:
      with open(path, 'wb') as file:
        file.write(data)
    else:
      with open(path, 'w', encoding=use['encoding']) as file:
        file.write(data)
    return True
  except Exception:
    return False
    