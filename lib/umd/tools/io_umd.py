from lib.umd.parsers.umd import load
from lib.umd.tools import io_raw
from lib.umd.tools import io_xml
from lib.umd.umd import UMDSection

def exp(ctx, input):
  raw = stringify(ctx, input)
  if raw:
    return io_raw.exp(ctx, { 'value': raw })
  return False


def imp(ctx, input):
  raw = io_raw.imp(ctx, input)
  return parse(ctx, { 'value': raw })


def parse(ctx, input):
  sections = []
  xml = io_xml.parse(ctx, input)
  if xml:
    siblings = { node: parent for parent in xml.iter() for node in parent }
    siblings[xml] = None

    for node in xml.iter():
      parent = siblings[node]
      parents = []
      segments = [ node.tag ]

      while parent is not None:
        segments.append(parent.tag)
        parents.append(parent)
        parent = siblings[parent]

      segments.reverse()
      path = '/'.join(segments)
      sections.append(UMDSection(node, path, parents))
  return load(ctx, sections)


def stringify(ctx, input):
  if 'path' in input and 'value' in input:
    try:
      XML.ElementTree(input['value']).write(input['path'], encoding='utf8')
      return True
    except Exception:
      return False
  return False