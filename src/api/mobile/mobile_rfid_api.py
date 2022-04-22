from src.api.api import API
from src.resources.tools import Tools
from src.fixtures.decorators import default_expected_code
from src.resources.messages import Message
from glbl import Log, Error

class MobileRfidApi(API):
    def get_manifest(self, device_id):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/manifest")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token, data=device_id)
        if response.status_code == 200:
            response_json = response.json()
            Log.info(f"Manifest with ID = '{response_json['data']['id']}' has been successfully got")
        else:
            Error.error(str(response.content))
        return response_json["data"]

    def get_new_delivery_manifest(self, device_id=None):
        stop_cycle = False
        if device_id is not None:
            stop_cycle = True
        while True:
            if device_id is None:
                device_id = Tools.random_string_u(20)
            manifest_data = self.get_manifest(device_id)
            if (len(manifest_data["items"]) == 0 and manifest_data["type"] == "DELIVERY"):
                response = {
                    "data": manifest_data,
                    "device_id": device_id
                }
                return response
            if stop_cycle:
                Error.error("Error during getting the delivery manifest")

    @default_expected_code(200)
    def create_manifest(self, manifest_type, expected_status_code=None):
        device_id = Tools.random_string_u(20)
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_type}")
        token = self.get_mobile_distributor_token()
        additional_header = {
            "deviceId": device_id
        }
        response = self.send_post(url, token, additional_headers=additional_header)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        response_json = response.json()
        if response.status_code == 200:
            Log.info(f"{manifest_type} manifest with ID = '{response_json['data']['id']}' has been successfully created")
        else:
            Log.info(f"{manifest_type} manifest has not been created and completed with status code = '{response.status_code}'")
        response = {
            "data": response_json["data"],
            "device_id": device_id
        }
        return response

    def close_manifest(self, manifest_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_id}/close")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token)
        if response.status_code == 200:
            Log.info(f"Manifest with ID = '{manifest_id}' has been successfully closed")
        else:
            Error.error(str(response.content))

    @default_expected_code(200)
    def add_to_manifest(self, label, manifest_id, shipto_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_id}/shiptos/{shipto_id}/items/add")
        token = self.get_mobile_distributor_token()
        dto = {
            "epc": str(label)
        }
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(f"Label '{label}' has been successfully added to the manifest")
        else:
            Log.info(f"Adding item to Manifest completed with status_code = '{response.status_code}', as expected: {response.content}")

    @default_expected_code(200)
    def submit_manifest(self, manifest_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_id}/submit")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(f"Manifest with ID = '{manifest_id}' has been successfully submitted")
        else:
            Log.info(f"Submit Manifest with ID = '{manifest_id}' completed with code = '{response.status_code}'")

    @default_expected_code(200)
    def rfid_put_away(self, shipto_id, rfid_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/putaway/shiptos/{shipto_id}/rfids/{rfid_id}/available")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(f"RFID label with ID = '{rfid_id}' has been put away")
        else:
            Log.info(f"RFID PutAway completed with status_code = '{response.status_code}', as expected: {response.content}")

    @default_expected_code(200)
    def create_rfid_label(self, location_id, shipto_id, product_sku, expected_status_code=None, label=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids/create")
        token = self.get_mobile_distributor_token()
        if label is None:
            label = Tools.random_string_u()
        dto = {
            "id": shipto_id,
            "labelId": str(label),
            "product_sku": product_sku
        }
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(f"RFID label for location with ID = '{location_id}' has been created")
        else:
            Log.info(f"Create RFID label completed with status_code = '{response.status_code}', as expected: {response.content}")

    @default_expected_code(200)
    def delete_rfid_label(self, location_id, label_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/labels/{label_id}/delete")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(f"RFID label = '{label_id}' has been deleted")
        else:
            Log.info(f"Delete RFID label completed with status_code = '{response.status_code}', as expected: {response.content}")

    def get_rfids_labels_by_location(self, location_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/locations/{location_id}/rfids")
        token = self.get_mobile_distributor_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            Log.info(f"RFID labels of location with ID = '{location_id}' has been successfully got")
        else:
            Error.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    @default_expected_code(200)
    def delete_rfid_label_from_manifest(self, manifest_id, item_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_id}/items/{item_id}/delete")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(f"Item with ID = '{item_id}' has been successfully deleted from the manifest with ID = '{manifest_id}'")
        else:
            Log.info(f"Item with ID = '{item_id}' has not been deleted from the manifest with ID = '{manifest_id}' and completed with code = '{response.status_code}'")

    @default_expected_code(200)
    def replace_rfid_label_in_manifest(self, manifest_id, item_id, label, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/manifest/{manifest_id}/items/{item_id}/replace")
        token = self.get_mobile_distributor_token()
        dto = {
            "epc": str(label + "_replaced")
        }
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            Log.info(f"Item with ID = '{item_id}' has been successfully replaced from the manifest with ID = '{manifest_id}'")
        else:
            Log.info(f"Item with ID = '{item_id}' has not been replaced in the manifest with ID = '{manifest_id}' and completed with code = '{response.status_code}'")
