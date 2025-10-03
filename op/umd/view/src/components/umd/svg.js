import { theme } from '../../umd.theme'

import * as connector from './connector'
import * as control from './control'
import * as part from './part'
import * as primary from './primary'

import { reg } from '../../services/globals'
import { query, umd } from '../../services/umd'

let ctx = null

export function append(elements, parent) {
  if (!Array.isArray(elements)) {
    elements = [ elements ]
  }

  if (Array.isArray(parent)) {
    parent = parent[0]
  }

  for (const element of elements) {
    parent.appendChild(element)
  }
}

export function create(type, props, value) {
  const element = document.createElementNS('http://www.w3.org/2000/svg', type)

  if (props instanceof Object) {
    for (const key of Object.keys(props)) {
      element.setAttribute(key, props[key])
    }
  }

  if (value) {
    element.textContent = value
  }

  return element
}

export async function render(pipeline, context) {
  function background(config) {
    const { colors } = config

    const back = create('pattern', {
      'id': 'back',
      'x': -10,
      'y': -10,
      width: 20,
      'height': 20,
      'patternUnits': 'userSpaceOnUse'
    })
    append(back, defs)

    append(create('rect', {
      width: 20,
      'height': 20,
      fill: colors.back
    }), back)

    append(create('circle', {
      'cx': 19,
      'cy': 19,
      'r': .5,
      fill: colors.dot
    }), back)

    append(create('rect', {
      width: '100%',
      'height': '100%',
      fill: 'url(#back)'
    }), svg)
  }

 

  const defs = create('defs'), svg = create('svg')
  const { config, scrolls } = theme
  const parts = {}

  const style = `@font-face {
    font-family: 'Oxanium';
    src: url(/fonts/Oxanium.woff2) format('woff2');
  }
  .hint, .label, .title { font-family: ${config.font.name} }
  .hint { font-size: ${config.hint.font.size}pt }
  .label { font-size: ${config.label.font.size}pt }
  .title { font-size: ${config.bar.font.size}pt }`

  const vars = { 
    '--scroll-back': scrolls.colors.back,
    '--scroll-front': scrolls.colors.front
  }

  for (const key of Object.keys(vars)) {
    document.documentElement.style.setProperty(key, vars[key])
  }

  append(create('style', null, style), defs)
  append(defs, svg)
  background(theme.frame)

  await umd(async setup => {
    if (context) {
      const res = await fetch('umd.xml')
      const umd = new DOMParser().parseFromString(await res.text(), 'application/xml')
      const root = umd.querySelector('umd')

      ctx = {
        pipelines: query(root, 'pipeline'),
        root,
        umd
      }

      for (const member of Object.keys(ctx)) {
        context[member] = ctx[member]
      }
    }

    if (!pipeline && ctx.pipelines.length > 0) {
      pipeline = ctx.pipelines[0].attributes.id.value
      context.pipeline = pipeline
    }

    return {
      ...ctx,
      pipeline
    }
  }, setup => {
    for (const prop of Object.keys(setup.frame)) {
      svg.style[prop] = `${setup.frame[prop]}px`
    }

    for (const state of setup.primary) {
      const parent = primary.render(state)
      
      for (const item of state.parts) {
        append(part.render(item), parent)
        parts[item.data.id] = item
      }
  
      append(parent, svg)
    }
  }, setup => {
    for (const connection of setup.connections) {
      append(connector.render(connection), svg)
    }

    reg('setup', setup)
  })

  append(control.render(context || ctx), svg)
 
  return svg
}