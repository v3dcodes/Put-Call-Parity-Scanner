export default function StatCard({ label, value, cls = '' }) {
  return (
    <div className="stat">
      <div className="k">{label}</div>
      <div className={`v ${cls}`}>{value}</div>
    </div>
  )
}
