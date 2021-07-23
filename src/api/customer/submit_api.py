from src.api.api import API
from src.resources.tools import Tools
from src.resources.messages import Message

class SubmitApi(API):
    def update_replenishment_item(self, shipto_id, replenishment_item_id, reorder_quantity):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/replenishments/list/{shipto_id}/items/{replenishment_item_id}/update")
        token = self.get_customer_token()
        dto = {
            "reorderQuantity": reorder_quantity
        }
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Replenishment item quantity", operation="updated"))
        else:
            self.logger.error(str(response.content))

    def submit_replenishment_list(self, items):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/replenishment/list")
        token = self.get_customer_token()
        replenishment_list_dto = Tools.get_dto("submit_replenishment_list_dto.json")
        replenishment_list_dto["items"] = items 
        response = self.send_post(url, token, replenishment_list_dto)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Replenishment list", operation="updated"))
        else:
            self.logger.error(str(response.content))
