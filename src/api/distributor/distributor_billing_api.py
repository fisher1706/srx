from src.resources.messages import Message
from src.api.api import API

class DistributorBillingApi(API):
    def get_distributor_fees(self):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/fees")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Distributor fees", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]