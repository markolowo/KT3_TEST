from api.base_request import BaseRequest


class UserApi(BaseRequest):
    ENDPOINT = "user"

    def create_user(self, user):
        return self.post(self.ENDPOINT, user)

    def get_user(self, username, expected_status=200):
        return self.get(f"{self.ENDPOINT}/{username}", expected_status=expected_status)

    def update_user(self, username, user):
        return self.put(f"{self.ENDPOINT}/{username}", user)

    def delete_user(self, username, expected_status=200):
        return self.delete(f"{self.ENDPOINT}/{username}", expected_status=expected_status)
