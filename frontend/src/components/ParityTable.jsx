function dteColor(dte, max) {
  const t = Math.min(1, dte / max)
  const a = [247, 201, 72], b = [100, 255, 218]
  return `rgb(${a.map((x, i) => Math.round(x + (b[i] - x) * t)).join(',')})`
}

export default function ParityTable({ rows }) {
  const maxDte = Math.max(1, ...rows.map((r) => r.dte))
  return (
    <table>
      <thead>
        <tr>
          <th>Expiry</th><th>Strike</th><th>Call</th><th>Put</th>
          <th>Residual</th><th>Edge</th><th>Signal</th>
        </tr>
      </thead>
      <tbody>
        {rows.length === 0 && (
          <tr><td colSpan="7" style={{ textAlign: 'center', padding: '22px', color: 'var(--faint)' }}>
            no parity breaks beyond spread cost
          </td></tr>
        )}
        {rows.map((r, i) => (
          <tr key={i}>
            <td><span className="pill" style={{ color: dteColor(r.dte, maxDte) }}>{r.expiry}</span></td>
            <td>{r.strike.toFixed(0)}</td>
            <td>{r.call_mid.toFixed(2)}</td>
            <td>{r.put_mid.toFixed(2)}</td>
            <td style={{ color: r.residual >= 0 ? 'var(--mint)' : 'var(--red)' }}>
              {(r.residual >= 0 ? '+' : '') + r.residual.toFixed(2)}
            </td>
            <td className="flag">{r.edge.toFixed(2)}</td>
            <td>{r.signal}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
