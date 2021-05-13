from src.api.api import API
from src.resources.messages import Message
from src.fixtures.decorators import Decorator

class ShiptoApi(API):
    @Decorator.default_expected_code(201)
    def create_shipto(self, dto, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shipto/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 201):
            self.logger.info(f"New ShipTo '{dto['number']}' has been successfully created")
            response_json = response.json()
            new_shipto = (response_json["data"].split("/"))[-1]
            return new_shipto
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="ShipTo", operation="creation", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def delete_shipto(self, shipto_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shipto/{shipto_id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"ShipTo with ID = '{shipto_id}' has been successfully deleted")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="ShipTo", operation="deletion", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def update_shipto(self, dto, shipto_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shipto/{shipto_id}/update")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"ShipTo with ID = '{shipto_id}' has been successfully updated")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="ShipTo", operation="updating", status_code=response.status_code, content=response.content))

    def get_shipto_by_number(self, number):
        if number is None:
            url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/pageable")
        else:
            url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/pageable?number={number}")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("ShipTo has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json

    def get_po_number_by_number(self, number):
        response = self.get_shipto_by_number(number)
        return response["data"]["entities"][0]["poNumber"]

    def check_po_number_by_number(self, number, expected_po_number):
        actual_po_number = self.get_po_number_by_number(number)
        if (actual_po_number == expected_po_number):
            self.logger.info("PO number is correct")
        else:
            self.logger.error(f"PO number should be '{expected_po_number}', but now it is '{actual_po_number}'")

    def get_shipto_by_id(self, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/shiptos/{shipto_id}")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("ShipTo has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]