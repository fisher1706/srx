from src.api.mobile.mobile_cycle_count_api import MobileCycleCountApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.location_api import LocationApi
from src.api.setups.setup_location import SetupLocation
import pytest

class TestMobileCycleCountLabels():
    @pytest.mark.parametrize("conditions", [
        {
            "ohi": 35,
            "result": 35,
            "testrail_case_id": 2278,
            "excepted_code": 200
        },
        {
            "ohi": 34,
            "result": 34,
            "testrail_case_id": 2279,
            "excepted_code": 200
        },
        {
            "ohi": 0,
            "result": 0,
            "testrail_case_id": 2304,
            "excepted_code": 200
        },
        {
            "ohi": 1,
            "result": 1,
            "testrail_case_id": 2307,
            "excepted_code": 200
        },
        {
            "ohi": 76.4,
            "result": 76,
            "testrail_case_id": 2305,
            "excepted_code": 200
        },
        {
            "ohi": 79.99,
            "result": 79,
            "testrail_case_id": 2306,
            "excepted_code": 200
        },
        {
            "ohi": -55,
            "result": 0,
            "testrail_case_id": 2308,
            "excepted_code": 400
        }
    ])
    @pytest.mark.regression
    def test_update_ohi_with_qty_multiple_and_not_multiple_issueqty(self, mobile_api, conditions, delete_shipto):
        mobile_api.testrail_case_id = conditions["testrail_case_id"]
        mca = MobileCycleCountApi(mobile_api)
        la = LocationApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": False, "track_ohi" : True})
        setup_location.setup_product.add_option("package_conversion", 3)
        setup_location.setup_product.add_option("issue_quantity", 7)
        setup_location.setup_product.add_option("round_buy", 5)
        setup_location.add_option("ohi", 0)
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "OHI of location should be equal to 0"


        data =  { 
            "id": response_location["location_id"],
            "onHandInventory": conditions["ohi"]
        }

        mca.update_ohi(data, response_location["shipto_id"], response_location["location_id"], expected_status_code=conditions["excepted_code"])

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == conditions["result"], f"OHI of location should be equal to {conditions['result']}"

    @pytest.mark.regression
    def test_update_ohi_with_disabled_track_ohi_option(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2280
        mca = MobileCycleCountApi(mobile_api)
        la = LocationApi(mobile_api)
        ohi = 56

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": False, "track_ohi" : False})
        setup_location.setup_product.add_option("package_conversion", 3)
        setup_location.setup_product.add_option("issue_quantity", 7)
        setup_location.setup_product.add_option("round_buy", 5)
        setup_location.add_option("ohi", 0)
        response_location = setup_location.setup()


        data =  { 
            "id": response_location["location_id"],
            "onHandInventory": ohi
        }

        mca.update_ohi(data, response_location["shipto_id"], response_location["location_id"], expected_status_code=400)

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] is None, f"OHI of location should be null"

    @pytest.mark.parametrize("conditions", [
        {
            "ohi": 30,
            "reorder_quantity": 20,
            "testrail_case_id": 2298
        },
        {
            "ohi": 21,
            "reorder_quantity": 30,
            "testrail_case_id": 2309
        }
    ])
    @pytest.mark.regression
    def test_update_ohi_with_qty_less_or_equal_min(self, mobile_api, conditions, delete_shipto):
        mobile_api.testrail_case_id = conditions["testrail_case_id"]
        mca = MobileCycleCountApi(mobile_api)
        la = LocationApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": True, "track_ohi" : True})
        setup_location.setup_product.add_option("package_conversion", 3)
        setup_location.setup_product.add_option("issue_quantity", 7)
        setup_location.setup_product.add_option("round_buy", 10)
        setup_location.add_option("ohi", 0)
        response_location = setup_location.setup()


        data =  { 
            "id": response_location["location_id"],
            "onHandInventory": conditions["ohi"]
        }

        mca.update_ohi(data, response_location["shipto_id"], response_location["location_id"])

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == conditions["ohi"], f"OHI of location should be {conditions['ohi']}"

        transactions_active = ta.get_transaction(shipto_id=response_location["shipto_id"],status="ACTIVE")["entities"]
        
        assert len(transactions_active) == 1 and transactions_active[0]["reorderQuantity"] == conditions["reorder_quantity"], f"Transactions quantity in Active status should be 1 and reorder quantity should be{conditions['reorder_quantity']}"
