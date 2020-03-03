from src.api.api import API
from src.api.api_methods import ApiMethods as apim

class SettingsApi(API):
    def __init__(self, case):
        super().__init__(case)

    def update_checkout_software_settings_shipto(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/checkout-software/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Checkout software settings of shipto with ID = '{shipto_id}' has been successfully updated")
        else:
            self.logger.error(str(response.content))

    def set_checkout_software_settings_for_shipto(self, shipto_id, reorder_controls="MIN", track_ohi=True, scan_to_order=True, enable_reorder_control=True):
        checkout_settings_dto = apim.get_dto("checkout_settings_dto.json")
        if (track_ohi == False):
            (checkout_settings_dto["settings"]["labelOptions"]).remove("TRACK_OHI")
        if (scan_to_order == False):
            (checkout_settings_dto["settings"]["labelOptions"]).remove("ENABLE_SCAN_TO_ORDER")
        if (enable_reorder_control == False):
            (checkout_settings_dto["settings"]["labelOptions"]).remove("ENABLE_REORDER_CONTROLS")
        if (reorder_controls == "ISSUED"):
            checkout_settings_dto["settings"]["reorderControls"] = "ADD_AS_ISSUED"
        self.update_checkout_software_settings_shipto(checkout_settings_dto, shipto_id)