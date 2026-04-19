import { useState, useEffect } from 'react'

export default function TaskForm({ categories, onSubmit, editingTask, onCancel }) {
  const initial = { title: '', description: '', status: 'todo', priority: 'medium', due_date: '', category_id: '' }
  const [form, setForm] = useState(initial)

  useEffect(() => {
    if (editingTask) {
      setForm({
        title: editingTask.title || '',
        description: editingTask.description || '',
        status: editingTask.status || 'todo',
        priority: editingTask.priority || 'medium',
        due_date: editingTask.due_date || '',
        category_id: editingTask.category_id != null ? String(editingTask.category_id) : ''
      })
    } else {
      setForm(initial)
    }
  }, [editingTask])

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = (e) => {
    e.preventDefault()
    const payload = { ...form }
    if (!payload.due_date) delete payload.due_date
    if (!payload.category_id) delete payload.category_id
    else payload.category_id = parseInt(payload.category_id, 10)
    onSubmit(payload)
    setForm(initial)
  }

  const inputStyle = { width: '100%', padding: '8px 10px', border: '1px solid #d1d5db', borderRadius: 6, fontSize: 14, boxSizing: 'border-box' }
  const labelStyle = { display: 'block', marginBottom: 4, fontSize: 13, fontWeight: 500, color: '#374151' }

  return (
    <form onSubmit={handleSubmit} style={{ background: '#f9fafb', border: '1px solid #e5e7eb', borderRadius: 10, padding: 20, marginBottom: 24 }}>
      <h2 style={{ margin: '0 0 16px', fontSize: 18 }}>{editingTask ? 'Edit Task' : 'New Task'}</h2>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
        <div style={{ gridColumn: '1 / -1' }}>
          <label style={labelStyle}>Title *</label>
          <input name="title" value={form.title} onChange={handleChange} required style={inputStyle} placeholder="Task title" />
        </div>
        <div style={{ gridColumn: '1 / -1' }}>
          <label style={labelStyle}>Description</label>
          <textarea name="description" value={form.description} onChange={handleChange} style={{ ...inputStyle, height: 80, resize: 'vertical' }} placeholder="Optional description" />
        </div>
        <div>
          <label style={labelStyle}>Status</label>
          <select name="status" value={form.status} onChange={handleChange} style={inputStyle}>
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
        </div>
        <div>
          <label style={labelStyle}>Priority</label>
          <select name="priority" value={form.priority} onChange={handleChange} style={inputStyle}>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
        <div>
          <label style={labelStyle}>Due Date</label>
          <input type="date" name="due_date" value={form.due_date} onChange={handleChange} style={inputStyle} />
        </div>
        <div>
          <label style={labelStyle}>Category</label>
          <select name="category_id" value={form.category_id} onChange={handleChange} style={inputStyle}>
            <option value="">None</option>
            {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>
      </div>
      <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
        <button type="submit" style={{ padding: '8px 20px', background: '#6366f1', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontWeight: 600 }}>
          {editingTask ? 'Update Task' : 'Create Task'}
        </button>
        {editingTask && <button type="button" onClick={onCancel} style={{ padding: '8px 20px', background: '#e5e7eb', color: '#374151', border: 'none', borderRadius: 6, cursor: 'pointer' }}>Cancel</button>}
      </div>
    </form>
  )
}
