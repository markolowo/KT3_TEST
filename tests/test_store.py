from conftest import make_order, wait_until


class TestStore:
    def test_place_order(self, store_api):
        order = make_order()

        response = store_api.place_order(order)

        assert response.status_code == 200
        received = response.json()
        assert received["id"] == order["id"]
        assert received["petId"] == order["petId"]
        assert received["quantity"] == order["quantity"]
        assert received["status"] == "placed"
        store_api.delete_order(order["id"], expected_status=None)

    def test_get_order(self, store_api, new_order):
        response = store_api.get_order(new_order["id"])

        assert response.status_code == 200
        received = response.json()
        assert received["id"] == new_order["id"]
        assert received["quantity"] == new_order["quantity"]
        assert received["complete"] is False

    def test_delete_order(self, store_api, new_order):
        response = store_api.delete_order(new_order["id"])

        assert response.status_code == 200
        assert response.json()["message"] == str(new_order["id"])

        def order_is_gone():
            return store_api.get_order(new_order["id"], expected_status=404).status_code == 404

        assert wait_until(order_is_gone), "Заказ всё ещё доступен после удаления"

    def test_get_inventory(self, store_api):
        response = store_api.get_inventory()

        assert response.status_code == 200
        inventory = response.json()
        assert isinstance(inventory, dict)
        assert all(isinstance(count, int) for count in inventory.values())

    def test_get_order_with_invalid_id_returns_404(self, store_api):
        response = store_api.get_order("abc", expected_status=404)

        assert response.status_code == 404
