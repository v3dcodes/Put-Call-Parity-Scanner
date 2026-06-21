export async function getParity() {
  const res = await fetch('/api/parity')
  if (!res.ok) throw new Error(`API ${res.status}`)
  return res.json()
}
