import pytest
import copy
from src.resources.locator import Locator
from src.resources.tools import Tools
from src.pages.general.login_page import LoginPage
from src.pages.customer.reorder_list_page import ReorderListPage
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_locker_location import setup_locker_location
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.activity_log_api import ActivityLogApi

class TestTransactions():
    @pytest.mark.regression
    def test_different_multiple_po_number(self, ui, delete_shipto):
        ui.testrail_case_id = 105

        lp = LoginPage(ui)
        rlp = ReorderListPage(ui)
        sa = ShiptoApi(ui)
        ta = TransactionApi(ui)
        la = LocationApi(ui)
        sta = SettingsApi(ui)

        response_location_1 = setup_location(ui)
        response_location_2 = setup_location(ui)

        product_1_dto = response_location_1["product"]
        product_2_dto = response_location_2["product"]
        shipto_1_dto = response_location_1["shipto"]
        shipto_2_dto = response_location_2["shipto"]
        new_shipto_1 = response_location_1["shipto_id"]
        new_shipto_2 = response_location_2["shipto_id"]
        
        sta.set_checkout_software_settings_for_shipto(new_shipto_1)
        sta.set_checkout_software_settings_for_shipto(new_shipto_1)

        ta.create_active_item(new_shipto_1, la.get_ordering_config_by_sku(new_shipto_1, product_1_dto["partSku"]))
        ta.create_active_item(new_shipto_2, la.get_ordering_config_by_sku(new_shipto_2, product_2_dto["partSku"]))

        lp.log_in_customer_portal()
        rlp.sidebar_orders_and_quotes()
        rlp.unselect_all()
        rlp.select_by_sku(product_1_dto["partSku"])
        rlp.select_by_sku(product_2_dto["partSku"])
        po_number_body = {
            shipto_1_dto["number"]:shipto_1_dto["poNumber"],
            shipto_2_dto["number"]:shipto_2_dto["poNumber"]
        }
        rlp.check_po_number_in_dialog(po_number_body.copy())
        new_po_number_body = {
            shipto_1_dto["number"]:Tools.random_string_l(10),
            shipto_2_dto["number"]:Tools.random_string_l(10)
        }
        rlp.submit_replenishment_list_different_po(new_po_number_body)


        sa.check_po_number_by_number(shipto_1_dto["number"], new_po_number_body[shipto_1_dto["number"]])
        sa.check_po_number_by_number(shipto_2_dto["number"], new_po_number_body[shipto_2_dto["number"]])

    @pytest.mark.regression
    def test_general_multiple_po_number(self, ui, delete_shipto):
        ui.testrail_case_id = 106

        lp = LoginPage(ui)
        rlp = ReorderListPage(ui)
        sa = ShiptoApi(ui)
        ta = TransactionApi(ui)
        la = LocationApi(ui)
        sta = SettingsApi(ui)

        response_location_1 = setup_location(ui)
        response_location_2 = setup_location(ui)
        product_1_dto = response_location_1["product"]
        product_2_dto = response_location_2["product"]
        shipto_1_dto = response_location_1["shipto"]
        shipto_2_dto = response_location_2["shipto"]
        new_shipto_1 = response_location_1["shipto_id"]
        new_shipto_2 = response_location_2["shipto_id"]
        
        sta.set_checkout_software_settings_for_shipto(new_shipto_1)
        sta.set_checkout_software_settings_for_shipto(new_shipto_1)

        ta.create_active_item(new_shipto_1, la.get_ordering_config_by_sku(new_shipto_1, product_1_dto["partSku"]))
        ta.create_active_item(new_shipto_2, la.get_ordering_config_by_sku(new_shipto_2, product_2_dto["partSku"]))

        lp.log_in_customer_portal()
        rlp.sidebar_orders_and_quotes()
        rlp.unselect_all()
        rlp.select_by_sku(product_1_dto["partSku"])
        rlp.select_by_sku(product_2_dto["partSku"])

        new_po_number = Tools.random_string_l(10)
        rlp.submit_replenishment_list_general_po(new_po_number)

        sa.check_po_number_by_number(shipto_1_dto["number"], new_po_number)
        sa.check_po_number_by_number(shipto_2_dto["number"], new_po_number)

    @pytest.mark.regression
    def test_create_transaction_for_noweight_locker(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1853

        ta = TransactionApi(api)
        la = LocationApi(api)
        sta = SettingsApi(api)

        response_location = setup_locker_location(api, no_weight=True)
        sta.set_checkout_software_settings_for_shipto(response_location["shipto_id"])

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_body = copy.deepcopy(response_location["location"])
        location_dto = copy.deepcopy(location_body)
        location_dto["onHandInventory"] = 1
        location_dto["orderingConfig"]["lockerWithNoWeights"] = True
        location_dto["id"] = location_id
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert len(transaction) == 1, "The number of transactions should be equal to 1"
        assert transaction[0]["reorderQuantity"] == (response_location["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_location['product']['roundBuy']*3}"
        assert transaction[0]["product"]["partSku"] == response_location["product"]["partSku"]


    @pytest.mark.smoke
    def test_smoke_label_transaction_and_activity_log(self, smoke_api):
        smoke_api.testrail_case_id = 2005
        ta = TransactionApi(smoke_api)
        ala = ActivityLogApi(smoke_api)

        activity_log_before = ala.get_activity_log()
        activity_log_records_before = activity_log_before["totalElements"]
        # close all Active transactions
        transactions = ta.get_transaction(status="ACTIVE")
        if (transactions["totalElements"] != 0):
            smoke_api.logger.info("There are some active transactions, they will be closed")
            ta.update_transactions_with_specific_status("ACTIVE", 0, "DO_NOT_REORDER")
        ta.create_active_item(smoke_api.data.shipto_id, smoke_api.data.ordering_config_id, repeat=6)
        transactions = ta.get_transaction(status="ACTIVE")
        transaction_id = transactions["entities"][0]["id"]
        assert transactions["totalElements"] != 0, "There is no ACTIVE transaction"
        ta.update_replenishment_item(transaction_id, 0, "DO_NOT_REORDER")
        activity_log_after = ala.get_activity_log()
        activity_log_records_after = activity_log_after["totalElements"]
        assert activity_log_records_before != activity_log_records_after, "There are no new records in activity log"