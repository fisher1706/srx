import pytest
import copy
import time
from src.resources.locator import Locator
from src.resources.tools import Tools
from src.resources.permissions import Permissions
from src.pages.general.login_page import LoginPage
from src.pages.distributor.order_status_page import OrderStatusPage
from src.pages.customer.reorder_list_page import ReorderListPage
from src.api.setups.setup_location import SetupLocation
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

        response_location_1 = SetupLocation(ui).setup()
        response_location_2 = SetupLocation(ui).setup()

        product_1_dto = response_location_1["product"]
        product_2_dto = response_location_2["product"]
        shipto_1_dto = response_location_1["shipto"]
        shipto_2_dto = response_location_2["shipto"]
        new_shipto_1 = response_location_1["shipto_id"]
        new_shipto_2 = response_location_2["shipto_id"]
        
        sta.set_reorder_controls_settings_for_shipto(new_shipto_1)
        sta.set_reorder_controls_settings_for_shipto(new_shipto_2)

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

        response_location_1 = SetupLocation(ui).setup()
        response_location_2 = SetupLocation(ui).setup()

        product_1_dto = response_location_1["product"]
        product_2_dto = response_location_2["product"]
        shipto_1_dto = response_location_1["shipto"]
        shipto_2_dto = response_location_2["shipto"]
        new_shipto_1 = response_location_1["shipto_id"]
        new_shipto_2 = response_location_2["shipto_id"]
        
        sta.set_reorder_controls_settings_for_shipto(new_shipto_1)
        sta.set_reorder_controls_settings_for_shipto(new_shipto_2)

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

        setup_location = SetupLocation(api)
        setup_location.add_option("locker_location")
        setup_location.setup_locker.add_option("no_weight")
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        response_location = setup_location.setup()

        location_body = copy.deepcopy(response_location["location"])
        location_dto = copy.deepcopy(location_body)
        location_dto["onHandInventory"] = 1
        location_dto["orderingConfig"]["lockerWithNoWeights"] = True
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert len(transaction) == 1, "The number of transactions should be equal to 1"
        assert transaction[0]["reorderQuantity"] == (response_location["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_location['product']['roundBuy']*3}"
        assert transaction[0]["product"]["partSku"] == response_location["product"]["partSku"]

    @pytest.mark.smoke_integration_logix
    def test_integration_submit_transaction_to_quote(self, smoke_api):
        smoke_api.testrail_case_id = 2281
        ta = TransactionApi(smoke_api)

        transactions = ta.get_transaction(status="ACTIVE")
        if (transactions["totalElements"] != 0):
            smoke_api.logger.info("There are some active transactions, they will be closed")
            ta.update_transactions_with_specific_status("ACTIVE", 0, "DO_NOT_REORDER")
        
        transactions = ta.get_transaction(status="QUOTED")
        if (transactions["totalElements"] != 0):
            smoke_api.logger.info("There are some quoted transactions, they will be closed")
            ta.update_transactions_with_specific_status("QUOTED", 0, "DO_NOT_REORDER")

        transactions = ta.get_transaction(status="ORDERED")
        if (transactions["totalElements"] != 0):
            smoke_api.logger.info("There are some ordered transactions, they will be closed")
            ta.update_transactions_with_specific_status("ORDERED", 0, "DO_NOT_REORDER")

        ta.create_active_item(smoke_api.data.shipto_id, smoke_api.data.ordering_config_id, repeat=6)
        transactions = ta.get_transaction(status="ACTIVE")
        transaction_id = transactions["entities"][0]["id"]
        assert transactions["totalElements"] != 0, "There is no ACTIVE transaction"
        
        post_data = {
            "poNumber": {
                "poNumber": "TEST DO NOT PROCESS",
                "useForAllShipTo": True,
                "distributors": [
                    {
                        "name": "SMOKE INTEGRATION LOGIX DISTRIBUTOR",
                        "total": "N/A",
                        "logo": None,
                        "shipTos": [
                            {
                                "id": smoke_api.data.shipto_id,
                                "number": "ShipTo",
                                "name": None,
                                "address": {
                                    "line1": "address",
                                    "line2": None,
                                    "city": "CN",
                                    "state": "AL",
                                    "zipCode": "00000"
                                },
                                "poNumber": "TEST DO NOT PROCESS",
                                "total": "N/A",
                                "submitType": "QUOTED",
                                "existQuotedItem": True
                            }
                        ]
                    }
                ]
            },
            "items": [
                {
                    "id": transaction_id,
                    "reorderQuantity": 100,
                    "status": "QUOTED"
                }
            ]
        }
        ta.submit_transaction(post_data)
        transactions = ta.get_transaction(status="QUOTED")
        assert transactions["totalElements"] == 1

        ta.update_replenishment_item(transaction_id, 0, "DO_NOT_REORDER")
        
        transactions = ta.get_transaction(status="QUOTED")
        assert transactions["totalElements"] == 0

    @pytest.mark.smoke
    def test_smoke_label_transaction_and_activity_log(self, smoke_api):
        smoke_api.testrail_case_id = 2005

        ta = TransactionApi(smoke_api)
        ala = ActivityLogApi(smoke_api)
        la = LocationApi(smoke_api)

        activity_log_before = ala.get_activity_log()
        last_activity_log_id_before = activity_log_before["entities"][0]["id"]
        location = la.get_locations(smoke_api.data.shipto_id)[0]
        location["onHandInventory"] = 50
        location_list = [copy.deepcopy(location)]
        la.update_location(location_list, smoke_api.data.shipto_id)
        # close all Active transactions
        transactions = ta.get_transaction(status="ACTIVE")
        if transactions["totalElements"] != 0:
            smoke_api.logger.info("There are some active transactions, they will be closed")
            ta.update_transactions_with_specific_status("ACTIVE", 0, "DO_NOT_REORDER")
        transactions = ta.get_transaction(status="ACTIVE")
        assert transactions["totalElements"] == 0
        location["onHandInventory"] = 0
        location_list = [copy.deepcopy(location)]
        la.update_location(location_list, smoke_api.data.shipto_id)
        for i in range(6):
            transactions = ta.get_transaction(status="ACTIVE")
            transactions_qty = transactions["totalElements"]
            if transactions_qty == 0:
                time.sleep(5)
                continue
            elif transactions_qty == 1:
                break
            else:
                smoke_api.logger.error(f"Incorrect QTY of transactions: '{transactions_qty}'")
        else:
            smoke_api.logger.error(f"New transaction has not been created")

        transaction_id = transactions["entities"][0]["id"]
        assert transactions["totalElements"] != 0, "There is no ACTIVE transaction"
        ta.update_replenishment_item(transaction_id, 0, "DO_NOT_REORDER")
        for i in range(3):
            time.sleep(10)
            activity_log_after = ala.get_activity_log()
            last_activity_log_id_after = activity_log_after["entities"][0]["id"]
            if last_activity_log_id_after <= last_activity_log_id_before:
                continue
            else:
                break
        assert last_activity_log_id_before < last_activity_log_id_after, "There are no new records in activity log"

    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": 2299
        },
        { 
            "user": Permissions.orders("EDIT"),
            "testrail_case_id": 2300
        }
        ])
    @pytest.mark.acl
    @pytest.mark.regression
    def test_transaction_crud_and_split(self, ui, permission_ui, permissions, delete_distributor_security_group, delete_shipto):
        ui.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

        ta = TransactionApi(context)
        la = LocationApi(ui)

        lp = LoginPage(context)
        osp = OrderStatusPage(context)

        setup_location = SetupLocation(ui)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        response_location = setup_location.setup()

        distributor_sku = response_location["product"]["partSku"]
        round_buy = response_location["product"]["roundBuy"]

        TransactionApi(ui).create_active_item(response_location["shipto_id"], la.get_ordering_config_by_sku(response_location["shipto_id"], distributor_sku))
        lp.log_in_distributor_portal()
        osp.sidebar_order_status()
        osp.wait_until_page_loaded()
        new_transaction_row = osp.scan_table(distributor_sku, "Distributor SKU")
        quantity = osp.get_table_item_text_by_header("Quantity", new_transaction_row)
        assert osp.get_table_item_text_by_header("Status", new_transaction_row) == "ACTIVE"
        new_quantity = int(quantity) + int(round_buy)
        osp.update_transaction(new_transaction_row, quantity=new_quantity, status="SHIPPED")

        assert osp.get_table_item_text_by_header("Status", new_transaction_row) == "SHIPPED"
        assert osp.get_table_item_text_by_header("Quantity", new_transaction_row) == str(new_quantity)

        osp.split_transaction(new_transaction_row, round_buy)

        transactions = ta.get_transaction(sku=distributor_sku)
        assert transactions["totalElements"] == 2

        if str(transactions["entities"][0]["reorderQuantity"]) == str(round_buy):
            assert str(transactions["entities"][1]["reorderQuantity"]) == str(quantity)
        elif str(transactions["entities"][0]["reorderQuantity"]) == str(quantity):
            assert str(transactions["entities"][1]["reorderQuantity"]) == str(round_buy)
        else:
            ui.logger.error(f"Incorrect quantity of transactions: '{transactions['entities'][0]['reorderQuantity']}' and {transactions['entities'][1]['reorderQuantity']}, when RoundBuy = '{round_buy}'")
   
    @pytest.mark.regression
    def test_zero_quantity_of_new_transaction(self, api, ui, delete_shipto):
        ui.testrail_case_id = 1841
        ta = TransactionApi(ui)
        la = LocationApi(api)
        lp = LoginPage(ui)
        osp = OrderStatusPage(ui)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.add_option("transaction",'ACTIVE')
        response_location = setup_location.setup()

        lp.log_in_distributor_portal()
        osp.sidebar_order_status()
        osp.wait_until_page_loaded()

        distributor_sku = response_location["product"]["partSku"]
        quantity = response_location["product"]["issueQuantity"]
        round_buy = response_location["product"]["roundBuy"]
  
        new_transaction_row = osp.scan_table(distributor_sku, "Distributor SKU")
        osp.update_transaction(new_transaction_row, quantity=quantity, status="QUOTED")

        TransactionApi(ui).create_active_item(response_location["shipto_id"], la.get_ordering_config_by_sku(response_location["shipto_id"], distributor_sku))
        second_transaction = ta.get_transaction(distributor_sku, shipto_id = response_location["shipto_id"], status="ACTIVE")["entities"]
        assert second_transaction[0]["reorderQuantity"] == 0

        quantity = osp.get_table_item_text_by_header("Quantity", new_transaction_row)
        new_quantity = int(quantity) + int(round_buy)

        osp.page_refresh()
        osp.wait_until_page_loaded()
        transaction_first_row = osp.scan_table("QUOTED", "Status")
        osp.update_transaction(transaction_first_row, status="ORDERED")
        second_transaction_row = new_transaction_row+1       
        osp.update_transaction(second_transaction_row, quantity=new_quantity,status="DELIVERED")
        TransactionApi(ui).create_active_item(response_location["shipto_id"], la.get_ordering_config_by_sku(response_location["shipto_id"], distributor_sku))
        third_transaction = ta.get_transaction(distributor_sku,status="ACTIVE")["entities"]
        assert third_transaction[0]["reorderQuantity"] == 0

        osp.page_refresh()
        osp.wait_until_page_loaded()
        transaction_first_row = osp.scan_table("ORDERED", "Status")
        osp.update_transaction(transaction_first_row, status="SHIPPED")
        third_transaction_row = new_transaction_row+1       
        osp.update_transaction(third_transaction_row, quantity=new_quantity,status="DELIVERED")
        TransactionApi(ui).create_active_item(response_location["shipto_id"], la.get_ordering_config_by_sku(response_location["shipto_id"], distributor_sku))
        fourth_transaction = ta.get_transaction(distributor_sku,status="ACTIVE")["entities"]
        assert fourth_transaction[0]["reorderQuantity"] == 0