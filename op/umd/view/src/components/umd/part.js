import { append, create } from './svg'
import { lang } from '../../lang'
import { theme } from '../../umd.theme'

export function render(state) {
  const { bar, hint, label, part, margin, primary } = theme.config
  const { colors } = theme.part
  const { umd } = lang
  const fallback = 'unknown'
  const handler = { name: state.tag || fallback }

  const base = {
    x: state.x,
    height: part.height / 2
  }
  const element = create('g')
  const io = { x: state.x + primary.width - part.edge.width - margin.x * 2 }
  const y = value => state.y + bar.height + base.height + (value || 0)

  let top = 0
  handler.colors = colors.tag[handler.name] || colors.tag[fallback]
  state.element = element

  append(create('rect', {
    ...base,
    y: y(top),
    width: part.tag.width,
    fill: handler.colors.back
  }), element)

  append(create('text', {
    ...base,
    'class': 'label', 
    x: base.x + margin.x / 2,
    y: y(top) + label.font.size + (base.height - label.font.size) * .25,
    fill: handler.colors.front
  }, handler.name), element)

  append(create('rect', {
    ...base,
    x: base.x + part.tag.width,
    y: y(top),
    width: primary.width - margin.x * 2 - part.tag.width,
    fill: colors.title.back
  }), element)

  append(create('text', {
    ...base,
    'class': 'hint', 
    x: base.x + part.tag.width + margin.x / 2,
    y: y(top) + hint.font.size + (base.height - hint.font.size) * .25,
    fill: colors.title.front
  }, state.data.load || state.data.path || ''), element)
  

  if (state.io) {
    append(create('rect', {
      ...base,
      x: io.x,
      y: y(top),
      width: part.edge.width,
      fill: colors.edge.in.back
    }), element)

    append(create('text', {
      ...base,
      'class': 'hint', 
      x: io.x + margin.x / 2,
      y: y(top) + hint.font.size + (base.height - hint.font.size) * .25,
      fill: colors.front
    }, umd.part.en['in']), element)
  }

  top += base.height - 5

  append(create('rect', {
    ...base,
    y: y(top),
    width: primary.width - margin.x * 2,
    fill: colors.back
  }), element)

  
  append(create('text', {
    ...base,
    'class': 'label', 
    x: base.x + margin.x / 2,
    y: y(top) + label.font.size + (base.height - label.font.size) * .5,
    fill: colors.front
  }, state.data.id), element)

  if (state.io) {
    append(create('rect', {
      ...base,
      x: io.x,
      y: y(top),
      width: part.edge.width,
      fill: colors.edge.out.back
    }), element)

    append(create('text', {
      ...base,
      'class': 'hint', 
      x: io.x + margin.x / 2,
      y: y(top) + hint.font.size + (base.height - hint.font.size) * .5,
      fill: colors.front
    }, umd.part.en['out']), element)
  }

  return element
}