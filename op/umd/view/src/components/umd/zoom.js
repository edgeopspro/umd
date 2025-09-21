import { theme } from '../../umd.theme'
import { use } from '../../services/globals'

export function render() {
  function select(element) {
    for (const scale of scales) {
      scale == element ? scale.setAttribute('data-select', '') : scale.removeAttribute('data-select')
    }
  }

  const { colors } = theme.zoom
  const { app, content } = use('elements')
  
  const element = document.createElement('div')
  const scales = []
  element.id = 'zoom'

  for (const value of [ 25, 50, 85, 100, 120, 150, 200 ]) {
    const scale = document.createElement('div')

    scale.textContent = `${value}%`
    scale.style.background = colors.back
    scale.style.color = colors.front

    scale.onclick = event => {
      function format(location) {
        return `${(location * scale - location) * .5}px`
      }

      const { frame } = use('setup')

      select(event.target)

      const scale = value / 100
      content.style.transform = `scale(${scale})`
      if (scale < 1) {
        app.style.height = `${scale * frame.height}px`
      }
      app.style.top = format(frame.height)
      app.style.left = format(frame.width * .5 - theme.config.primary.width)
    }

    element.appendChild(scale)
    scales.push(scale)
  }

  select(scales[3])

  return element
}