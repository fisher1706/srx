import random
import pytest
from src.api.mobile.mobile_rfid_api import MobileRfidApi
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.location_api import LocationApi
from src.api.setups.setup_location import SetupLocation
from src.resources.permissions import Permissions

@pytest.mark.parametrize("conditions", [
    {
        "testrail_case_id": 7598,
        "state": "CHECK_IN",
        "expected_code": 200,
        "state_after_putaway": "AVAILABLE",
        "returned" : False,
        "round_buy": 1,
        "expected_ohi": 1
    },
    {
        "testrail_case_id": 7599,
        "state": "RETURN_CHECK_IN",
        "expected_code": 200,
        "state_after_putaway": "AVAILABLE",
        "returned": True,
        "round_buy": 8,
        "expected_ohi": 8
    },
    {
        "testrail_case_id": 7600,
        "state": "ISSUED",
        "expected_code": 400,
        "state_after_putaway": "ISSUED",
        "returned": False,
        "round_buy": 11,
        "expected_ohi": 0
    },
    {
        "testrail_case_id": 7601,
        "state": "ASSIGNED",
        "expected_code": 400,
        "state_after_putaway": "ASSIGNED",
        "returned": False,
        "round_buy": 4,
        "expected_ohi": 0
    },
    {
        "testrail_case_id": 7602,
        "state": "MANIFEST",
        "expected_code": 400,
        "state_after_putaway": "MANIFEST",
        "returned": False,
        "round_buy": 10,
        "expected_ohi": 0
    },
    {
        "testrail_case_id": 7603,
        "state": "RETURN_MANIFEST",
        "expected_code": 400,
        "state_after_putaway": "RETURN_MANIFEST",
        "returned": False,
        "round_buy": 15,
        "expected_ohi": 0
    },
    {
        "testrail_case_id": 7604,
        "state": "AVAILABLE",
        "expected_code": 400,
        "state_after_putaway": "AVAILABLE",
        "returned": False,
        "round_buy": 14,
        "expected_ohi": 14
    }
])
@pytest.mark.regression
def test_rfid_putaway_with_permission(mobile_api, conditions, delete_shipto):
    mobile_api.testrail_case_id = conditions["testrail_case_id"]
    mra = MobileRfidApi(mobile_api)
    ra = RfidApi(mobile_api)
    la =LocationApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": False})
    setup_location.add_option("type", "RFID")
    setup_location.setup_product.add_option("round_buy", conditions["round_buy"])
    setup_location.add_option("ohi", 0)
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfid_labels[0]["id"], conditions["state"])
    updated_rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    mra.rfid_put_away(response_location["shipto_id"], updated_rfid_labels[0]["id"], expected_status_code = conditions["expected_code"])

    rfid_labels_after_putaway = mra.get_rfids_labels_by_location(response_location["location_id"])
    assert rfid_labels_after_putaway[0]["state"] == conditions["state_after_putaway"], f"Status of RFID Tag should be {conditions['state_after_putaway']}"
    assert rfid_labels_after_putaway[0]["returned"] == conditions["returned"], f"Returned field should be marked as {conditions['returned']}"

    locations = la.get_locations(response_location["shipto_id"], mobile=True)
    assert locations[0]["onHandInventory"] == conditions["expected_ohi"], f"OHI should be equal {conditions['expected_ohi']}"


@pytest.mark.regression
def test_rfid_putaway_without_permission(mobile_api, permission_api, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = 7605
    Permissions.set_configured_user(mobile_api, Permissions.mobile_rfid_putaway("ENABLE", False))
    mra = MobileRfidApi(permission_api)
    super_mra = MobileRfidApi(mobile_api)
    ra = RfidApi(mobile_api)
    la =LocationApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": False})
    setup_location.add_option("type", "RFID")
    setup_location.add_option("ohi", 0)
    response_location = setup_location.setup()

    super_mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfid_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfid_labels[0]["id"], "CHECK_IN")
    updated_rfid_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    mra.rfid_put_away(response_location["shipto_id"], updated_rfid_labels[0]["id"], expected_status_code=400)

    rfid_labels_after_putaway = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    assert rfid_labels_after_putaway[0]["state"] == "CHECK_IN", "Status of RFID Tag should be CHECK_IN"

    locations = la.get_locations(response_location["shipto_id"], mobile=True)
    assert locations[0]["onHandInventory"] == 0, "OHI of location should be equal to 0"

@pytest.mark.regression
def test_putaway_non_existent_label(mobile_api, delete_shipto):
    mobile_api.testrail_case_id = 7609
    mra = MobileRfidApi(mobile_api)
    ra = RfidApi(mobile_api)
    la = LocationApi(mobile_api)
    non_existing_tag_id = random.randint(9000000, 18000000)

    setup_location = SetupLocation(mobile_api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": False})
    setup_location.add_option("type", "RFID")
    setup_location.add_option("ohi", 0)
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfid_labels[0]["id"], "RETURN_CHECK_IN")

    mra.rfid_put_away(response_location["shipto_id"], non_existing_tag_id, expected_status_code=404)

    rfid_labels_after_putaway = mra.get_rfids_labels_by_location(response_location["location_id"])
    assert rfid_labels_after_putaway[0]["state"] == "RETURN_CHECK_IN", "Status of RFID Tag should be RETURN_CHECK_IN"

    locations = la.get_locations(response_location["shipto_id"], mobile=True)
    assert locations[0]["onHandInventory"] == 0, "OHI of location should be equal to 0"
