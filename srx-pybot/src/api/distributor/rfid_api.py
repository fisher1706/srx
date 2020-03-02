from src.api.api import API
import random

class RfidApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_rfid(self, location_id, label=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids/create")
        token = self.get_distributor_token()
        if (label is None):
            label = self.case.random_string_u()
        dto = {
            "labelId": str(label),
            "locationId": location_id
        }
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"New RFID label '{dto['labelId']}' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_rfid_id = (response_json["data"].split("/"))[-1]
        return_response = {
            "rfid_id": new_rfid_id,
            "label": label
        }
        return return_response

    def get_manifest(self, device_id):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/manifest")
        token = self.get_distributor_token()
        response = self.send_post(url, token, line_data=device_id)
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
                device_id = self.case.random_string_u(20)
            manifest_data = self.get_manifest(device_id)
            if (len(manifest_data["items"]) == 0 and manifest_data["type"] == "DELIVERY"):
                response = {
                    "data": manifest_data,
                    "device_id": device_id
                }
                return response
            else:
                if (stop_cycle == True):
                    self.logger.error("Error during getting the delivery manifest")

    def create_return_manifest(self):
        device_id = self.case.random_string_u(20)
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/return")
        token = self.get_distributor_token()
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
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Manifest with ID = '{manifest_id}' has been successfully closed")
        else:
            self.logger.error(str(response.content))

    def add_to_manifest(self, label, manifest_id, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_id}/shiptos/{shipto_id}/items/add")
        token = self.get_distributor_token()
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
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Manifest with ID = '{manifest_id}' has been successfully submitted")
        else:
            self.logger.error(str(response.content))

    def rfid_issue(self, serial_number, label):
        url = f"https://{serial_number}:{serial_number}@api-{self.case.activity.variables.api_environment}.storeroomlogix.com/api/webhook/events/rfid/issued"
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

    def rfid_put_away(self, shipto_id, rfid_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/putaway/shiptos/{shipto_id}/rfids/{rfid_id}/available")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"RFID label with ID = '{rfid_id}' has been put away")
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

    def update_rfid_label(self, location_id, rfid_id, status):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids/{rfid_id}/status-update")
        token = self.get_distributor_token()
        dto = {
            "state": status
        }
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"RFID label with ID = '{rfid_id}' has been successfully updated")
        else:
            self.logger.error(str(response.content))