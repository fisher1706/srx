import time
from src.api.api import API
from src.resources.tools import Tools
from src.resources.messages import Message

class SettingsApi(API):
    def update_reorder_controls_settings_shipto(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/checkout-software/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Reorder Controls settings of shipto", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def set_reorder_controls_settings_for_shipto(self, shipto_id, reorder_controls=None, track_ohi=None, scan_to_order=None, enable_reorder_control=None):
        #DEFAULT configuration is enabled Reorder Controls at MIN and enabled Track OHI. Scan to order is disabled
        if reorder_controls is None:
            reorder_controls = "MIN"
        if track_ohi is None:
            track_ohi = True
        if scan_to_order is None:
            scan_to_order = False
        if (enable_reorder_control is None and not scan_to_order):
            enable_reorder_control = True

        checkout_settings_dto = Tools.get_dto("reorder_controls_settings_dto.json")
        if not track_ohi:
            (checkout_settings_dto["settings"]["labelOptions"]).remove("TRACK_OHI")
        if not scan_to_order:
            (checkout_settings_dto["settings"]["labelOptions"]).remove("ENABLE_SCAN_TO_ORDER")
        if not enable_reorder_control:
            (checkout_settings_dto["settings"]["labelOptions"]).remove("ENABLE_REORDER_CONTROLS")
        if reorder_controls == "ISSUED":
            checkout_settings_dto["settings"]["reorderControls"] = "ADD_AS_ISSUED"
        self.update_reorder_controls_settings_shipto(checkout_settings_dto, shipto_id)

    def get_reorder_controls_settings_for_shipto(self, shipto_id):
        token = self.get_distributor_token()
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/checkout-software/settings")
        response = self.send_get(url, token)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Checkout Software settings of shipto", id=shipto_id, operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        if not bool(response_json["data"]):
            self.logger.error(f"Checkout software settings of shipto with ID = '{shipto_id}' are empty")
        return response_json["data"]

    def update_autosubmit_settings_shipto(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/autosubmit/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Auto-Submit settings of shipto", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def set_autosubmit_settings_shipto(self, shipto_id, enabled=None, immediately=None, as_order=None):
        autosubmit_settings_dto = Tools.get_dto("autosubmit_settings_dto.json")
        autosubmit_settings_dto["settings"]["submitImmediately"] = bool(immediately)
        autosubmit_settings_dto["settings"]["autoSubmit"] = bool(enabled)
        autosubmit_settings_dto["settings"]["autoSubmitAsOrder"] = bool(as_order)
        self.update_autosubmit_settings_shipto(autosubmit_settings_dto, shipto_id)

    def update_rl_rules_settings_shipto(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/customer-settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="RL Rules settings of shipto", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def set_rl_rules_settings_shipto(self, shipto_id, order="ORDERED_AND_QUOTED", pricing="NULL_PRICE"):
        rl_rules_settings_dto = Tools.get_dto("rl_rules_dto.json")
        rl_rules_settings_dto["replenishmentListRules"]["settings"]["orderSubmitSettings"] = order
        rl_rules_settings_dto["replenishmentListRules"]["settings"]["pricingNotAvailableBehavior"] = pricing
        self.update_rl_rules_settings_shipto(rl_rules_settings_dto, shipto_id)

    def update_serialization_settings_shipto(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/serialnumber/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Serialization settings of shipto", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def set_serialization_settings_shipto(self, shipto_id, expiration=None, alarm=None, sleep=0):
        serialization_settings_dto = Tools.get_dto("serialization_settings_dto.json")
        serialization_settings_dto["settings"]["enableAutoExpire"] = bool(expiration)
        serialization_settings_dto["settings"]["daysUntilAutoExpiration"] = 0 if expiration is None else expiration
        serialization_settings_dto["settings"]["enableExpirationAlarm"] = bool(alarm)
        serialization_settings_dto["settings"]["daysUntilExpirationAlarm"] = 0 if alarm is None else alarm
        self.update_serialization_settings_shipto(serialization_settings_dto, shipto_id)
        time.sleep(sleep)

    def update_adjustment_settings(self, dto, shipto_id, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/shiptos/{shipto_id}/settings/inventory-adjustment")
        token = self.get_distributor_token()
        response = self.send_put(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Adjustment settings of shipto", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def save_and_adjust_moving_status(self, enabled, shipto_id, customer_id=None, current_shiptos=None, use_all=False, sleep=0):
        if current_shiptos is None:
            current_shiptos = list()
        time.sleep(sleep)
        dto = {
            "currentShipTos": current_shiptos,
            "enabled": enabled,
            "useAll": use_all
        }
        self.update_adjustment_settings(dto, shipto_id, customer_id)
        time.sleep(sleep)

    def get_adjustment_settings(self, shipto_id, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/shiptos/{shipto_id}/settings/inventory-adjustment")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Adjustment settings of shipto", id=shipto_id, operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def update_vmi_settings(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/vmilist/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="VMI List settings of shipto", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def update_checkout_settings(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/allow/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="QR Code Kit & Checkout Portal settings of shipto", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def set_checkout_settings(self, shipto_id, checkout_software=True, qr_code_kit=True):
        checkout_settings_dto = Tools.get_dto("checkout_settings_dto.json")
        checkout_settings_dto["settings"]["enableCheckoutSoftware"] = bool(checkout_software)
        checkout_settings_dto["settings"]["enableQrCodeKit"] = bool(qr_code_kit)
        self.update_checkout_settings(checkout_settings_dto, shipto_id)

    def update_customer_level_catalog_flag(self, dto, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/catalog/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="CLC flag of customer", id=customer_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def set_customer_level_catalog_flag(self, flag, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        dto = {
            "customerCatalogEnabled": flag
        }
        self.update_customer_level_catalog_flag(dto, customer_id)

    def get_cache_settings(self, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/customer-settings")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Cache settings of ShipTo", id=shipto_id, operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def update_cache_settings(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/customer-settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Cache settings of ShipTo", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def update_critical_min_and_stockout_alert_settings(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/critical-min-alert/settings")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Critical Min & Stockout settings of ShipTo", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def set_critical_min_and_stockout_alert_settings(self, shipto_id, critical_min, stockout, emails=None):
        critical_min_alert_dto = Tools.get_dto("critical_min_alert_settings.json")
        critical_min_alert_dto["settings"]["enabled"] = bool(critical_min)
        critical_min_alert_dto["settings"]["enableStockOut"] = bool(stockout)
        critical_min_alert_dto["settings"]["alertEmails"] = emails
        self.update_critical_min_and_stockout_alert_settings(critical_min_alert_dto, shipto_id)

    def update_vmi_list_integration_settings(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/shiptos/{shipto_id}/vmi-list-integration/settings/save")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="VMI List integration settings of ShipTo", id=shipto_id, operation="updated"))
        else:
            self.logger.error(str(response.content))

    def set_critical_min_and_stockout_alert_settings(self, shipto_id):
        vmi_integration_dto = Tools.get_dto("vmi_integration_settings_dto.json")
        self.update_vmi_list_integration_settings(vmi_integration_dto, shipto_id)
