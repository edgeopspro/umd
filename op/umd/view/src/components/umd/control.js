import { create } from './svg'
import { theme } from '../../umd.theme'

export function render(ctx) {
  const { colors } = theme.control
  const { bar, margin } = theme.config
  
  const element = create('rect', {
    x: 0,
    y: 0,
    width: '100%',
    height: bar.height,
    fill: 'none'
  })

  const title = create('text', { 
    'class': 'title', 
    x: '50%', 
    y: bar.font.size + margin.y / 2,
    fill: colors.front,
    width: '100%',
    'text-anchor': 'middle'
  }, ctx.pipeline)


  return [ element, title ]
}