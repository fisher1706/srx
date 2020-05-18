from src.api.api import API
from src.api.distributor.location_api import LocationApi

class CheckoutApi(API):
    def __init__(self, case):
        super().__init__(case)
    
    def checkout_cart(self, location_id, location_type, quantity=None, epc=None, issue_product=None, return_product=None):
        if (location_type == "LABEL"):
            cart = [{
                "locationId": location_id,
                "quantity": quantity,
                "type": location_type
            }]
        if (location_type == "RFID"):
            cart = [{
                "locationId": location_id,
                "epc": epc,
                "type": location_type
            }]
        if (issue_product is True):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/issue")
        elif (return_product is True):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/return")
        token = self.get_checkout_token()
        response = self.send_post(url, token, cart)
        response_json = response.json()
        if (response.status_code == 200):
            self.logger.info(f"Cart checkout has been successfully processed")
        else:
            self.logger.error(str(response.content))

    def validate_rfid(self, location_id, location_type, epc, issue_product=None, return_product=None):
        cart = {
            "locationId": location_id,
            "epc": epc,
            "type": location_type
        }
        if (issue_product is True):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/issue/item/rfid/validate")
        elif (return_product is True):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/return/item/rfid/validate")
        token = self.get_checkout_token()
        response = self.send_post(url, token, cart)
        response_json = response.json()
        if (response.status_code == 200):
            self.logger.info(f"RFID is validated")
        else:
            self.logger.error(str(response.content))

    def get_cart(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart")
        token = self.get_checkout_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Cart has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]
    
    def close_cart(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/close")
        token = self.get_checkout_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Cart is empty now")
        else:
            self.logger.error(str(response.content))

    def issue_product(self, location_dto):
        if (location_dto[0]["orderingConfig"]["type"] == "LABEL"):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/issue/label/process")
        if (location_dto[0]["orderingConfig"]["type"] == "RFID"):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/issue/rfid/process")
        token = self.get_checkout_token()
        response = self.send_post(url, token, location_dto)
        if (response.status_code == 200):
            self.logger.info(f"{location_dto[0]['quantity']} items of product '{location_dto[0]['orderingConfig']['product']['partSku']}' has been successfully issued")
        else:
            self.logger.error(str(response.content))
    
    def return_product(self, location_dto):
        if (location_dto[0]["orderingConfig"]["type"] == "LABEL"):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/return/label/process")
        if (location_dto[0]["orderingConfig"]["type"] == "RFID"):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/return/rfid/process")
        token = self.get_checkout_token()
        response = self.send_post(url, token, location_dto)
        if (response.status_code == 200):
            self.logger.info(f"{location_dto[0]['quantity']} items of product '{location_dto[0]['orderingConfig']['product']['partSku']}' has been successfully returned")
        else:
            self.logger.error(str(response.content))

            