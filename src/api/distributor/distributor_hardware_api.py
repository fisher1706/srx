from src.api.api import API
from src.resources.messages import Message

class DistributorHardwareApi(API):
    def update_hardware(self, dto):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/hardware")
        token = self.get_distributor_token()
        response = self.send_put(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Hardware", id=dto['id'], operation="updated"))
        else:
            self.logger.error(str(response.content))

    def get_device_list(self):
        url = self.url.get_iothub_api_url_for_env("/generic/list-devices")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Device statuses", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]