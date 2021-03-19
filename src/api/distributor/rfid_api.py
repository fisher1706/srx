from src.api.api import API
from src.resources.tools import Tools
from src.resources.messages import Message
from src.fixtures.decorators import Decorator

class RfidApi(API):
    @Decorator.default_expected_code(200)
    def create_rfid(self, location_id, expected_status_code, label=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids/create")
        token = self.get_distributor_token()
        if (label is None):
            label = Tools.random_string_u()
        dto = {
            "labelId": str(label),
            "locationId": location_id
        }
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"New RFID label '{dto['labelId']}' has been successfully created")
            response_json = response.json()
            new_rfid_id = (response_json["data"].split("/"))[-1]
            return_response = {
                "rfid_id": new_rfid_id,
                "label": label
            }
            return return_response
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="RFID label", operation="creation", status_code=response.status_code, content=response.content))

    def rfid_issue(self, serial_number, label):
        url = f"https://{serial_number}:{serial_number}@api-{self.context.session_context.environment}.storeroomlogix.com/api/webhook/events/rfid/issued"
        token = self.get_distributor_token()
        dto = {
            "reader_name": "pybot",
            "tag_reads": [
                {
                "epc": str(label)
                }
            ]
        }
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"RFID label '{label}' has been issued")
        else:
            self.logger.error(str(response.content))

    def get_rfid_labels(self, location_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(f"RFID labels of location with ID = '{location_id}' has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    @Decorator.default_expected_code(200)
    def update_rfid_label(self, location_id, rfid_id, status, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids/{rfid_id}/status-update")
        token = self.get_distributor_token()
        dto = {
            "state": status
        }
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"RFID label with ID = '{rfid_id}' has been successfully updated")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="RFID label", operation="creation", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def delete_rfid_label(self, location_id, rfid_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids/{rfid_id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"RFID label with ID = '{rfid_id}' has been successfully deleted")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="RFID label", operation="deletion", status_code=response.status_code, content=response.content))
