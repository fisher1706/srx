from src.api.api import API
from src.api.distributor.location_api import LocationApi

class CheckoutApi(API):
    def __init__(self, case):
        super().__init__(case)
    
    def checkout_cart(self, location_id, quantity, location_type):
        cart = {
            "locationId": location_id,
            "quantity": quantity,
            "type": location_type
        }
        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart/issue")
        token = self.get_customer_token()
        response = self.send_post(url, token, cart)
        if (response.status_code == 200):
            self.logger.info(f"grats")
        else:
            self.logger.error(str(response.content))

    def get_cart(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/cart")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(f"grats")
        else:
            self.logger.error(str(response.content))
        count = len(response["data"]["items"])
        assert count == 1, f"{count}123"
        return response["data"]

    def issue_product(self, location_dto):
        cart_response = self.get_cart()

        url = self.url.get_api_url_for_env("/customer-portal/customer/checkout/carts/issue/label/process")
        token = self.get_customer_token()
        response = self.send_post(url, token, location_dto)
        if (response.status_code == 200):
            self.logger.info(f"{location_dto['quantity']} items of product '{location_dto['orderingConfig']['product']['partSku']}' has been successfully issued")
        else:
            self.logger.error(str(response.content))

    def return_product(self, customer_user_id):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/users/{customer_user_id}")
        token = self.get_customer_token()
        response = self.send_delete(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Customer user with ID = '{customer_user_id}' has been successfully deleted")
        else:
            self.logger.error(str(response.content))
