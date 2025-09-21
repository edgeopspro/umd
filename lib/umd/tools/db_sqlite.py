import sqlite3

connections = []

def invoke(ctx, input, handler):
  service = 'db'
  if isinstance(input, dict):
    preserve = False
    if service in input:
      connection = input[service]
      if connection:
        ctx.run.info(f'using an open db connection with id "{id}')
        preserve = True
  if not preserve:
    connection = connect(ctx, input)
  if connection:
    result = handler(connection, ctx, input)
    if not preserve:
      close(ctx, { 'connection': connection })
    return result
  return None


def close(ctx, input):
  for connection in connections:
    if isinstance(connection, sqlite3.Connection):
      path = input['path'] if 'path' in input else ''
      ctx.run.info(f'closing db connection {path}')
      connection.close()


def connect(ctx, input):
  src = None
  preserve = True
  if 'path' in input:
    src = input['path']
    ctx.run.info(f'starting a new connection to db using path {src}')
  if not src:
    preserve = False
    src = ':memory:'
    ctx.run.info(f'starting a new connection to an in-memory db')
  connection = sqlite3.connect(src, check_same_thread=False)
  if preserve:
    connections.append(connection)
    ctx.run.posts.append(lambda: close(ctx, { 'connection': connection, 'path': src if preserve else None }))
  return connection


def exec(ctx, input):
  def apply(connection, ctx, input):
    connection.executescript(input['value'])
  return invoke(ctx, input, apply)


def query(ctx, input):
  def apply(connection, ctx, input):
    all = []
    try:
      query = input['value']
      connection.row_factory = sqlite3.Row
      cursor = connection.cursor()
      ctx.run.info(f'executing query: {query}')
      cursor.execute(query)
      columns = [column[0] for column in cursor.description]
      rows = cursor.fetchall()
      for row in rows:
        all.append({ key: value for key, value in zip(columns, row) })
      ctx.run.info(f'query returned {len(all)} items')
      return all
    except Exception as error:
      return { 'error': error }
  return invoke(ctx, input, apply)


def verify(ctx, input):
  def apply(connection, ctx, input):
    try:
      if not 'value' in input:
        return False
      connection.row_factory = sqlite3.Row
      cursor = connection.cursor()
      cursor.execute(input['value'])
      return None
    except Exception as ex:
      return ex
  return invoke(ctx, input, apply)