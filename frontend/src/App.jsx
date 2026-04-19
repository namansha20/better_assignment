import { useState, useEffect } from 'react'
import TaskForm from './components/TaskForm.jsx'
import TaskList from './components/TaskList.jsx'
import { getTasks, createTask, updateTask, deleteTask, getCategories } from './services/api.js'

export default function App() {
  const [tasks, setTasks] = useState([])
  const [categories, setCategories] = useState([])
  const [editingTask, setEditingTask] = useState(null)
  const [error, setError] = useState(null)

  const loadData = async () => {
    try {
      const [tasksRes, catsRes] = await Promise.all([getTasks(), getCategories()])
      setTasks(tasksRes.data)
      setCategories(catsRes.data)
    } catch (e) {
      setError('Failed to load data. Is the backend running?')
    }
  }

  useEffect(() => { loadData() }, [])

  const handleSubmit = async (data) => {
    try {
      if (editingTask) {
        await updateTask(editingTask.id, data)
        setEditingTask(null)
      } else {
        await createTask(data)
      }
      setError(null)
      loadData()
    } catch (e) {
      setError(e.response?.data?.error ? JSON.stringify(e.response.data.error) : 'Failed to save task')
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this task?')) return
    try {
      await deleteTask(id)
      loadData()
    } catch (e) {
      setError('Failed to delete task')
    }
  }

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '24px 16px', fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ margin: 0, fontSize: 28, color: '#1f2937' }}>📋 Task Manager</h1>
        <span style={{ color: '#6b7280', fontSize: 14 }}>{tasks.length} task{tasks.length !== 1 ? 's' : ''}</span>
      </div>
      {error && (
        <div style={{ background: '#fee2e2', color: '#dc2626', padding: '10px 14px', borderRadius: 6, marginBottom: 16 }}>
          {error}
        </div>
      )}
      <TaskForm
        categories={categories}
        onSubmit={handleSubmit}
        editingTask={editingTask}
        onCancel={() => setEditingTask(null)}
      />
      <TaskList tasks={tasks} onEdit={setEditingTask} onDelete={handleDelete} />
    </div>
  )
}
