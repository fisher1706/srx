from src.api.api import API
from src.fixtures.decorators import Decorator
from src.resources.tools import Tools
from src.resources.messages import Message

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
            self.logger.info(Message.entity_operation_done.format(entity="Distributor User", operation="got"))
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
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if response.status_code == 201:
            self.logger.info(f"Distributor User {dto['email']} has been successfuly created")
            response_json = response.json()
            new_user_id = (response_json["data"].split("/"))[-1]
            return new_user_id
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="User", operation="creation", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def delete_distributor_user(self, user_id, expected_status_code, distributor_id=None):
        if distributor_id is None:
            distributor_id = self.data.distributor_id
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/{distributor_id}/users/{user_id}/delete")
        token = self.get_admin_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Distributor User", operation="deleted"))
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="User", operation="deletion", status_code=response.status_code, content=response.content))