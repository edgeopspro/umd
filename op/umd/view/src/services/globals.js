const shared = {}

export function reg(key, value) {
  shared[key] = value
}

export function use(key) {
  return shared[key]
}