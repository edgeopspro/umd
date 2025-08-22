from op.mesh.core.ctx import Context
from op.mesh.http import op
from op.umd.engine.core.ctx import Context as UMDContext
from op.umd.engine.core.loader import load
from op.umd.engine.router import router
from op.umd.engine.toolkit import tools


def http(cyc, mids, conf):
  ctx = Context(cyc, mids, conf)

  shared = ctx.conf([ 'use' ])
  if isinstance(shared, dict):
    umds = shared['umds'] if 'umds' in shared else None
    if umds:
      for entry in load(umds, router):
        path, name, mids = entry
        ctx.reg(f'umd_{name}', lambda config: UMDContext.load({ **shared, **config }, mids=mids, path=path))
  
  try:
    op.start(ctx)
  except SystemExit:
    op.stop(ctx)
  except KeyboardInterrupt:
    op.stop(ctx)