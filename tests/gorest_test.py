import json
import os
import uuid
from pprint import pprint

import pytest
import requests
from assertpy import assert_that

current_dir = os.path.dirname(__file__)
config_path = os.path.join(current_dir, '..', 'config.json')

with open(config_path) as config_file:
    config = json.load(config_file)


BASE_URL = config['baseUrl']
TOKEN = config['token']


@pytest.fixture
def auth_header():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }


@pytest.fixture
def unique_email():
    return f"testuser_{uuid.uuid4()}@example.com"


def test_create_user(auth_header, unique_email):
    url = f'{BASE_URL}/users'
    payload = {
        "name": "John Doe",
        "email": unique_email,
        "gender": "male",
        "status": "active"
    }
    response = requests.post(url, json=payload, headers=auth_header)
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.json()['name']).is_equal_to(payload['name'])
    assert_that(response.json()['email']).is_equal_to(unique_email)
    assert_that(response.json()['gender']).is_equal_to(payload['gender'])
    assert_that(response.json()['status']).is_equal_to(payload['status'])


def test_get_user_details(auth_header, unique_email):
    # Create user first
    create_url = f'{BASE_URL}/users'
    create_payload = {
        "name": "Jane Doe",
        "email": unique_email,
        "gender": "female",
        "status": "active"
    }
    create_response = requests.post(create_url, json=create_payload, headers=auth_header)
    user_id = create_response.json()['id']

    # Get user details
    url = f'{BASE_URL}/users/{user_id}'
    response = requests.get(url, headers=auth_header)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.json()['id']).is_equal_to(user_id)
    assert_that(response.json()['name']).is_equal_to(create_payload['name'])
    assert_that(response.json()['email']).is_equal_to(unique_email)
    assert_that(response.json()['gender']).is_equal_to(create_payload['gender'])
    assert_that(response.json()['status']).is_equal_to(create_payload['status'])


def test_update_user_details(auth_header, unique_email):
    create_url = f'{BASE_URL}/users'
    create_payload = {
        "name": "Jake Doe",
        "email": unique_email,
        "gender": "male",
        "status": "active"
    }
    create_response = requests.post(create_url, json=create_payload, headers=auth_header)
    user_id = create_response.json()['id']

    # update user
    url = f'{BASE_URL}/users/{user_id}'
    update_payload = {
        "name": "Jake Smith"
    }
    response = requests.put(url, json=update_payload, headers=auth_header)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.json()['name']).is_equal_to(update_payload['name'])


def test_delete_user(auth_header, unique_email):
    create_url = f'{BASE_URL}/users'
    create_payload = {
        "name": "Janice Doe",
        "email": "janicedoe@example.com",
        "gender": "female",
        "status": "active"
    }
    create_response = requests.post(create_url, json=create_payload, headers=auth_header)
    user_id = create_response.json()['id']

    # delete user
    url = f'{BASE_URL}/users/{user_id}'
    response = requests.delete(url, headers=auth_header)

    assert_that(response.status_code).is_equal_to(204)


# -------------- negative test -------------
def test_create_user_with_invalid_email(auth_header):
    url = f'{BASE_URL}/users'
    payload = {
        "name": "John Doe",
        "email": "Invalid-email",
        "gender": "male",
        "status": "active"
    }
    response = requests.post(url, json=payload, headers=auth_header)
    assert_that(response.status_code).is_equal_to(422)
    assert_that(response.json()[0]['field']).is_equal_to('email')


def test_create_user_with_invalid_gender(auth_header, unique_email):
    url = f'{BASE_URL}/users'
    payload = {
        "name": "John Doe",
        "email": unique_email,
        "gender": "invalid-gender",
        "status": "active"
    }
    response = requests.post(url, json=payload, headers=auth_header)
    assert_that(response.status_code).is_equal_to(422)
    assert_that(response.json()[0]['field']).is_equal_to('gender')


def test_update_user_with_invalid_email(auth_header, unique_email):
    create_url = f'{BASE_URL}/users'
    create_payload = {
        "name": "Jake Doe",
        "email": unique_email,
        "gender": "male",
        "status": "active"
    }
    create_response = requests.post(create_url, json=create_payload, headers=auth_header)
    user_id = create_response.json()['id']
    # update user
    url = f'{BASE_URL}/users/{user_id}'
    update_payload = {
        "email": "invalid-email"
    }
    response = requests.put(url, json=update_payload, headers=auth_header)
    assert_that(response.status_code).is_equal_to(422)
    assert_that(response.json()[0]['field']).is_equal_to('email')


def test_update_user_with_invalid_gender(auth_header, unique_email):
    create_url = f'{BASE_URL}/users'
    create_payload = {
        "name": "Jake Doe",
        "email": unique_email,
        "gender": "male",
        "status": "active"
    }
    create_response = requests.post(create_url, json=create_payload, headers=auth_header)
    user_id = create_response.json()['id']
    # update user
    url = f'{BASE_URL}/users/{user_id}'
    update_payload = {
        "gender": "invalid-gender"
    }
    response = requests.put(url, json=update_payload, headers=auth_header)
    assert_that(response.status_code).is_equal_to(422)
    assert_that(response.json()[0]['field']).is_equal_to('gender')


def test_get_nonexistent_user(auth_header):
    url = f'{BASE_URL}/users/nonexistent_userid1234'
    response = requests.get(url, headers=auth_header)
    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.json()['message']).is_equal_to("Resource not found")


def test_delete_nonexistent_user(auth_header):
    url = f'{BASE_URL}/users/nonexistent_userid1234'
    response = requests.get(url, headers=auth_header)
    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.json()['message']).is_equal_to('Resource not found')