from op.umd.engine.umds import demo

router = {
  'demo': [ demo.pre, demo.proc, demo.post ]
}