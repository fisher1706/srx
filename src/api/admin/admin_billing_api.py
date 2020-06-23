from src.api.api import API

class AdminBillingApi(API):
    def billing_calculate(self, timestamp):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/calculateWaterMark?currentTime={timestamp}")
        token = self.get_admin_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("Billing calculation has been completed")
        else:
            self.logger.error(str(response.content))

    def billing_transit(self, timestamp):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/transitInventoryStatus?currentTime={timestamp}")
        token = self.get_admin_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("Billing transition has been completed")
        else:
            self.logger.error(str(response.content))