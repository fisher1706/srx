from re import T
from src.api.api import API
from src.fixtures.decorators import Decorator
from src.resources.tools import Tools

class AdminUserApi(API):
    def get_distributor_user(self, email=None, distributor_id=None):
        if distributor_id is None:
            distributor_id = self.data.distributor_id
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/{distributor_id}/users/pageable")
        params = dict()
        Tools.add_to_dict_if_not_none(params, "email", email)
        token = self.get_admin_token()
        response = self.send_get(url, token, params)
        if response.status_code == 200:
            self.logger.info("Distributor user has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    @Decorator.default_expected_code(201)
    def create_distributor_user(self, dto, expected_status_code, distributor_id=None):
        if distributor_id is None:
            distributor_id = self.data.distributor_id
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/{distributor_id}/users/admin/create")
        token = self.get_admin_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        if response.status_code == 201:
            self.logger.info(f"Distributor User {dto['email']} has been successfuly created")
            response_json = response.json()
            new_user_id = (response_json["data"].split("/"))[-1]
            return new_user_id
        else:
            self.logger.info(f"User creation completed with status_code = '{response.status_code}', as expected: {response.content}")

    @Decorator.default_expected_code(200)
    def delete_distributor_user(self, user_id, expected_status_code, distributor_id=None):
        if distributor_id is None:
            distributor_id = self.data.distributor_id
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/{distributor_id}/users/{user_id}/delete")
        token = self.get_admin_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        if response.status_code == 200:
            self.logger.info(f"Distributor user has been successfully deleted")
        else:
            self.logger.info(f"User deletion completed with status_code = '{response.status_code}', as expected: {response.content}")