import random
import time
import uuid

import pytest

from api.store_api import StoreApi
from api.user_api import UserApi


def wait_until(check, attempts=10, delay_seconds=1):
    for _ in range(attempts):
        if check():
            return True
        time.sleep(delay_seconds)
    return False


@pytest.fixture(scope="session")
def user_api():
    return UserApi()


@pytest.fixture(scope="session")
def store_api():
    return StoreApi()


def make_user():
    username = f"kt3_{uuid.uuid4().hex[:8]}"
    return {
        "id": random.randint(100000, 999999),
        "username": username,
        "firstName": "Ivan",
        "lastName": "Testov",
        "email": f"{username}@example.com",
        "password": "secret123",
        "phone": "+79990000000",
        "userStatus": 1,
    }


def make_order():
    return {
        "id": random.randint(100000, 999999),
        "petId": random.randint(1, 100),
        "quantity": 2,
        "shipDate": "2026-11-20T10:00:00.000Z",
        "status": "placed",
        "complete": False,
    }


@pytest.fixture
def new_user(user_api):
    user = make_user()
    user_api.create_user(user)
    yield user
    user_api.delete_user(user["username"], expected_status=None)


@pytest.fixture
def new_order(store_api):
    order = make_order()
    store_api.place_order(order)
    yield order
    store_api.delete_order(order["id"], expected_status=None)
