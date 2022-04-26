from src.api.api import API
from src.resources.messages import Message
from glbl import Error

class AdminBillingApi(API):
    def billing_calculate(self, timestamp):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/calculateWaterMark")
        params = {
            "currentTime": timestamp
        }
        token = self.get_admin_token()
        response = self.send_post(url, token, params=params)
        Error.check(response.status_code == 200,
            Message.entity_operation_done.format(entity="Billing calculation", operation="completed"),
            str(response.content))

    def billing_transit(self, timestamp):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/transitInventoryStatus")
        params = {
            "currentTime": timestamp
        }
        token = self.get_admin_token()
        response = self.send_post(url, token, params=params)
        Error.check(response.status_code == 200,
            Message.entity_operation_done.format(entity="Billing transition", operation="completed"),
            str(response.content))
