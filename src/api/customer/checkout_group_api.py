from src.api.api import API
from src.resources.messages import Message
from glbl import LOG, ERROR

class CheckoutGroupApi(API):
    def create_checkout_group(self, dto):
        url = self.url.get_api_url_for_env("/customer-portal/customer/pass-code/checkout-groups")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            LOG.info(f"New checkout group '{dto['name']}' has been successfully created")
        else:
            ERROR(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def delete_checkout_group(self, checkout_group_id):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/pass-code/checkout-groups/{checkout_group_id}")
        token = self.get_customer_token()
        response = self.send_delete(url, token)
        if response.status_code == 200:
            LOG.info(Message.entity_with_id_operation_done.format(entity="Checkout Group", id=checkout_group_id, operation="deleted"))
        else:
            ERROR(str(response.content))

    def add_shipto_to_checkout_group(self, shipto_id=None, checkout_group_id=None):
        if shipto_id is None:
            shipto_id = self.data.shipto_id
        if checkout_group_id is None:
            checkout_group_id = self.data.checkout_group_id
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/pass-code/checkout-groups/{checkout_group_id}/shiptos")
        shipto_dto = [{
            "issue": True,
            "putAway": True,
            "return": True,
            "shipTo": {
                "id": shipto_id
                }
            }]
        token = self.get_customer_token()
        response = self.send_post(url, token, shipto_dto)
        if response.status_code == 200:
            LOG.info(f"Shipto {shipto_id} was successfully added to the checkout group {checkout_group_id}")
        else:
            ERROR(str(response.content))
