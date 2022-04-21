from src.api.api import API
from src.resources.messages import Message
from glbl import CHECK

class MocksApi(API):
    def set_list_of_available_endpoints(self, endpoints_list):
        url = self.url.get_ip_url("/set-available-endpoints")
        dto = {
            "data": endpoints_list
        }
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto, timeout=30)
        CHECK(response.status_code == 200,
            Message.entity_operation_done.format(entity="List of available endpoints", operation="set"),
            str(response.content))

    def set_list_of_sales_orders_v1_items(self, items_list):
        url = self.url.get_ip_url("/set-sales-orders-status-v1-items")
        dto = {
            "data": items_list
        }
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto, timeout=30)
        CHECK(response.status_code == 200,
            Message.entity_operation_done.format(entity="List of salesOrdersStatus items", operation="set"),
            str(response.content))

    def set_list_of_sales_orders_v2_items(self, items_list):
        url = self.url.get_ip_url("/set-sales-orders-status-v2-items")
        dto = {
            "data": items_list
        }
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto, timeout=30)
        CHECK(response.status_code == 200,
            Message.entity_operation_done.format(entity="List of salesOrdersStatusV2 items", operation="set"),
            str(response.content))
