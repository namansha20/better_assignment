from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from extensions import db
from models import Category
from schemas import category_schema, categories_schema

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify(categories_schema.dump(categories)), 200

@categories_bp.route('', methods=['POST'])
def create_category():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided'}), 400
    try:
        data = category_schema.load(json_data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 422

    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category with this name already exists'}), 409

    category = Category(name=data['name'], color=data.get('color', '#6366f1'))
    db.session.add(category)
    db.session.commit()
    return jsonify(category_schema.dump(category)), 201

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(category_schema.dump(category)), 200

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    db.session.delete(category)
    db.session.commit()
    return '', 204
