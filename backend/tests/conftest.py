import pytest
from app import create_app
from extensions import db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    return app

@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app, db):
    return app.test_client()

@pytest.fixture
def sample_category(db):
    from models import Category
    cat = Category(name='Work', color='#ff5733')
    db.session.add(cat)
    db.session.commit()
    return cat

@pytest.fixture
def sample_task(db, sample_category):
    from models import Task, StatusEnum, PriorityEnum
    task = Task(
        title='Sample Task',
        description='A test task',
        status=StatusEnum.todo,
        priority=PriorityEnum.medium,
        category_id=sample_category.id
    )
    db.session.add(task)
    db.session.commit()
    return task
