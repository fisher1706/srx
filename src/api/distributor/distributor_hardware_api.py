from src.api.api import API
from src.resources.messages import Message
from glbl import Log, Error

class DistributorHardwareApi(API):
    def update_hardware(self, dto):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/hardware")
        token = self.get_distributor_token()
        response = self.send_put(url, token, dto)
        if response.status_code == 200:
            Log.info(Message.entity_with_id_operation_done.format(entity="Hardware", id=dto['id'], operation="updated"))
        else:
            Error.error(str(response.content))

    def get_device_list(self):
        url = self.url.get_iothub_api_url_for_env("/generic/list-devices")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            Log.info(Message.entity_operation_done.format(entity="Device statuses", operation="got"))
        else:
            Error.error(str(response.content))
        response_json = response.json()
        return response_json["data"]
