import CategoryBadge from './CategoryBadge.jsx'

const priorityColors = { low: '#22c55e', medium: '#f59e0b', high: '#ef4444' }
const statusLabels = { todo: 'To Do', in_progress: 'In Progress', done: 'Done' }

export default function TaskCard({ task, onEdit, onDelete }) {
  return (
    <div style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: 16, background: '#fff', boxShadow: '0 1px 3px rgba(0,0,0,0.07)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
        <h3 style={{ margin: 0, fontSize: 16, fontWeight: 600 }}>{task.title}</h3>
        <span style={{ background: priorityColors[task.priority], color: '#fff', padding: '2px 8px', borderRadius: 12, fontSize: 11, fontWeight: 700, textTransform: 'uppercase' }}>
          {task.priority}
        </span>
      </div>
      {task.description && <p style={{ margin: '0 0 8px', color: '#6b7280', fontSize: 14 }}>{task.description}</p>}
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 8 }}>
        <span style={{ background: '#ede9fe', color: '#7c3aed', padding: '2px 8px', borderRadius: 12, fontSize: 12 }}>
          {statusLabels[task.status] || task.status}
        </span>
        {task.category && <CategoryBadge category={task.category} />}
      </div>
      {task.due_date && <p style={{ margin: '0 0 8px', fontSize: 13, color: '#9ca3af' }}>Due: {task.due_date}</p>}
      <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
        <button onClick={() => onEdit(task)} style={{ flex: 1, padding: '6px 12px', background: '#6366f1', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 13 }}>Edit</button>
        <button onClick={() => onDelete(task.id)} style={{ flex: 1, padding: '6px 12px', background: '#fee2e2', color: '#ef4444', border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 13 }}>Delete</button>
      </div>
    </div>
  )
}
