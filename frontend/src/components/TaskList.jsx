import TaskCard from './TaskCard.jsx'

export default function TaskList({ tasks, onEdit, onDelete }) {
  if (tasks.length === 0) {
    return <div style={{ textAlign: 'center', color: '#9ca3af', padding: 48 }}>No tasks yet. Create one above!</div>
  }
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16, padding: '16px 0' }}>
      {tasks.map(task => (
        <TaskCard key={task.id} task={task} onEdit={onEdit} onDelete={onDelete} />
      ))}
    </div>
  )
}
