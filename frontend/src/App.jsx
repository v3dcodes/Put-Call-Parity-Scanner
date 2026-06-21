import { useEffect, useState } from 'react'
import { getParity } from './api'
import StatCard from './components/StatCard'
import ParityTable from './components/ParityTable'

export default function App() {
  const [d, setD] = useState(null)

  useEffect(() => {
    getParity().then(setD).catch((e) => console.error(e))
  }, [])

  return (
    <div className="wrap">
      <div className="sh"><h2>parity scanner</h2></div>
      <div className="eyebrow">SPX · C − P vs S − K·e^(−rT)</div>

      <div className="viz">
        <div className="stats">
          <StatCard label="pairs scanned" value={d ? d.n_scanned : '—'} />
          <StatCard label="flagged" value={d ? d.n_flagged : '—'} cls="flag" />
          <StatCard label="top edge" value={d && d.top.length ? d.top[0].edge.toFixed(2) : '—'} />
        </div>
        <div className="vh"><span>parity breaks · ranked by spread-adjusted edge</span></div>
        <ParityTable rows={d ? d.top : []} />
      </div>
      <div className="foot">
        synthetic chain with injected mispricings by default · set <code>SCHWAB_TOKEN</code> for a live chain
      </div>
    </div>
  )
}
