# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db as _db
from app.models import User, Recipe


@pytest.fixture
def app():
    """Create a fresh Flask app configured for testing, with a clean in-memory DB."""
    app = create_app('testing')

    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """A test client for making requests without running a real server."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Give tests direct access to the db session, tables already created by create_app()."""
    yield _db
    _db.session.remove()
    _db.drop_all()
    _db.create_all()


@pytest.fixture
def user_a(db):
    """A pre-created user, for tests that need a logged-in user."""
    user = User(name='Alice', email='alice@test.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def user_b(db):
    """A second, different user — needed for the permission test."""
    user = User(name='Bob', email='bob@test.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def recipe_by_a(db, user_a):
    """A recipe owned by user_a, for testing edit/delete permissions."""
    recipe = Recipe(
        title='Alice\'s Pancakes',
        short_description='Fluffy pancakes.',
        full_recipe='Mix and cook.',
        category='Breakfast',
        prep_time=15,
        servings=2,
        author=user_a
    )
    db.session.add(recipe)
    db.session.commit()
    return recipe


def login(client, email, password):
    """Helper: log in via the real route, as a browser would."""
    return client.post('/auth/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)