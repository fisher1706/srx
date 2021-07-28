from src.api.mobile.mobile_rfid_api import MobileRfidApi
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.setups.setup_location import SetupLocation
from src.resources.permissions import Permissions
import pytest


@pytest.mark.regression
def test_create_label_for_rfid_with_permission(mobile_api, delete_shipto):
    mobile_api.testrail_case_id = 4094
    mra = MobileRfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])

    rfids_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    assert len(rfids_labels) == 1, "There should be 1 RFID label"
    assert rfids_labels[0]["state"] == "ASSIGNED", "RFID label's state should be ASSIGNED"


@pytest.mark.acl
@pytest.mark.regression
def test_create_label_for_rfid_without_permission(mobile_api, permission_api, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = 6306
    Permissions.set_configured_user(mobile_api, Permissions.mobile_rfid_manage("ENABLE", False))
    mra = MobileRfidApi(permission_api)
    super_mra = MobileRfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"], expected_status_code=400)

    rfids_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    assert len(rfids_labels) == 0, "RFID label should not be created without permission"


@pytest.mark.parametrize("conditions", [
    {
        "testrail_case_id": 6307,
        "state": "ASSIGNED",
        "result_state": "ASSIGNED",
        "expected_code": 200,
        "rfid_labels_expected_qty": 0
    },
    {
        "testrail_case_id": 6309,
        "state": "MANIFEST",
        "result_state": "MANIFEST",
        "expected_code": 200,
        "rfid_labels_expected_qty": 0
    },
    {
        "testrail_case_id": 6310,
        "state": "RETURN_MANIFEST",
        "result_state": "RETURN_MANIFEST",
        "expected_code": 200,
        "rfid_labels_expected_qty": 0
    },
    {
        "testrail_case_id": 6311,
        "state": "CHECK_IN",
        "result_state": "CHECK_IN",
        "expected_code": 200,
        "rfid_labels_expected_qty": 0
    },
    {
        "testrail_case_id": 6312,
        "state": "RETURN_CHECK_IN",
        "result_state": "RETURN_CHECK_IN",
        "expected_code": 200,
        "rfid_labels_expected_qty": 0
    },
    {
        "testrail_case_id": 6308,
        "state": "ISSUED",
        "result_state": "ISSUED",
        "expected_code": 400,
        "rfid_labels_expected_qty": 1
    }
])
@pytest.mark.regression
def test_delete_label_for_rfid_with_permission(mobile_api, conditions, delete_shipto):
    mobile_api.testrail_case_id = conditions["testrail_case_id"]
    mra = MobileRfidApi(mobile_api)
    ra = RfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])

    rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfid_labels[0]["id"], conditions["state"])
    updated_rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    assert updated_rfid_labels[0]["state"] == conditions["result_state"], f"RFID label's state should be {conditions['result_state']}"

    mra.delete_rfid_label(response_location["location_id"], updated_rfid_labels[0]["labelId"], expected_status_code=conditions["expected_code"])

    updated_rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    assert len(updated_rfid_labels) == conditions["rfid_labels_expected_qty"], f"There should be {conditions['rfid_labels_expected_qty']} RFID label(s)"


@pytest.mark.acl
@pytest.mark.regression
def test_delete_label_for_rfid_without_permission(mobile_api, permission_api, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = 6314
    Permissions.set_configured_user(mobile_api, Permissions.mobile_rfid_manage("ENABLE", False))
    mra = MobileRfidApi(permission_api)
    super_mra = MobileRfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    super_mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])

    rfid_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    assert len(rfid_labels) == 1, "There should be 1 RFID label"

    mra.delete_rfid_label(response_location["location_id"], rfid_labels[0]["labelId"], expected_status_code=400)

    updated_rfid_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    assert len(updated_rfid_labels) == 1, "There should be 1 RFID label"
    assert updated_rfid_labels[0]["labelId"] == rfid_labels[0]["labelId"], "RFID label should stay without changes after unassign without permission"


