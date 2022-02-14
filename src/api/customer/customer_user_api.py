from src.api.api import API
from src.resources.messages import Message

class CustomerUserApi(API):
    def create_customer_user(self, dto):
        url = self.url.get_api_url_for_env("/customer-portal/customer/users")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(f"New customer user '{dto['email']}' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_customer_user = (response_json["data"]["id"])
        return new_customer_user

    def delete_customer_user(self, customer_user_id):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/users/{customer_user_id}")
        token = self.get_customer_token()
        response = self.send_delete(url, token)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Customer User", id=customer_user_id, operation="deleted"))
        else:
            self.logger.error(str(response.content))

    def update_customer_user(self, dto):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/users/{dto['id']}")
        token = self.get_customer_token()
        response = self.send_put(url, token, dto)
        if response.status_code == 200:
            self.logger.info(f"Customer user '{dto['email']}' has been successfully udated")
        else:
            self.logger.error(str(response.content))

    def get_customer_users(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/users")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Customer User", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def get_customer_user_transactions(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/reports/full-transactions?&sort=createdAt,desc")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Customer User Transation Report", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]
