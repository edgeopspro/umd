import { theme } from '../umd.theme'

export function query(use, tag) {
  const nodes = use instanceof HTMLCollection ? use : use.children

  return Array.from(nodes).filter(element => element.tagName == tag)
}

export async function umd(pre, process, post) {
  function adjust(value) {
    if (value % 5 == 0) {
      return value
    }

    return (parseInt(value / 5) + 1) * 5
  }

  function depth(values, type, level) {
    if (!level) {
      level = 0
    }
    if (!levels[type]) {
      levels[type] = []
    }
    if (!levels[type][level]) {
      levels[type][level] = { min: Number.MAX_VALUE, max: Number.MIN_VALUE }
    }
    if (Array.isArray(values)) {
      for (const value of values) {
        if (value <= levels[type][level].min) {
          levels[type][level].min = value
        }
        else if (value >= levels[type][level].max) {
          levels[type][level].max = value
        }
        else {
          level = depth(values, type, level + 1)
        }
      }
    }

    return level
  }

  function identify(parent, value) {
    return `[${parent}/${value.join('/')}]`
  }

  function parse(key) {
    return key.substring(1, key.length - 1).split('/')
  }

  function props(node) {
    const obj = {}
    
    for (const attr of node.attributes) {
      obj[attr.name] = attr.value
    }

    obj.value = node.textContent
    obj.raw = {
      input: query(node, 'input')[0]
    }

    return obj
  }

  function rect(g) {
    const rects = query(g, 'rect')
    const first = rects.shift()
    const last = rects.pop()
    const x = parseInt(first.attributes.x.value)
    const y = parseInt(last.attributes.y.value)
    
    return { 
      x1: x,
      y1: y,
      x2: x + config.primary.width,
      y2: y + config.part.height
    }
  }

  function remove(array, indexes) {
    let count = 0

    for (const index of indexes) {
      array.splice(index - count, 1)
      count++
    }
  }

  function values(node) {
    const results = []

    results.push(...Object.values(props(node)))

    for (const child of node.children) {
      results.push(...values(child))
    }
    
    return results
  }

  const { config } = theme
  const setup = {
    connections: [],
    frame: { 
      width: config.primary.width * 3,
      height: config.bar.height + config.margin.y
    },
    links: {},
    parts: {},
    primary: []
  }

  let ctx = {}

  if (pre instanceof Function) {
    ctx = await pre(setup)
  }

  const space = config.margin.y * 2
  const xml = ctx.umd
  setup.xml = xml

  for (const primary of ctx.root.children) {
    const state = {
      data: props(primary),
      parts: [],
      width: config.primary.width,
      tag: primary.tagName
    }

    for (const part of primary.children) {
      const data = props(part)
      const tag = part.tagName
      const key = data.id ? identify(state.data.id || state.tag, [ tag, data.id ]) : null
      
      if (key && !setup.links[key]) {
        setup.links[key] = []
      }

      const instance = {
        data,
        input: { 
          values: values(part)
        },
        tag,
        io: [ 'cmd' ].indexOf(tag) > -1
      }

      state.parts.push(instance)
      if (key) {
        setup.parts[key] = instance
      }
    }

    setup.primary.push(state)
  }

  for (const state of setup.primary) {
    state.x = (setup.frame.width - config.primary.width) / 2

    for (const part of state.parts) {
      part.x = state.x + config.margin.x

      if (part.data.id && part.input.values) {
        for (const link of part.input.values) {
          
          if (link[0] == '[') {
            const sections = parse(link)
            let parent = state.data.id
            switch (sections[0]) {
              case 'output':
                sections[0] = 'cmd'
                break
              case 'model':
                parent = 'setup'
                break
              case 'run':
                switch (sections[1]) {
                  case 'pipe':
                      const data = props(part.data.raw.input)
                      const primary = setup.primary.filter(prim => prim.data.id == data.id)[0]
                      
                      if (primary) {
                        parent = data.id

                        const link = identify(parent, sections)
  
                        setup.parts[link] = primary
                        setup.links[link] = []
                      }
                    break
                }
                break
            }

            const key = identify(parent, sections)
            let handler = setup.links[key]

            if (!handler) {
              handler = setup.links[key.replace('output/', 'cmd/').replace('model/', 'setup/model/')]
            }
           
            if (handler) {
              handler.push({
                id: part.data.id,
                handler: part,
                parent: state.data.id
              })
            }
          }
          
        }
      }
    }
  }

  const links = Object.values(setup.links).flat()
  const unprim = []
  const unlinked = []
  for (const key of Object.keys(setup.links)) {
    const [ parent, tag, name ] = parse(key)
    const values = setup.links[key]
    let unlink = false
    
    if (values.length == 0) {
      if (links.filter(link => link.id == name && link.parent == (ctx.pipeline ? ctx.pipeline : parent) && link.handler.tag == tag) == 0) {
        unlink = true
      }
    } else if (ctx.pipeline) {
      unlink = true
      for (const link of values) {
        if (link.parent == ctx.pipeline) {
          unlink = false
          break
        }
      }
    }
    if (unlink) {
      if (ctx.pipeline) {
        for (const link of links) {
          const { input } = link.handler.data.raw
          
          if (input && input.attributes.id && input.attributes.id.value == parent && link.parent == ctx.pipeline) {
            unlink = false
          }
        }
      }

      if (unlink) {
        unlinked.push([ key, parent, tag, name ])
      }
    }
  }

  for (const link of unlinked) {
    const [ key, parent, tag, name ] = link
    delete setup.links[key]
    for (const prim of setup.primary) {
      if (prim.data.id == parent || prim.tag == parent) {
        const removed = []

        prim.parts.forEach((part, index) => {
          if (part.tag == tag && part.data.id == name) {
            removed.push(index)
          }
        })
        remove(prim.parts, removed)
      }
    }
  }

  let y = setup.frame.height
  for (const state of setup.primary) {
    state.height = state.parts.length * config.part.height + (state.parts.length + 1) * space
    state.y = y
    for (const part of state.parts) {
      
      part.y = y
      y += config.part.height + space
      
    }
    setup.frame.height += state.height + config.margin.y
    y += space * 2
  }
  setup.frame.height += space * 2

  const linked = Object.keys(setup.links).map(link => parse(link)[0])
  
  setup.primary.forEach((prim, index) => {
    if (prim.tag == 'setup') return
    
    if (linked.indexOf(prim.data.id) < 0) {
      unprim.push(index)
    }
  })

  remove(setup.primary, unprim)

  if (process instanceof Function) {
    process(setup)
  }

  const levels = {}

  for (const link of Object.keys(setup.links)) {
    const source = setup.parts[link], targets = setup.links[link].map(state => state.handler)

    if (source.element && targets.length > 0) {
      const from = rect(source.element)
      const prim = source.tag == 'pipeline'
      const bindings = link.includes('/var/') || link.includes('/use/')
      const x = bindings ? from.x1 : from.x2 + (prim ? 40 : 0)
      const state = {
        bindings,
        stroke: bindings ? 'dashed' : 'solid',
        type: 'output',
        source: { 
          id: source.data.id,
          x,
          y: adjust(from.y1) + (source.io ? config.part.height / 2 : prim ? config.margin.y / 2 + config.bar.height / 2 : 0)
        }, 
        targets: targets.map(target => ({ id: target.data.id, parentX: target, x, y: adjust(rect(target.element).y1 - config.part.height / 2) }))
      }

      state.level = depth([ state.source.y, ...state.targets.map(target => target.y) ], bindings ? 'bind' : 'flow')
      
      setup.connections.push(state)
    }
  }

  if (post instanceof Function) {
    post(setup)
  }

  return setup
}