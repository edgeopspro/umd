import { lang } from '../../lang'
import { query } from '../../services/umd'
import * as http from '../../services/http'

const css = {
  active: 'active'
}

function pipeline(frame, pipeline, ctx) {
  const bar = document.createElement('div')
  const info = document.createElement('div')
  const output = document.createElement('textarea')
  const panel = document.createElement('div')
  const run = document.createElement('button')
  const vars = document.createElement('span')
  const id = pipeline.attributes.id.value
  const parent = pipeline.attributes.path.value

  bar.className = 'pipeline bar'
  info.className = 'info'
  panel.className = 'pipeline panel'

  bar.textContent = id
  info.innerHTML = pipeline.attributes.info && pipeline.attributes.info.value ? pipeline.attributes.info.value.replaceAll('\\n', '<br/>') : ''
  output.setAttribute('readonly', '')
  vars.textContent = lang.menu.en.pipelines.vars

  if (info.textContent.length > 0) {
    panel.appendChild(info)
  }
  panel.appendChild(vars)
  run.textContent = lang.menu.en.pipelines.run

  for (const handler of query(pipeline, 'var')) {
    const name = handler.attributes.id.value
    const { value } = handler.attributes

    panel.appendChild(variable(panel, name, value ? value.value : null))
  }
 
  bar.onclick = async () => {
    if (bar.classList.toggle(css.active)) {
      for (const element of frame.querySelectorAll('.bar')) {
        if (element != bar) {
          element.classList.toggle(css.active, false)
        }
      }
      await ctx.render(id)
    }
  }

  panel.onclick = async () => {
    await ctx.render(id)
  }

  run.onclick = async () => {
    run.classList.add(css.active)
    const args = update(panel)
    if (args) {
      output.value = ''
      const result = await http.req('/umd/engine', args, { 
        'UMD-ENTRY': parent.substring(0, parent.length - 4),
        'UMD-PIPE': id
      })
      if (!result || result.error) {
        output.value = `!!ERROR!! ${result.error}`
      } else {
        let index = 0
        const handler = setInterval(() => {
          if (index == result.log.length) {
            clearInterval(handler)
          } else {
            output.value += `${result.log[index]}\n`
            index++
          }
        }, 10)
      }
    }
    run.classList.remove(css.active)
  }

  
  frame.appendChild(bar)
  frame.appendChild(panel)
  panel.appendChild(run)
  panel.appendChild(output)
  update(panel)
}

function variable(panel, name, value) {
  const element = document.createElement('div')
  const input = document.createElement('input')
  const label = document.createElement('label')
  const key = `${new Date().getTime().toString(36)}_${name}`

  element.className = 'var'
  label.setAttribute('for', key)
  label.textContent = name
  input.id = key
  input.name = key
  if (value) {
    input.value = value
  }
  input.onchange = () => update(panel)
  input.onkeyup = () => update(panel)

  element.appendChild(label)
  element.appendChild(input)
  
  return element
}

export function render(element, ctx) {
  for (const instance of ctx.pipelines) {
    pipeline(element, instance, ctx)
  }
}

function update(panel) {
  const button = panel.querySelector('button')
  let enabled = true
  const results = {}

  for (const variable of panel.querySelectorAll('.var > input')) {
    if (variable.value) {
      results[variable.id.split('_')[1]] = variable.value
    } else {
      enabled = false
      break
    }
  }

  if (enabled) {
    button.removeAttribute('disabled')
    return results
  } else {
    button.setAttribute('disabled', '')
  }

}