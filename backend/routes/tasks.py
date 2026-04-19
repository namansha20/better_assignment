from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from marshmallow import ValidationError
from extensions import db
from models import Task, StatusEnum, PriorityEnum
from schemas import task_schema, tasks_schema

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    status = request.args.get('status')
    priority = request.args.get('priority')
    category_id = request.args.get('category_id')

    query = Task.query
    if status:
        try:
            query = query.filter(Task.status == StatusEnum(status))
        except ValueError:
            return jsonify({'error': f'Invalid status: {status}'}), 400
    if priority:
        try:
            query = query.filter(Task.priority == PriorityEnum(priority))
        except ValueError:
            return jsonify({'error': f'Invalid priority: {priority}'}), 400
    if category_id:
        query = query.filter(Task.category_id == category_id)

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify(tasks_schema.dump(tasks)), 200

@tasks_bp.route('', methods=['POST'])
def create_task():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided'}), 400
    try:
        data = task_schema.load(json_data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 422

    task = Task(
        title=data['title'],
        description=data.get('description'),
        status=StatusEnum(data.get('status', 'todo')),
        priority=PriorityEnum(data.get('priority', 'medium')),
        due_date=data.get('due_date'),
        category_id=data.get('category_id')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task_schema.dump(task)), 201

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task_schema.dump(task)), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        data = task_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 422

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = StatusEnum(data['status'])
    if 'priority' in data:
        task.priority = PriorityEnum(data['priority'])
    if 'due_date' in data:
        task.due_date = data['due_date']
    if 'category_id' in data:
        task.category_id = data['category_id']

    task.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify(task_schema.dump(task)), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return '', 204
