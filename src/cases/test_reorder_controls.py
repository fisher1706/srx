import pytest
import copy
from src.resources.locator import Locator
from src.resources.tools import Tools
from src.pages.distributor.order_status_page import OrderStatusPage
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.location_api import LocationApi

class TestReorderControls():
    @pytest.mark.parametrize("conditions", [
        {
            "coefficient": 0,
            "transaction_qty": 1,
            "reorder_qty_coefficient": 3,
            "testrail_case_id": 2581
        },
        { 
            "coefficient": 1,
            "transaction_qty": 1,
            "reorder_qty_coefficient": 2,
            "testrail_case_id": 2582
        },
        {
            "coefficient": 2,
            "transaction_qty": 0,
            "reorder_qty_coefficient": 0,
            "testrail_case_id": 2583
        }
        ])
    @pytest.mark.regression
    def test_create_transaction_at_min(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        #update OHi to Max
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        #update OHI
        location_dto["onHandInventory"] = response_location["product"]["roundBuy"]*conditions["coefficient"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert len(transaction) == conditions["transaction_qty"], f"The number of transactions should be equal to {conditions['transaction_qty']}"
        if conditions["transaction_qty"] != 0:
            assert transaction[0]["reorderQuantity"] == (response_location["product"]["roundBuy"]*conditions["reorder_qty_coefficient"]), f"Reorder quantity of transaction should be equal to {response_location['product']['roundBuy']*conditions['reorder_qty_coefficient']}"
            assert transaction[0]["product"]["partSku"] == response_location["product"]["partSku"]

    @pytest.mark.parametrize("conditions_issued", [
        {
            "coefficient": 2,
            "transaction_qty": 0,
            "reorder_qty_coefficient": 0,
            "testrail_case_id": 3198
        },
        {
            "coefficient": 0.5,
            "transaction_qty": 1,
            "reorder_qty_coefficient": 2,
            "testrail_case_id": 3197
        }
        ])
    @pytest.mark.regression
    def test_create_transaction_as_issued(self, api, conditions_issued, delete_shipto):
        api.testrail_case_id = conditions_issued["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls": "ISSUED"})
        response_location = setup_location.setup()

        #update OHi
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]*conditions_issued["coefficient"]
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert len(transaction) == conditions_issued["transaction_qty"], f"The number of transactions should be equal to {conditions_issued['transaction_qty']}"
        if conditions_issued["transaction_qty"] != 0:
            assert transaction[0]["reorderQuantity"] == (response_location["product"]["roundBuy"]*conditions_issued["reorder_qty_coefficient"]), f"Reorder quantity of transaction should be equal to {response_location['product']['roundBuy']*conditions_issued['reorder_qty_coefficient']}"
            assert transaction[0]["product"]["partSku"] == response_location["product"]["partSku"]
             
    @pytest.mark.parametrize("conditions_close", [
        {
            "coefficient": 0,
            "close_transaction_cofficient":2, # MAX > OHI > MIN
            "transaction_qty": 1,
            "close_transaction_qty": 0,
            "reorder_controls": "MIN",
            "testrail_case_id": 3199
        },
        {
            "coefficient": 0.5,
            "close_transaction_cofficient":4,
            "transaction_qty": 1,
            "close_transaction_qty": 0,
            "reorder_controls": "ISSUED",
            "testrail_case_id": 3200
        }
        ])
    @pytest.mark.regression
    def test_close_transaction(self, api, conditions_close, delete_shipto):
        api.testrail_case_id = conditions_close["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_close['reorder_controls']})
        response_location = setup_location.setup()

        #transaction create 
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]*conditions_close["coefficient"]
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction[0]["status"] == "ACTIVE"
        #close transaction
        location_dto["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]*conditions_close["close_transaction_cofficient"]
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction[0]["status"] == "DO_NOT_REORDER"

    @pytest.mark.regression
    def test_update_reorder_quantity_at_min(self, api, delete_shipto):
        api.testrail_case_id = 3201

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls":'MIN'})
        response_location = setup_location.setup()

        #transaction create 
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity_old = transaction[0]["reorderQuantity"]
        #change OHI
        location_dto["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]*0
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction_updated= ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["reorderQuantity"] == quantity_old + (response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"] - location_dto["onHandInventory"])
       
    @pytest.mark.regression
    def test_update_reorder_quantity_as_issued(self, api, delete_shipto):
        api.testrail_case_id = 3202

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls":'ISSUED'})
        response_location = setup_location.setup()

        #transaction create 
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]*0.5
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity_old = transaction[0]["reorderQuantity"]
        #change OHI
        location_dto["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]-1
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction_updated= ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["reorderQuantity"] == quantity_old/2
