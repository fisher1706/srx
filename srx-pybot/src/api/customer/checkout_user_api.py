from src.api.api import API

class CheckoutUserApi(API):
    def __init__(self, case):
        super().__init__(case)

    def get_checkout_users(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/pass-code/checkout-users")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Checkout users have been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json

    def checkout_user_should_be_present(self, checkout_user_body):
        checkout_users = self.get_checkout_users()
        count = len(checkout_users["data"])
        for index in range(0, count):
            if (checkout_user_body["email"] == checkout_users["data"][index]["email"]):
                if (checkout_user_body["lastName"] == checkout_users["data"][index]["lastName"] and checkout_user_body["firstName"] == checkout_users["data"][index]["firstName"]):
                    self.logger.info(f"New checkout user '{checkout_user_body['email']}' has been successfuly created")
                    break
        else:
            self.logger.error(f"New checkout user '{checkout_user_body['email']}' has not been successfuly created")
        return count

    def checkout_user_should_not_be_present(self, checkout_user_body):
        checkout_users = self.get_checkout_users()
        count = len(checkout_users["data"])
        for index in range(0, count):
            if (checkout_user_body["firstName"] == checkout_users["data"][index]["firstName"]):
                self.logger.error(f"There is checkout user with email '{checkout_user_body['email']}'")
                break
        else:
            self.logger.info(f"There is no checkout user with email '{checkout_user_body['email']}'")
        return count