import json
import pytest

class TestGetTasks:
    def test_get_tasks_empty(self, client):
        response = client.get('/api/tasks')
        assert response.status_code == 200
        assert response.json == []

    def test_get_tasks_with_data(self, client, sample_task):
        response = client.get('/api/tasks')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['title'] == 'Sample Task'

    def test_get_tasks_filter_by_status(self, client, sample_task):
        response = client.get('/api/tasks?status=todo')
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_get_tasks_filter_by_invalid_status(self, client):
        response = client.get('/api/tasks?status=invalid')
        assert response.status_code == 400

class TestCreateTask:
    def test_create_task_minimal(self, client):
        response = client.post('/api/tasks',
            data=json.dumps({'title': 'New Task'}),
            content_type='application/json')
        assert response.status_code == 201
        assert response.json['title'] == 'New Task'
        assert response.json['status'] == 'todo'
        assert response.json['priority'] == 'medium'

    def test_create_task_full(self, client, sample_category):
        data = {
            'title': 'Full Task',
            'description': 'A detailed task',
            'status': 'in_progress',
            'priority': 'high',
            'due_date': '2025-12-31',
            'category_id': sample_category.id
        }
        response = client.post('/api/tasks',
            data=json.dumps(data),
            content_type='application/json')
        assert response.status_code == 201
        assert response.json['title'] == 'Full Task'
        assert response.json['status'] == 'in_progress'
        assert response.json['priority'] == 'high'

    def test_create_task_missing_title(self, client):
        response = client.post('/api/tasks',
            data=json.dumps({'description': 'no title'}),
            content_type='application/json')
        assert response.status_code == 422

    def test_create_task_invalid_status(self, client):
        response = client.post('/api/tasks',
            data=json.dumps({'title': 'Task', 'status': 'invalid'}),
            content_type='application/json')
        assert response.status_code == 422

    def test_create_task_invalid_priority(self, client):
        response = client.post('/api/tasks',
            data=json.dumps({'title': 'Task', 'priority': 'critical'}),
            content_type='application/json')
        assert response.status_code == 422

    def test_create_task_no_data(self, client):
        response = client.post('/api/tasks', content_type='application/json')
        assert response.status_code == 400

class TestGetTask:
    def test_get_task_by_id(self, client, sample_task):
        response = client.get(f'/api/tasks/{sample_task.id}')
        assert response.status_code == 200
        assert response.json['id'] == sample_task.id

    def test_get_task_not_found(self, client):
        response = client.get('/api/tasks/9999')
        assert response.status_code == 404
        assert 'error' in response.json

class TestUpdateTask:
    def test_update_task(self, client, sample_task):
        response = client.put(f'/api/tasks/{sample_task.id}',
            data=json.dumps({'title': 'Updated Title', 'status': 'done'}),
            content_type='application/json')
        assert response.status_code == 200
        assert response.json['title'] == 'Updated Title'
        assert response.json['status'] == 'done'

    def test_update_task_not_found(self, client):
        response = client.put('/api/tasks/9999',
            data=json.dumps({'title': 'X'}),
            content_type='application/json')
        assert response.status_code == 404

    def test_update_task_invalid_status(self, client, sample_task):
        response = client.put(f'/api/tasks/{sample_task.id}',
            data=json.dumps({'status': 'invalid'}),
            content_type='application/json')
        assert response.status_code == 422

    def test_status_transition_todo_to_done(self, client, sample_task):
        response = client.put(f'/api/tasks/{sample_task.id}',
            data=json.dumps({'status': 'done'}),
            content_type='application/json')
        assert response.status_code == 200
        assert response.json['status'] == 'done'

class TestDeleteTask:
    def test_delete_task(self, client, sample_task):
        response = client.delete(f'/api/tasks/{sample_task.id}')
        assert response.status_code == 204

        get_response = client.get(f'/api/tasks/{sample_task.id}')
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client):
        response = client.delete('/api/tasks/9999')
        assert response.status_code == 404
