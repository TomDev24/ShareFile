from shareFile import create_app
import pdb
from html.parser import HTMLParser
import os
import io

def test_home_page_anonim(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Home page" in response.data

def test_register_page_anonim(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_login_page_anonim(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200

def test_logout_page_anonim(test_client):
    response = test_client.get('/logout')
    assert response.status_code == 302

def test_account_page_anonim(test_client):
    response = test_client.get('/account')
    assert response.status_code == 302

def test_non_exist_file_page(test_client):
    response = test_client.get('/files/12fdsjj')
    assert response.status_code == 302

def test_register_page_correct_post(test_client):
    post_data = dict(username="new_user", email="u@gmail.com", password="great12", confirm_password="great12")
    response = test_client.post('/register', data=post_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created" in response.data

def test_login_page_correct_post(test_client):
    test_client.get('/login')
    post_data = dict(email="u@gmail.com", password="great12")
    response = test_client.post('/login', data=post_data)
    assert response.status_code == 302

def test_account_page_logged(test_client):
    response = test_client.get('/account')
    assert response.status_code == 200
    assert b"new_user" in response.data

def test_login_page_logged(test_client):
    response = test_client.get('/login')
    assert response.status_code == 302

def test_register_page_logged(test_client):
    response = test_client.get('/register')
    assert response.status_code == 302

def test_file_upload(test_client):
    file_path = os.path.join(os.getcwd(), "shareFile/", "static/", "FileCollection/", "b3653d7bc54923d4.jpg")
    file_bytes = (open(file_path, "rb"), "some_name")
    post_data = dict(filename="big_problem", access_setting=2, file=file_bytes)
    response = test_client.post('/account', data=post_data)
    assert response.status_code == 302
    response = test_client.get('/account')
    assert b"big_problem" in response.data

def test_file_in_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"big_problem" in response.data

def test_file_increase_download_amount(test_client):
    response = test_client.get('/')
    assert b"big_problem" in response.data
    assert b"Downloaded: 0" in response.data
    #unfinished

def test_logout_of_logged_user(test_client):
    response = test_client.get('/account')
    assert response.status_code == 200
    response = test_client.get('/logout')
    assert response.status_code == 302
    response = test_client.get('/account')
    assert response.status_code == 302
