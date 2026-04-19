import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: { 'Content-Type': 'application/json' }
})

export const getTasks = (params = {}) => api.get('/api/tasks', { params })
export const createTask = (data) => api.post('/api/tasks', data)
export const getTask = (id) => api.get(`/api/tasks/${id}`)
export const updateTask = (id, data) => api.put(`/api/tasks/${id}`, data)
export const deleteTask = (id) => api.delete(`/api/tasks/${id}`)

export const getCategories = () => api.get('/api/categories')
export const createCategory = (data) => api.post('/api/categories', data)
export const getCategory = (id) => api.get(`/api/categories/${id}`)
export const deleteCategory = (id) => api.delete(`/api/categories/${id}`)

export default api
