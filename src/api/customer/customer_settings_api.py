from src.api.api import API
from src.resources.tools import Tools
from src.resources.messages import Message
from glbl import Log, Error

class CustomerSettingsApi(API):
    def update_reorder_controls_settings_shipto(self, dto, supplier_id):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/distributors/{supplier_id}/checkout-software/settings")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            Log.info(Message.entity_with_id_operation_done.format(entity="Reorder Controls settings of shipto", id=supplier_id, operation="updated"))
        else:
            Error.error(str(response.content))

    def set_reorder_controls_settings_for_shipto(self, supplier_id, reorder_controls=None, track_ohi=None, scan_to_order=None, enable_reorder_control=None):
        #DEFAULT configuration is enabled Reorder Controls at MIN and enabled Track OHI. Scan to order is disabled
        if reorder_controls is None:
            reorder_controls = "MIN"
        if track_ohi is None:
            track_ohi = True
        if scan_to_order is None:
            scan_to_order = False
        if (enable_reorder_control is None and not scan_to_order):
            enable_reorder_control = True

        checkout_settings_dto = Tools.get_dto("customer_reorder_controls_settings_dto.json")
        if not track_ohi:
            (checkout_settings_dto["labelOptions"]).remove("TRACK_OHI")
        if not scan_to_order:
            (checkout_settings_dto["labelOptions"]).remove("ENABLE_SCAN_TO_ORDER")
        if not enable_reorder_control:
            (checkout_settings_dto["labelOptions"]).remove("ENABLE_REORDER_CONTROLS")
        if reorder_controls == "ISSUED":
            checkout_settings_dto["reorderControls"] = "ADD_AS_ISSUED"
        self.update_reorder_controls_settings_shipto(checkout_settings_dto, supplier_id)
