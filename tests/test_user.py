from conftest import make_user, wait_until


class TestUser:
    def test_create_user(self, user_api):
        user = make_user()

        response = user_api.create_user(user)

        assert response.status_code == 200
        assert response.json()["message"] == str(user["id"])
        user_api.delete_user(user["username"], expected_status=None)

    def test_get_user(self, user_api, new_user):
        response = user_api.get_user(new_user["username"])

        assert response.status_code == 200
        received = response.json()
        assert received["username"] == new_user["username"]
        assert received["email"] == new_user["email"]
        assert received["firstName"] == new_user["firstName"]

    def test_update_user(self, user_api, new_user):
        changed_user = dict(new_user)
        changed_user["firstName"] = "Petr"
        changed_user["phone"] = "+79991112233"

        response = user_api.update_user(new_user["username"], changed_user)
        assert response.status_code == 200

        def user_is_updated():
            received = user_api.get_user(new_user["username"]).json()
            return received.get("firstName") == "Petr" and received.get("phone") == "+79991112233"

        assert wait_until(user_is_updated), "Изменения пользователя не применились"

    def test_delete_user(self, user_api, new_user):
        response = user_api.delete_user(new_user["username"])

        assert response.status_code == 200
        assert response.json()["message"] == new_user["username"]

        def user_is_gone():
            return user_api.get_user(new_user["username"], expected_status=404).status_code == 404

        assert wait_until(user_is_gone), "Пользователь всё ещё доступен после удаления"

    def test_get_unknown_user_returns_404(self, user_api):
        response = user_api.get_user("kt3_no_such_user_404", expected_status=404)

        assert response.status_code == 404
        assert response.json()["message"] == "User not found"
