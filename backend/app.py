import logging
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from extensions import db

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Structured JSON logging
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
    )

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    from routes.tasks import tasks_bp
    from routes.categories import categories_bp

    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')

    # Health check
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'ok'}), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({'error': 'Unprocessable entity'}), 422

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    # Create tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=app.config.get('DEBUG', False))
