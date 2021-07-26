import pytest
from src.resources.tools import Tools
from src.api.import_api import ImportApi
from src.api.admin.distributor_settings_api import DistributorSettingsApi
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.location_api import LocationApi
from src.api.setups.setup_location import SetupLocation

@pytest.mark.regression
def test_location_created_with_frozen_status(api, delete_shipto):
    api.testrail_case_id = 2349

    la = LocationApi(api)

    response_location = SetupLocation(api).setup()

    location = la.get_locations(shipto_id=response_location["shipto_id"])

    assert len(location) == 1
    assert location[0]["inventoryStatus"] == "FROZEN"

@pytest.mark.parametrize("conditions", [
    {
        "months": -5,
        "testrail_case_id": 2350,
        "status": "FROZEN"
    },
    {
        "months": -3,
        "testrail_case_id": 2351,
        "status": "SLOW"
    },
    {
        "months": -1,
        "testrail_case_id": 2352,
        "status": "SLOW"
    }
    ])
@pytest.mark.regression
def test_inventory_status_with_1_usage_history_record(api, conditions, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    dsa = DistributorSettingsApi(api)
    sa = SettingsApi(api)
    ia = ImportApi(api)
    la = LocationApi(api)
    response_location = SetupLocation(api).setup()

    dsa.set_freeze_settings(slow=2, frozen=4)
    usage_history_body = {
        "Order Number": Tools.random_string_l(),
        "ShipTo Number": response_location["shipto"]["number"],
        "Distributor SKU": response_location["product"]["partSku"],
        "Quantity": response_location["product"]["roundBuy"],
        "Date": Tools.ymd_dateformat(conditions["months"])
    }
    usage_history = [
        [usage_history_body["Order Number"], None, usage_history_body["ShipTo Number"], None, usage_history_body["Distributor SKU"], usage_history_body["Quantity"], usage_history_body["Date"]]
    ]
    
    ia.full_import_usage_history(usage_history)
    sa.save_and_adjust_moving_status(True, response_location["shipto_id"], sleep=5)
    location = la.get_locations(shipto_id=response_location["shipto_id"])

    assert len(location) == 1
    assert location[0]["inventoryStatus"] == conditions["status"]

@pytest.mark.parametrize("conditions", [
    {
        "months_1": -1,
        "months_2": -5,
        "testrail_case_id": 2457,
        "status": "SLOW"
    },
    {
        "months_1": -1,
        "months_2": -3,
        "testrail_case_id": 2460,
        "status": "MOVING"
    },
    {
        "months_1": -3,
        "months_2": -3,
        "testrail_case_id": 2461,
        "status": "SLOW"
    }
    ])
@pytest.mark.regression
def test_inventory_status_with_2_usage_history_records(api, conditions, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    dsa = DistributorSettingsApi(api)
    sa = SettingsApi(api)
    ia = ImportApi(api)
    la = LocationApi(api)
    response_location = SetupLocation(api).setup()

    dsa.set_freeze_settings(slow=2, frozen=4)
    usage_history_body = {
        "Order Number": Tools.random_string_l(),
        "ShipTo Number": response_location["shipto"]["number"],
        "Distributor SKU": response_location["product"]["partSku"],
        "Quantity": response_location["product"]["roundBuy"],
        "Date1": Tools.ymd_dateformat(conditions["months_1"]),
        "Date2": Tools.ymd_dateformat(conditions["months_2"])
    }
    usage_history = [
        [usage_history_body["Order Number"], None, usage_history_body["ShipTo Number"], None, usage_history_body["Distributor SKU"], usage_history_body["Quantity"], usage_history_body["Date1"]],
        [usage_history_body["Order Number"], None, usage_history_body["ShipTo Number"], None, usage_history_body["Distributor SKU"], usage_history_body["Quantity"], usage_history_body["Date2"]]
    ]
    
    ia.full_import_usage_history(usage_history)
    sa.save_and_adjust_moving_status(True, response_location["shipto_id"], sleep=10)
    location = la.get_locations(shipto_id=response_location["shipto_id"])

    assert len(location) == 1
    assert location[0]["inventoryStatus"] == conditions["status"]