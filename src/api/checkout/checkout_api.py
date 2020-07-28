from src.api.api import API
from src.api.distributor.location_api import LocationApi
import hashlib

class CheckoutApi(API):
    def checkout_cart(self, location_id, location_type, quantity=None, epc=None, issue_product=None, return_product=None, passcode=None):
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
        if (issue_product):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/issue")
        elif (return_product):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/return")
        if (passcode is not None):
            token = self.get_checkout_group_token()
            sub_token = self.get_checkout_user_sub_token(passcode)
            additional_header = {
                "Sub-Authorization": sub_token
            }
            response = self.send_post(url, token, cart, additional_headers=additional_header)
        else:
            token = self.get_checkout_token()
            response = self.send_post(url, token, cart)
        response_json = response.json()
        if (response.status_code == 200):
            self.logger.info(f"Cart checkout has been successfully processed")
        else:
            self.logger.error(str(response.content))

    def validate_rfid(self, location_id, location_type, epc, issue_product=None, return_product=None, passcode=None):
        cart = {
            "locationId": location_id,
            "epc": epc,
            "type": location_type
        }
        if (issue_product):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/issue/item/rfid/validate")
        elif (return_product):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/return/item/rfid/validate")
        if (passcode is not None):
            token = self.get_checkout_group_token()
            sub_token = self.get_checkout_user_sub_token(passcode)
            additional_header = {
                "Sub-Authorization": sub_token
            }
            response = self.send_post(url, token, cart, additional_headers=additional_header)
        else:
            token = self.get_checkout_token()
            response = self.send_post(url, token, cart)
        response_json = response.json()
        if (response.status_code == 200):
            self.logger.info(f"RFID is validated")
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
    
    def close_cart(self, passcode=None):
        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/close")
        if (passcode is not None):
            token = self.get_checkout_group_token()
            sub_token = self.get_checkout_user_sub_token(passcode)
            additional_header = {
                "Sub-Authorization": sub_token
            }
            response = self.send_post(url, token, additional_headers=additional_header)
        else:
            token = self.get_checkout_token()
            response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Cart is empty now")
        else:
            self.logger.error(str(response.content))

    def issue_product(self, location_dto, passcode=None):
        if (location_dto[0]["orderingConfig"]["type"] == "LABEL"):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/issue/label/process")
        if (location_dto[0]["orderingConfig"]["type"] == "RFID"):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/issue/rfid/process")
        if (passcode is not None):
            token = self.get_checkout_group_token()
            sub_token = self.get_checkout_user_sub_token(passcode)
            additional_header = {
                "Sub-Authorization": sub_token
            }
            response = self.send_post(url, token, location_dto, additional_headers=additional_header)
        else:
            token = self.get_checkout_token()
            response = self.send_post(url, token, location_dto)
        if (response.status_code == 200):
            self.logger.info(f"{location_dto[0]['quantity']} items of product '{location_dto[0]['orderingConfig']['product']['partSku']}' has been successfully issued")
        else:
            self.logger.error(str(response.content))
    
    def return_product(self, location_dto, passcode=None):
        if (location_dto[0]["orderingConfig"]["type"] == "LABEL"):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/return/label/process")
        if (location_dto[0]["orderingConfig"]["type"] == "RFID"):
            url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/return/rfid/process")
        if (passcode is not None):
            token = self.get_checkout_group_token()
            sub_token = self.get_checkout_user_sub_token(passcode)
            additional_header = {
                "Sub-Authorization": sub_token
            }
            response = self.send_post(url, token, location_dto, additional_headers=additional_header)
        else:
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

