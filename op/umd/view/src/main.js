import './style.css'
import './components/menu/style.css'
import './theme.css'

import { render } from './components/umd/svg'
import * as menu from './components/menu'
import * as zoom from './components/umd/zoom'

import { reg } from './services/globals'

async function app() {
  const app = document.getElementById('app')
  const content = document.createElement('div')
  const frame = document.createElement('div')

  const ctx = { 
    render: async pipeline => {
      if (pipeline != ctx.pipeline) {
        ctx.pipeline = pipeline
        content.childNodes[0].remove()
        content.appendChild(await render(pipeline, ctx))
        
      }
    }
  }
  const element = await render(null, ctx)
  const elements = { app: content, content: element }

  reg('elements', elements)
  
  content.className = 'content'
  frame.className = 'frame'
  content.appendChild(element)
  frame.appendChild(content)
  app.appendChild(frame)
  app.appendChild(zoom.render())
  app.appendChild(menu.render(ctx))
}

(async() => {
  await app()
})()
