from src.api.api import API
from src.resources.tools import Tools
from src.fixtures.decorators import default_expected_code
from src.resources.messages import Message

class MobileRfidApi(API):
    def get_manifest(self, device_id):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/manifest")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token, data=device_id)
        if (response.status_code == 200):
            response_json = response.json()
            self.logger.info(f"Manifest with ID = '{response_json['data']['id']}' has been successfully got")
        else:
            self.logger.error(str(response.content))
        return response_json["data"]

    def get_new_delivery_manifest(self, device_id=None):
        stop_cycle = False
        if (device_id is not None):
            stop_cycle = True
        while True:
            if (device_id is None):
                device_id = Tools.random_string_u(20)
            manifest_data = self.get_manifest(device_id)
            if (len(manifest_data["items"]) == 0 and manifest_data["type"] == "DELIVERY"):
                response = {
                    "data": manifest_data,
                    "device_id": device_id
                }
                return response
            else:
                if (stop_cycle):
                    self.logger.error("Error during getting the delivery manifest")

    def create_return_manifest(self):
        device_id = Tools.random_string_u(20)
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/return")
        token = self.get_mobile_distributor_token()
        additional_header = {
            "deviceId": device_id
        }
        response = self.send_post(url, token, additional_headers=additional_header)
        if (response.status_code == 200):
            response_json = response.json()
            self.logger.info(f"Return manifest with ID = '{response_json['data']['id']}' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response = {
            "data": response_json["data"],
            "device_id": device_id
        }
        return response

    def close_manifest(self, manifest_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_id}/close")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Manifest with ID = '{manifest_id}' has been successfully closed")
        else:
            self.logger.error(str(response.content))

    def add_to_manifest(self, label, manifest_id, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_id}/shiptos/{shipto_id}/items/add")
        token = self.get_mobile_distributor_token()
        dto = {
            "epc": str(label)
        }
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Label '{label}' has been successfully added to the manifest")
        else:
            self.logger.error(str(response.content))

    def submit_manifest(self, manifest_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_id}/submit")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Manifest with ID = '{manifest_id}' has been successfully submitted")
        else:
            self.logger.error(str(response.content))

    def rfid_put_away(self, shipto_id, rfid_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/putaway/shiptos/{shipto_id}/rfids/{rfid_id}/available")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"RFID label with ID = '{rfid_id}' has been put away")
        else:
            self.logger.error(str(response.content))

    @default_expected_code(200)
    def create_rfid_label(self, location_id, shipto_id, product_sku, expected_status_code=None, label = None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids/create")
        token = self.get_mobile_distributor_token()
        if (label is None):
            label = Tools.random_string_u()
        dto = {
            "id": shipto_id,
            "labelId": str(label),
            "product_sku": product_sku
        }
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"RFID label for location with ID = '{location_id}' has been created")
        else:
            self.logger.info(f"Create RFID label completed with status_code = '{response.status_code}', as expected: {response.content}")

    @default_expected_code(200)
    def delete_rfid_label(self, location_id, label_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/labels/{label_id}/delete")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"RFID label = '{label_id}' has been deleted")
        else:
            self.logger.info(f"Delete RFID label completed with status_code = '{response.status_code}', as expected: {response.content}")

    def get_rfids_labels_by_location(self, location_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids")
        token = self.get_mobile_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
             self.logger.info(f"RFID labels of location with ID = '{location_id}' has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]