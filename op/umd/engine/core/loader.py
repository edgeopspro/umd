from os import path, walk

def load(dir, router):
  postfix = '.xml'
  umds = []
  for root, _, files in walk(dir):
    for file in files:
      if file.endswith(postfix):
        use = path.join(root, file).replace('\\', '/')
        name = use[len(dir) + 1:].replace(postfix, '')
        umds.append([ use, name, router[name] if router and name in router else None ])
  return umds