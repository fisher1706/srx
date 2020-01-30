from src.api.api import API

class CheckoutGroupApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_checkout_group(self, dto):
        url = self.url.get_api_url_for_env("/customer-portal/customer/pass-code/checkout-groups")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info("New checkout group '"+dto["name"]+"' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def delete_checkout_group(self, checkout_group_id):
        url = self.url.get_api_url_for_env("/customer-portal/customer/pass-code/checkout-groups/"+str(checkout_group_id))
        token = self.get_customer_token()
        response = self.send_delete(url, token)
        if (response.status_code == 200):
            self.logger.info("Checkout group with ID = '"+str(checkout_group_id)+"' has been successfully deleted")
        else:
            self.logger.error(str(response.content))