@pytest.mark.regression
def test_delete_available_label_for_rfid_without_reoreder(mobile_api, delete_shipto):
    mobile_api.testrail_case_id = 6313
    mra = MobileRfidApi(mobile_api)
    ra = RfidApi(mobile_api)
    la = LocationApi(mobile_api)
    ta = TransactionApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": False})
    setup_location.add_option("type", "RFID")
    setup_location.setup_product.add_option("round_buy", 1)
    setup_location.add_option("ohi", 0)
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfid_labels[0]["id"], "AVAILABLE")

    locations = la.get_locations(response_location["shipto_id"], mobile=True)
    assert locations[0]["onHandInventory"] == 1, "OHI of location should be equal to 1"

    active_transactions = ta.get_transaction(shipto_id=response_location["shipto_id"], status="ACTIVE")["entities"]
    assert len(active_transactions) == 0, "Active transactions should not been created"

    mra.delete_rfid_label(response_location["location_id"], rfid_labels[0]["labelId"])
    updated_rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    assert len(updated_rfid_labels) == 0, "There should be 0 RFID labels"

    updated_locations = la.get_locations(response_location["shipto_id"], mobile=True)
    assert updated_locations[0]["onHandInventory"] == 0, "OHI of location should be equal to 0"

    updated_active_transactions = ta.get_transaction(shipto_id=response_location["shipto_id"], status="ACTIVE")["entities"]
    assert len(updated_active_transactions) == 0, "Active transactions should not been created"


@pytest.mark.parametrize("conditions", [
    {
        "round_buy": 1,
        "ohi_after_assign_available": 1,
        "ohi_after_unassign_available": 0,
        "reorder_qty_after_assign_available": 2,
        "reorder_qty_after_unassign_available": 3
    },
    {
        "round_buy": 10,
        "ohi_after_assign_available": 10,
        "ohi_after_unassign_available": 0,
        "reorder_qty_after_assign_available": 20,
        "reorder_qty_after_unassign_available": 30
    },
    {
        "round_buy": 6,
        "ohi_after_assign_available": 6,
        "ohi_after_unassign_available": 0,
        "reorder_qty_after_assign_available": 12,
        "reorder_qty_after_unassign_available": 18
    }
])
@pytest.mark.regression
def test_delete_available_label_for_rfid_with_reoreder(mobile_api, conditions, delete_shipto):
    mobile_api.testrail_case_id = 7004
    mra = MobileRfidApi(mobile_api)
    ra = RfidApi(mobile_api)
    la = LocationApi(mobile_api)
    ta = TransactionApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True})
    setup_location.add_option("type", "RFID")
    setup_location.setup_product.add_option("round_buy", conditions["round_buy"])
    setup_location.add_option("ohi", 0)
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfid_labels[0]["id"], "AVAILABLE")

    locations = la.get_locations(response_location["shipto_id"], mobile=True)
    assert locations[0]["onHandInventory"] == conditions["ohi_after_assign_available"], f"OHI of location should be equal to {conditions['ohi_after_assign_available']}"

    active_transactions = ta.get_transaction(shipto_id=response_location["shipto_id"], status="ACTIVE")["entities"]
    assert len(active_transactions) == 1, "Active transaction should be created by Reorder Controls option"
    assert active_transactions[0]["reorderQuantity"] == conditions["reorder_qty_after_assign_available"], f"Reorder quantity should be equal {conditions['reorder_qty_after_assign_available']}"

    mra.delete_rfid_label(response_location["location_id"], rfid_labels[0]["labelId"])
    updated_rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    assert len(updated_rfid_labels) == 0, "There should be 0 RFID labels"

    updated_locations = la.get_locations(response_location["shipto_id"], mobile=True)
    assert updated_locations[0]["onHandInventory"] == conditions["ohi_after_unassign_available"], f"OHI of location should be equal to {conditions['ohi_after_unassign_available']}"

    updated_active_transactions = ta.get_transaction(shipto_id=response_location["shipto_id"], status="ACTIVE")["entities"]
    assert len(updated_active_transactions) == 1, "Active transactions should not been created"
    assert updated_active_transactions[0]["reorderQuantity"] == conditions["reorder_qty_after_unassign_available"], f"Reorder quantity should be equal {conditions['reorder_qty_after_unassign_available']}"


@pytest.mark.regression
def test_create_existing_label_for_rfid(mobile_api, delete_shipto):
    mobile_api.testrail_case_id = 7005
    mra = MobileRfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfids_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"], expected_status_code=400, label=rfids_labels[0]["labelId"])

    updated_rfids_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    assert len(updated_rfids_labels) == 1, "There should be 1 RFID label"


@pytest.mark.regression
def test_delete_non_existent_label_for_rfid(mobile_api, delete_shipto):
    mobile_api.testrail_case_id = 7006
    mra = MobileRfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])

    mra.delete_rfid_label(response_location["location_id"], "NON-EXISTING RFID TAG", expected_status_code=404)

    rfid_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    assert len(rfid_labels) == 1, "There should be 1 RFID label"
