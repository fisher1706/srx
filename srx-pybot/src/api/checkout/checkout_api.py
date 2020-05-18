from src.api.api import API
from src.api.distributor.location_api import LocationApi
import hashlib

class CheckoutApi(API):
    def __init__(self, case):
        super().__init__(case)
    
    def checkout_cart(self, location_id, quantity, location_type, issue_product=None, return_product=None):
        cart = [{
            "locationId": location_id,
            "quantity": quantity,
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

    def get_cart(self, passcode=None):
        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart")
        if (passcode is not None):
            token = self.get_checkout_group_token()
            sub_token = self.get_checkout_user_sub_token(passcode)
            additional_header = {
                "Sub-Authorization": sub_token
            }
            response = self.send_get(url, token, additional_headers=additional_header)
        else:
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
        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/issue/label/process")
        token = self.get_checkout_token()
        response = self.send_post(url, token, location_dto)
        if (response.status_code == 200):
            self.logger.info(f"{location_dto[0]['quantity']} items of product '{location_dto[0]['orderingConfig']['product']['partSku']}' has been successfully issued")
        else:
            self.logger.error(str(response.content))
    
    def return_product(self, location_dto):
        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/return/label/process")
        token = self.get_checkout_token()
        response = self.send_post(url, token, location_dto)
        if (response.status_code == 200):
            self.logger.info(f"{location_dto[0]['quantity']} items of product '{location_dto[0]['orderingConfig']['product']['partSku']}' has been successfully returned")
        else:
            self.logger.error(str(response.content))

    def get_checkout_user_sub_token(self, passcode):
        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/checkout-users/passcode")
        token = self.get_checkout_group_token()
        sha256passcode = hashlib.sha256(passcode.encode('utf-8')).hexdigest()
        additional_header = {
            "Sub-Authorization": sha256passcode
        }
        response = self.send_post(url, token, additional_headers=additional_header)
        if (response.status_code == 200):
            self.logger.info(f"Sub-Authorization token for checkout user has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["passToken"]
