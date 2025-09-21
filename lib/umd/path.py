def resolve(obj, path):
  sections = path if isinstance(path, list) else path.split('/')
  if isinstance(obj, dict):
    next = obj
    valid = True
    for section in sections:
      if section in next:
        next = next[section]
      elif isinstance(next, list):
        next = resolve(next, section)
      else:
        valid = False
    if valid:
      return next
  elif isinstance(obj, list):
    results = []
    for item in obj:
      results.append(resolve(item, path))
    return results
  return None


def scan(obj, handler, path=[], parent=None):
  if isinstance(obj, dict):
    for key, value in obj.items():
      scan(value, handler, path + [ key ], obj)
  elif isinstance(obj, list):
    handler(obj, path, parent)
    for index, item in enumerate(obj):
      scan(item, handler, path + [ f'${index}' ], obj)
  else:
    handler(obj, path, parent)