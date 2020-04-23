from src.api.api import API
import time

class UserApi(API):
    def __init__(self, case):
        super().__init__(case)

    def get_distributor_users(self, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/shiptos/{shipto_id}/distributor-users")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Distributor users have been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def get_first_distributor_user(self, shipto_id):
        distributor_users = self.get_distributor_users(shipto_id)
        return distributor_users[0]

    def get_customer_users(self, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/shiptos/{shipto_id}/customer-users")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Customer users have been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def get_first_customer_user(self, shipto_id):
        customer_users = self.get_customer_users(shipto_id)
        return customer_users[0]

    def create_distributor_user(self, dto):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/superusers/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 201):
            self.logger.info(f"User {dto['email']} has been successfuly created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_user_id = (response_json["data"].split("/"))[-1]
        return new_user_id

    def get_distributor_super_user_by_email(self, email):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/superusers/pageable?email={email}")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Distributor super user has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def delete_user(self, id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/superusers/{id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("Distributor super user has been successfully deleted")
        else:
            self.logger.error(str(response.content))

