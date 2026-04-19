export default function CategoryBadge({ category }) {
  if (!category) return null
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4, padding: '2px 8px', borderRadius: 12, background: '#f3f4f6', fontSize: 12 }}>
      <span style={{ width: 8, height: 8, borderRadius: '50%', background: category.color, display: 'inline-block' }} />
      {category.name}
    </span>
  )
}
