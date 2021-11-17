from shareFile import create_app, db
import pdb

def test_home_page_anonim():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Home page" in response.data

def test_register_page_anonim(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/register')
    assert response.status_code == 200

def test_login_page_anonim(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200

def test_register_page_correct_post(test_client):
    post_data = dict(username="New_user", email="user@gmail.com", password="great12", confirm_password="great12")
    response = test_client.post('/register', data=post_data, follow_redirects=True)
    #pdb.set_trace()
    assert response.status_code == 200
    assert b"Account created" in response.data
