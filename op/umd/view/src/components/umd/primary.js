import { append, create } from './svg'
import { theme } from '../../umd.theme'

export function render(state) {
  const { bar, margin } = theme.config
  const { colors } = theme.primary

  const base = { ...state }
  const element = create('g')

  delete base.data
  delete base.parts

  append(create('rect', {
    ...base,
    fill: colors.back
  }), element)

  append(create('rect', {
    ...base,
    height: bar.height,
    fill: colors.back
  }), element)

  append(create('text', {
    ...base,
    'class': 'title',
    x: state.x + margin.x / 2,
    y: state.y + bar.font.size + margin.y / 2,
    fill: colors.front
  }, state.data.id || state.tag || '???'), element)

  state.element = element

  return element
}