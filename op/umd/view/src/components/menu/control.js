import menu from '../../media/menu.svg?raw'

export function render(parent) {
  const element = document.createElement('div')

  element.className = 'control'
  element.onclick = () => {
    parent.classList.toggle('active')
  }

  element.innerHTML = menu
  return element
}