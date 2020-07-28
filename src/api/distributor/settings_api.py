from src.api.api import API
from src.resources.tools import Tools

class SettingsApi(API):
    def update_checkout_software_settings_shipto(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/checkout-software/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Checkout software settings of shipto with ID = '{shipto_id}' has been successfully updated")
        else:
            self.logger.error(str(response.content))

    def set_checkout_software_settings_for_shipto(self, shipto_id, reorder_controls=None, track_ohi=None, scan_to_order=None, enable_reorder_control=None):
        if (reorder_controls is None):
            reorder_controls = "MIN"
        if (track_ohi is None):
            track_ohi = True
        if (scan_to_order is None):
            scan_to_order = True
        if (enable_reorder_control is None):
            enable_reorder_control = True

        checkout_settings_dto = Tools.get_dto("checkout_settings_dto.json")
        if (not track_ohi):
            (checkout_settings_dto["settings"]["labelOptions"]).remove("TRACK_OHI")
        if (not scan_to_order):
            (checkout_settings_dto["settings"]["labelOptions"]).remove("ENABLE_SCAN_TO_ORDER")
        if (not enable_reorder_control):
            (checkout_settings_dto["settings"]["labelOptions"]).remove("ENABLE_REORDER_CONTROLS")
        if (reorder_controls == "ISSUED"):
            checkout_settings_dto["settings"]["reorderControls"] = "ADD_AS_ISSUED"
        self.update_checkout_software_settings_shipto(checkout_settings_dto, shipto_id)

    def get_checkout_software_settings_for_shipto(self, shipto_id):
        token = self.get_distributor_token()
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/checkout-software/settings")
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Checkout software settings of shipto with ID = '{shipto_id}' has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        if (not bool(response_json["data"])):
            self.logger.error(f"Checkout software settings of shipto with ID = '{shipto_id}' are empty")
        return response_json["data"]

    def update_autosubmit_settings_shipto(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Auto-Submit settings of shipto with ID = '{shipto_id}' has been successfully updated")
        else:
            self.logger.error(str(response.content))

    def set_autosubmit_settings_shipto(self, shipto_id, enabled=None, immediately=None, as_order=None):
        autosubmit_settings_dto = Tools.get_dto("autosubmit_settings_dto.json")
        autosubmit_settings_dto["transactionAutoSubmitSettings"]["submitImmediately"] = bool(immediately)
        autosubmit_settings_dto["transactionAutoSubmitSettings"]["autoSubmit"] = bool(enabled)
        autosubmit_settings_dto["transactionAutoSubmitSettings"]["autoSubmitAsOrder"] = bool(as_order)
        self.update_autosubmit_settings_shipto(autosubmit_settings_dto, shipto_id)

    def update_rl_rules_settings_shipto(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/customer-settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"RL Rules settings of shipto with ID = '{shipto_id}' has been successfully updated")
        else:
            self.logger.error(str(response.content))

    def set_rl_rules_settings_shipto(self, shipto_id, order="ORDERED_AND_QUOTED", pricing="NULL_PRICE"):
        rl_rules_settings_dto = Tools.get_dto("rl_rules_dto.json")
        rl_rules_settings_dto["replenishmentListRules"]["settings"]["orderSubmitSettings"] = order
        rl_rules_settings_dto["replenishmentListRules"]["settings"]["pricingNotAvailableBehavior"] = pricing
        self.update_rl_rules_settings_shipto(rl_rules_settings_dto, shipto_id)