from lib.umd.tools import code, data, db_sqlite, io_json, io_raw, io_text, net_https, run
from lib.umd import path

tools = {
  'code': {
    'run': code.run
  },
  'data': {
    'map': data.map
  },
  'db': {
    'sqlite': {
      'exec': db_sqlite.exec,
      'query': db_sqlite.query,
      'verify': db_sqlite.verify
    },
    'use': {
      'sqlite': db_sqlite.connect
    }
  },
  'io': {
    'fs': {
      'copy': io_raw.copy,
      'exp': io_raw.exp,
      'imp': io_raw.imp
    },
    'json': {
      'parse': io_json.parse,
      'stringify': io_json.stringify,

      'fs': {
        'exp': io_json.exp,
        'imp': io_json.imp
      }
    },
    'text': {
      'format': io_text.format,
      'fs': {
        'exp': io_raw.exp,
        'imp': io_raw.imp
      }
    }
  },
  'net': {
    'https': {
      'api': net_https.api
    }
  },
  'run': {
    'pipe': run.pipeline
  }
}

def resolve(value):
  return path.resolve(tools, value)