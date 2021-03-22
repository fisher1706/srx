from src.api.api import API
import urllib.parse
from src.fixtures.decorators import Decorator

class UserApi(API):
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

    def create_customer_user(self, customer_id, email):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/users")
        token = self.get_distributor_token()
        dto = {
            "email": email
        }
        response = self.send_put(url, token, dto)
        if (response.status_code == 201):
            self.logger.info(f"Customer Super User {email} has been successfuly created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_user_id = (response_json["data"].split("/"))[-1]
        return new_user_id

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

    def create_distributor_superuser(self, dto):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/superusers/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 201):
            self.logger.info(f"Distributor Super User {dto['email']} has been successfuly created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_user_id = (response_json["data"].split("/"))[-1]
        return new_user_id

    @Decorator.default_expected_code(201)
    def create_distributor_user(self, dto, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/users/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        if (response.status_code == 201):
            self.logger.info(f"Distributor User {dto['email']} has been successfuly created")
            response_json = response.json()
            new_user_id = (response_json["data"].split("/"))[-1]
            return new_user_id
        else:
            self.logger.info(f"User creation completed with status_code = '{response.status_code}', as expected: {response.content}")

    @Decorator.default_expected_code(200)
    def update_distributor_user(self, dto, expected_status_code, user_id=None):
        if (user_id is None):
            user_id = dto.get("id")
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/users/{user_id}/update")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        if (response.status_code == 200):
            self.logger.info(f"User {dto['email']} has been successfuly updated")
        else:
            self.logger.info(f"User updating completed with status_code = '{response.status_code}', as expected: {response.content}")

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

    def get_distributor_user(self, email):
        url_string = "/distributor-portal/distributor/users/pageable?"
        if (email is not None):
            email = urllib.parse.quote(email)
            url_string += f"email={email}&"
        url = self.url.get_api_url_for_env(url_string)
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Distributor user has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def delete_superuser(self, id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/superusers/{id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("Distributor super user has been successfully deleted")
        else:
            self.logger.error(str(response.content))

    @Decorator.default_expected_code(200)
    def delete_distributor_user(self, user_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/users/{user_id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        if (response.status_code == 200):
            self.logger.info(f"Distributor user has been successfully deleted")
        else:
            self.logger.info(f"User deletion completed with status_code = '{response.status_code}', as expected: {response.content}")

    def get_acl_sctructure(self):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/acl-structure")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("ACL structure has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def create_security_group(self, dto):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/user-groups/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Security Group {dto['name']} has been successfuly created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_security_group_id = (response_json["data"].split("/"))[-1]
        return new_security_group_id
        
    def delete_security_group(self, security_group_id, new_security_group_id=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/user-groups/{security_group_id}/delete")
        if (new_security_group_id is not None):
            url += f"/{new_security_group_id}"
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Security Group with ID = '{security_group_id}' has been successfuly deleted")
        else:
            self.logger.error(str(response.content))

    def clear_acl_cache(self):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/clear-acl-cache")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if response.status_code != 200:
            self.logger.error(str(response.content))

    def get_current_user(self):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/users/current")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Current User has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]
