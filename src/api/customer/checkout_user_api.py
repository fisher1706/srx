from src.api.api import API
from src.resources.messages import Message

class CheckoutUserApi(API):
    def get_checkout_users(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/pass-code/checkout-users")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Checkout User", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json

    def checkout_user_should_be_present(self, checkout_user_body):
        checkout_users = self.get_checkout_users()
        count = len(checkout_users["data"])
        for index in range(count):
            if checkout_user_body["email"] == checkout_users["data"][index]["email"]:
                if (checkout_user_body["lastName"] == checkout_users["data"][index]["lastName"] and checkout_user_body["firstName"] == checkout_users["data"][index]["firstName"]):
                    self.logger.info(f"There is checkout user with email '{checkout_user_body['email']}'")
                    break
        else:
            self.logger.error(f"There is NO checkout user with email '{checkout_user_body['email']}'")
        return count

    def checkout_user_should_not_be_present(self, checkout_user_body):
        checkout_users = self.get_checkout_users()
        count = len(checkout_users["data"])
        for index in range(count):
            if (checkout_user_body["firstName"] == checkout_users["data"][index]["firstName"] and checkout_user_body["lastName"] == checkout_users["data"][index]["lastName"]):
                self.logger.error(f"There is checkout user with email '{checkout_user_body['email']}'")
                break
        else:
            self.logger.info(f"There is NO checkout user with email '{checkout_user_body['email']}'")
        return count
