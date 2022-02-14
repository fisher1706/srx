from src.api.api import API
from src.resources.messages import Message
from src.resources.tools import Tools
from src.fixtures.decorators import default_expected_code

class ShiptoApi(API):
    @default_expected_code(201)
    def create_shipto(self, dto, expected_status_code=None, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/shipto/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 201:
            self.logger.info(f"New ShipTo '{dto['number']}' has been successfully created")
            response_json = response.json()
            new_shipto = (response_json["data"].split("/"))[-1]
            return new_shipto
        self.logger.info(Message.info_operation_with_expected_code.format(entity="ShipTo", operation="creation", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def delete_shipto(self, shipto_id, expected_status_code=None, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/shipto/{shipto_id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="ShipTo", id=shipto_id, operation="deleted"))
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="ShipTo", operation="deletion", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def update_shipto(self, dto, shipto_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shipto/{shipto_id}/update")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="ShipTo", id=shipto_id, operation="updated"))
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="ShipTo", operation="updating", status_code=response.status_code, content=response.content))

    def get_shipto_by_number(self, number):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/pageable")
        params = dict()
        Tools.add_to_dict_if_not_none(params, "number", number)
        token = self.get_distributor_token()
        response = self.send_get(url, token, params=params)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="ShipTo", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json

    def get_shiptos_total_elements(self):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/pageable")
        params = {
            "size": 1
        }
        token = self.get_distributor_token()
        response = self.send_get(url, token, params=params)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Product", operation="got"))
            response_json = response.json()
            return response_json["data"]["totalElements"]
        self.logger.error(str(response.content))

    def get_po_number_by_number(self, number):
        response = self.get_shipto_by_number(number)
        return response["data"]["entities"][0]["poNumbers"][0]["value"]

    def check_po_number_by_number(self, number, expected_po_number):
        actual_po_number = self.get_po_number_by_number(number)
        if actual_po_number == expected_po_number:
            self.logger.info("PO number is correct")
        else:
            self.logger.error(f"PO number should be '{expected_po_number}', but now it is '{actual_po_number}'")

    def get_shipto_by_id(self, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/shiptos/{shipto_id}")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="ShipTo", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]
