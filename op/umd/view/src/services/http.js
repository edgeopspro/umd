import { config } from '../umd.config'

export async function req(entry, payload, headers) {
  if (!payload) {
    payload = ''
  }

  try {
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
  } catch (error) {
    console.warn(error)
    return { error: error.message }
  }
}