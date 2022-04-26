from src.api.api import API
from src.resources.messages import Message
from src.fixtures.decorators import default_expected_code
from glbl import Log, Error

class OrganizationApi(API):
    def create_site(self, dto):
        url = self.url.get_api_url_for_env("/customer-portal/customer/facilities")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 201:
            Log.info(f"New Site '{dto['number']}' has been successfully created")
            response_json = response.json()
            site_id = (response_json["data"]["id"])
            return site_id
        Error.error(str(response.content))

    def create_subsite(self, dto):
        url = self.url.get_api_url_for_env("/customer-portal/customer/shared-spaces")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 201:
            Log.info(f"New Sub-Site '{dto['number']}' has been successfully created")
            response_json = response.json()
            subsite_id = (response_json["data"]["id"])
            return subsite_id
        Error.error(str(response.content))

    def create_supplier(self, dto):
        url = self.url.get_api_url_for_env("/customer-portal/customer/distributors")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 201:
            Log.info(f"New Supplier '{dto['name']}' has been successfully created")
            response_json = response.json()
            supplier_id = (response_json["data"]["id"])
            return supplier_id
        Error.error(str(response.content))

    def create_shipto(self, dto):
        url = self.url.get_api_url_for_env("/customer-portal/customer/shiptos")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 201:
            Log.info(f"New ShipTo '{dto['name']}' has been successfully created")
            response_json = response.json()
            shipto_id = (response_json["data"]["id"])
            return shipto_id
        Error.error(str(response.content))

    @default_expected_code(200)
    def delete_site(self, site_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/facilities/{site_id}")
        token = self.get_customer_token()
        response = self.send_delete(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(Message.entity_with_id_operation_done.format(entity="Site", id=site_id, operation="deleted"))
        else:
            Log.info(Message.info_operation_with_expected_code.format(entity="Site", operation="deletion", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def delete_subsite(self, subsite_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/shared-spaces/{subsite_id}")
        token = self.get_customer_token()
        response = self.send_delete(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(Message.entity_with_id_operation_done.format(entity="Sub-Site", id=subsite_id, operation="deleted"))
        else:
            Log.info(Message.info_operation_with_expected_code.format(entity="Sub-Site", operation="deletion", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def delete_supplier(self, supplier_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/distributors/{supplier_id}")
        token = self.get_customer_token()
        response = self.send_delete(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(Message.entity_with_id_operation_done.format(entity="Supplier", id=supplier_id, operation="deleted"))
        else:
            Log.info(Message.info_operation_with_expected_code.format(entity="supplier", operation="deletion", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def delete_shipto(self, shipto_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/shiptos/{shipto_id}")
        token = self.get_customer_token()
        response = self.send_delete(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(Message.entity_with_id_operation_done.format(entity="ShipTo", id=shipto_id, operation="deleted"))
        else:
            Log.info(Message.info_operation_with_expected_code.format(entity="ShipTo", operation="deletion", status_code=response.status_code, content=response.content))
