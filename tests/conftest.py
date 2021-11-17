from shareFile import create_app, db
from config import TestConfig
import pytest

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
