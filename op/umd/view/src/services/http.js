import { config } from '../umd.config'

export async function req(entry, payload, headers) {
  if (!payload) {
    payload = ''
  }

  const res = await fetch(`${config.http.url}${entry}`, {
    method: 'POST',
    body: JSON.stringify(payload),
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': payload.length,
      ...(headers || {})
    }
  })

  return res.json()
}