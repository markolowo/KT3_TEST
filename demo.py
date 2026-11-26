import uuid

from api.store_api import StoreApi
from api.user_api import UserApi

user_api = UserApi()
store_api = StoreApi()

username = f"demo_{uuid.uuid4().hex[:6]}"
user = {
    "id": 424242,
    "username": username,
    "firstName": "Demo",
    "lastName": "User",
    "email": f"{username}@example.com",
    "password": "secret123",
    "phone": "+70000000000",
    "userStatus": 1,
}

print("===== USER: 4 запроса =====")
user_api.create_user(user)
user_api.get_user(username)
user["firstName"] = "Changed"
user_api.update_user(username, user)
user_api.delete_user(username)

order = {"id": 424242, "petId": 7, "quantity": 1, "status": "placed", "complete": False}

print("===== STORE: 4 запроса =====")
store_api.place_order(order)
store_api.get_order(order["id"])
store_api.get_inventory()
store_api.delete_order(order["id"])
