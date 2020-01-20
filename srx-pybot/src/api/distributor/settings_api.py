from src.api.api import API

class SettingsApi(API):
    def __init__(self, case):
        super().__init__(case)

    def update_checkout_software_settings_shipto(self, dto, shipto_id):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/customers/shiptos/"+str(shipto_id)+"/checkout-software/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info("Checkout software settings of shipto with ID = '"+str(shipto_id)+"' has been successfully updated")
        else:
            self.logger.error(str(response.content))