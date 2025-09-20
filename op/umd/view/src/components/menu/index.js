import * as control from './control'
import * as pipelines from './pipelines'

import { lang } from '../../lang'

export function render(ctx) {
  const content = document.createElement('div')
  const element = document.createElement('div')
  const title = document.createElement('div')

  content.className = 'content'
  element.className = 'menu'
  title.className = 'title'
  title.textContent = lang.menu.en.title
  
  element.appendChild(title)
  element.appendChild(content)
  element.appendChild(control.render(element))
  pipelines.render(content, ctx)

  return element
}