import json
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


def test_create_user(auth_header):
    url = f'{BASE_URL}/users'
    payload = {
        "name": "John Doe",
        "email": "johndoee33300011@mail.com",
        "gender": "male",
        "status": "active"
    }
    response = requests.post(url,json=payload,headers=auth_header)
    pprint(response.json())
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.json()['email']).is_equal_to("johndoee33300011@mail.com")
