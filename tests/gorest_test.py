import json
import uuid
from pprint import pprint

import pytest
import requests
from assertpy import assert_that

with open('../config.json') as config_file:
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
    response = requests.post(url,json=payload,headers=auth_header)
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.json()['email']).is_equal_to(unique_email)
