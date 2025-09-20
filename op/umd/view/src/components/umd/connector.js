import { append, create } from './svg'
import { theme } from '../../umd.theme'

const config = { colors: [ '#98acbc', '#6D9CBC', '#6BBAAB' ], shades: ['ff', 'df', 'bf', 'af', '8f'], levels: {} }

function outconn(element, state) {
  const { bindings, source, targets, stroke } = state
  const sections = [ source, ...targets ]

  if (sections.length == 1) {
    return
  }

  const level = state.level || 0
  const size = 4, radius = 15, ext = 40 * (level + 1)
  const base = {
    stroke: config.colors[parseInt(level / config.shades.length)] + config.shades[level % config.shades.length],
    'stroke-width': size,
  }
  const path = [ `M -${radius} ${radius} L -${radius} ${ext} M 0 0 A ${radius} ${radius} 0 0 0 -${radius} ${radius}` ]
 
  sections.sort((a, b) => a.y - b.y)
  const anchor = { x: source.x, y: sections.shift().y }
  const last = sections.length - 1

  sections.forEach((section, index) => {
    const diff = section.y - anchor.y
    if (diff > 0) {
      let value = diff > radius + size ? diff : 0

      if (anchor.y != source.y && index == last) {
        value -= theme.config.part.height
      }
      path.push(`M 0 0 L ${value} 0 A ${radius} ${radius} 0 0 1 ${radius + value} ${radius} L ${radius + value} ${ext}`)
    }
  })

  const offset = level > 0 || !bindings ? level * ext / (level + (bindings ? 0 : 1)) : ext

  append(create('path', {
    ...base,
    d: path.join(' '),
    fill: 'transparent',
    'stroke-dasharray': stroke == 'dashed' ? `${size * 2}, ${size}` : null,
    transform: `translate(${anchor.x + offset * (bindings ? -1 : 1)}, ${anchor.y + (anchor.y == source.y ? 0 : theme.config.part.height / 2)}) rotate(90, 0, 0) scale(1, ${bindings ? -1 : 1})`
  }), element)
}

export function render(state) {
  const { type } = state

  const element = create('g')

  switch (type) {
    case 'output': 
      outconn(element, state)
      break
  }

  return element
}