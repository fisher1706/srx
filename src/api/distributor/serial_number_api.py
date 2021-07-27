from src.api.api import API
from src.fixtures.decorators import default_expected_code
from src.resources.messages import Message

class SerialNumberApi(API):
    @default_expected_code(201)
    def create_serial_number(self, location_id, shipto_id, serial_number, expected_status_code=None, additional_options=None, lot=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/serialnumber")
        token = self.get_distributor_token()
        dto = {
            "location":{
                "id": location_id
            },
            "shipto":{
                "id": shipto_id
            },
            "number": serial_number,
            "lot": lot
        }
        if (additional_options is not None):
            dto.update(additional_options)
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if (response.status_code == 201):
            response_json = response.json()
            sn_id = (response_json["data"].split("/"))[-1]
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Serial Number", id=sn_id, operation="created"))
            return sn_id
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Serial Number", operation="creation", status_code=response.status_code, content=response.content))

    @default_expected_code(201)
    def create_serial_numbers_by_lot(self, dto, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/serialnumber/lot/generate")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if (response.status_code == 201):
            self.logger.info(f"{dto['numberQuantity']} Serial Numbers have been created with lot = {dto['lot']}")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Serial Number", operation="creation by lot", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def update_serial_number(self, dto, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/serialnumber/")
        token = self.get_distributor_token()
        response = self.send_put(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if (response.status_code == 200):
            response_json = response.json()
            sn_id = (response_json["data"].split("/"))[-1]
            self.logger.info(f"Serial Number '{dto['number']}' has been successfully updated")
            return sn_id
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Serial Number", operation="updating", status_code=response.status_code, content=response.content))

    def get_serial_number(self, shipto_id):
        return self.get_serial_number_base(shipto_id)["entities"]

    def get_serial_number_count(self, shipto_id):
        return self.get_serial_number_base(shipto_id)["totalElements"]

    def get_serial_number_base(self, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/serialnumbers")
        params = {
            "shipToId": shipto_id
        }
        token = self.get_distributor_token()
        response = self.send_get(url, token, params)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Serial Number", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    @default_expected_code(200)
    def delete_serial_number(self, serial_number_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/serialnumber/{serial_number_id}")
        token = self.get_distributor_token()
        response = self.send_delete(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Serial Number", id=serial_number_id, operation="deleted"))
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Serial Number", operation="deletion", status_code=response.status_code, content=response.content))
