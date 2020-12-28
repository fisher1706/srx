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

