from api.base_request import BaseRequest


class StoreApi(BaseRequest):
    ENDPOINT = "store"

    def place_order(self, order):
        return self.post(f"{self.ENDPOINT}/order", order)

    def get_order(self, order_id, expected_status=200):
        return self.get(f"{self.ENDPOINT}/order/{order_id}", expected_status=expected_status)

    def delete_order(self, order_id, expected_status=200):
        return self.delete(f"{self.ENDPOINT}/order/{order_id}", expected_status=expected_status)

    def get_inventory(self):
        return self.get(f"{self.ENDPOINT}/inventory")
