import json
import pytest

class TestGetCategories:
    def test_get_categories_empty(self, client):
        response = client.get('/api/categories')
        assert response.status_code == 200
        assert response.json == []

    def test_get_categories_with_data(self, client, sample_category):
        response = client.get('/api/categories')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Work'

class TestCreateCategory:
    def test_create_category(self, client):
        response = client.post('/api/categories',
            data=json.dumps({'name': 'Personal', 'color': '#00ff00'}),
            content_type='application/json')
        assert response.status_code == 201
        assert response.json['name'] == 'Personal'
        assert response.json['color'] == '#00ff00'

    def test_create_category_default_color(self, client):
        response = client.post('/api/categories',
            data=json.dumps({'name': 'Work'}),
            content_type='application/json')
        assert response.status_code == 201
        assert response.json['color'] == '#6366f1'

    def test_create_category_missing_name(self, client):
        response = client.post('/api/categories',
            data=json.dumps({'color': '#ff0000'}),
            content_type='application/json')
        assert response.status_code == 422

    def test_create_category_invalid_color(self, client):
        response = client.post('/api/categories',
            data=json.dumps({'name': 'Test', 'color': 'red'}),
            content_type='application/json')
        assert response.status_code == 422

    def test_create_category_duplicate_name(self, client, sample_category):
        response = client.post('/api/categories',
            data=json.dumps({'name': 'Work'}),
            content_type='application/json')
        assert response.status_code == 409

    def test_create_category_no_data(self, client):
        response = client.post('/api/categories', content_type='application/json')
        assert response.status_code == 400

class TestGetCategory:
    def test_get_category_by_id(self, client, sample_category):
        response = client.get(f'/api/categories/{sample_category.id}')
        assert response.status_code == 200
        assert response.json['id'] == sample_category.id

    def test_get_category_not_found(self, client):
        response = client.get('/api/categories/9999')
        assert response.status_code == 404

class TestDeleteCategory:
    def test_delete_category(self, client, sample_category):
        response = client.delete(f'/api/categories/{sample_category.id}')
        assert response.status_code == 204

        get_response = client.get(f'/api/categories/{sample_category.id}')
        assert get_response.status_code == 404

    def test_delete_category_not_found(self, client):
        response = client.delete('/api/categories/9999')
        assert response.status_code == 404
