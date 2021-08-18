import random
import pytest
from src.api.mobile.mobile_rfid_api import MobileRfidApi
from src.api.distributor.rfid_api import RfidApi
from src.api.setups.setup_location import SetupLocation
from src.resources.permissions import Permissions

@pytest.mark.parametrize("conditions", [
    {
        "testrail_case_id": 8105,
        "state": "ISSUED",
        "manifest_type": "RETURN",
        "expected_manifest_type": "RETURN",
        "state_after_submit": "RETURN_MANIFEST",
    },
    {
        "testrail_case_id": 8106,
        "state": "ASSIGNED",
        "manifest_type": "DELIVERY",
        "expected_manifest_type": "DELIVERY",
        "state_after_submit": "MANIFEST",
    }
])
@pytest.mark.regression
def test_manifest_full_positive_flow(mobile_api, conditions, delete_shipto):
    mobile_api.testrail_case_id = conditions["testrail_case_id"]
    mra = MobileRfidApi(mobile_api)
    ra = RfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfids_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfids_labels[0]["id"], conditions["state"])
    updated_rfids_labels = mra.get_rfids_labels_by_location(response_location["location_id"])

    initial_manifest = mra.create_manifest(conditions["manifest_type"])
    assert initial_manifest["data"]["type"] == conditions["expected_manifest_type"], f"Manisfest type should be {conditions['expected_manifest_type']}"

    mra.add_to_manifest(updated_rfids_labels[0]["labelId"], initial_manifest["data"]["id"], response_location["shipto_id"])
    manifest = mra.get_manifest(initial_manifest["device_id"])
    assert len(manifest["items"]) == 1, "Only 1 item has been added to manifest"
    assert manifest["items"][0]["rfidLabel"]["labelId"] == updated_rfids_labels[0]["labelId"], f"RFID tag should be equal {updated_rfids_labels[0]['labelId']}"
    assert manifest["items"][0]["rfidLabel"]["state"] == updated_rfids_labels[0]["state"], f"RFID tag should be in status {conditions['state']}"
    
    mra.submit_manifest(initial_manifest["data"]["id"])
    submitted_manifest = mra.get_manifest(initial_manifest["device_id"])
    assert submitted_manifest["items"][0]["rfidLabel"]["labelId"] == updated_rfids_labels[0]["labelId"], f"RFID tag should be equal {updated_rfids_labels[0]['labelId']}"
    assert submitted_manifest["items"][0]["rfidLabel"]["state"] == conditions["state_after_submit"], f"RFID tag should be in status {conditions['state_after_submit']}"

    mra.delete_rfid_label_from_manifest(initial_manifest["data"]["id"], submitted_manifest["items"][0]["id"])
    manifest_after_deleted_item = mra.get_manifest(initial_manifest["device_id"])
    assert len(manifest_after_deleted_item["items"]) == 0, f"In Manifest with ID = {initial_manifest['data']['id']} should not be any items"

    mra.close_manifest(initial_manifest["data"]["id"])

@pytest.mark.parametrize("conditions", [
    {
        "testrail_case_id": 8107,
        "state": "CHECK_IN",
        "manifest_type": "RETURN"
    },
    {
        "testrail_case_id": 8108,
        "state": "RETURN_CHECK_IN",
        "manifest_type": "RETURN"
    },
    {
        "testrail_case_id": 8109,
        "state": "MANIFEST",
        "manifest_type": "RETURN"
    },
    {
        "testrail_case_id": 8110,
        "state": "RETURN_MANIFEST",
        "manifest_type": "RETURN"
    },
    {
        "testrail_case_id": 8111,
        "state": "ASSIGNED",
        "manifest_type": "RETURN"
    },
    {
        "testrail_case_id": 8112,
        "state": "AVAILABLE",
        "manifest_type": "RETURN"
    },
    {
        "testrail_case_id": 8113,
        "state": "CHECK_IN",
        "manifest_type": "DELIVERY"
    },
    {
        "testrail_case_id": 8114,
        "state": "RETURN_CHECK_IN",
        "manifest_type": "DELIVERY"
    },
    {
        "testrail_case_id": 8115,
        "state": "MANIFEST",
        "manifest_type": "DELIVERY"
    },
    {
        "testrail_case_id": 8116,
        "state": "RETURN_MANIFEST",
        "manifest_type": "DELIVERY"
    },
    {
        "testrail_case_id": 8117,
        "state": "AVAILABLE",
        "manifest_type": "DELIVERY"
    },
    {
        "testrail_case_id": 8118,
        "state": "ISSUED",
        "manifest_type": "DELIVERY"
    },
])
@pytest.mark.regression
def test_add_tags_in_different_statuses_to_manifest(mobile_api, conditions, delete_shipto):
    mobile_api.testrail_case_id = conditions["testrail_case_id"]
    mra = MobileRfidApi(mobile_api)
    ra = RfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": False})
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfids_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfids_labels[0]["id"], conditions["state"])
    updated_rfids_labels = mra.get_rfids_labels_by_location(response_location["location_id"])

    initial_manifest = mra.create_manifest(conditions["manifest_type"])

    mra.add_to_manifest(updated_rfids_labels[0]["labelId"], initial_manifest["data"]["id"], response_location["shipto_id"], expected_status_code=400)
    manifest = mra.get_manifest(initial_manifest["device_id"])
    assert len(manifest["items"]) == 0, f"In Manifest with ID = {initial_manifest['data']['id']} should not be any items"
    
    mra.close_manifest(initial_manifest["data"]["id"])

@pytest.mark.parametrize("conditions", [
    {
        "testrail_case_id": 8119,
        "state": "ASSIGNED",
        "manifest_type": "DELIVERY"
    },
    {
        "testrail_case_id": 8120,
        "state": "ISSUED",
        "manifest_type": "RETURN"
    }

])
@pytest.mark.regression
def test_add_tag_to_manifest_without_permissions(mobile_api, permission_api, conditions, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = conditions["testrail_case_id"]
    Permissions.set_configured_user(mobile_api, Permissions.mobile_rfid_manifest("ENABLE", False))
    mra = MobileRfidApi(permission_api)
    ra = RfidApi(mobile_api)
    super_mra = MobileRfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    super_mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfids_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfids_labels[0]["id"], conditions["state"])
    updated_rfids_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])

    initial_manifest = super_mra.create_manifest(conditions["manifest_type"])
    mra.add_to_manifest(updated_rfids_labels[0]["labelId"], initial_manifest["data"]["id"], response_location["shipto_id"], expected_status_code=400)
    manifest = super_mra.get_manifest(initial_manifest["device_id"])
    assert len(manifest["items"]) == 0, f"RFID tag has not been added to Manifest with ID = {initial_manifest['data']['id']}"

@pytest.mark.parametrize("conditions", [
    {
        "testrail_case_id": 8121,
        "manifest_type": "DELIVERY"
    },
    {
        "testrail_case_id": 8122,
        "manifest_type": "RETURN"
    }
])
@pytest.mark.regression
def test_create_manifest_without_permissions(mobile_api, permission_api, conditions, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = conditions["testrail_case_id"]
    Permissions.set_configured_user(mobile_api, Permissions.mobile_rfid_manifest("ENABLE", False))
    mra = MobileRfidApi(permission_api)

    initial_manifest = mra.create_manifest(conditions["manifest_type"], expected_status_code=400)
    assert initial_manifest["data"] is None, f"Can't create {conditions['manifest_type']} manifest without RFID Manifest permission"

@pytest.mark.parametrize("conditions", [
    {
        "testrail_case_id": 8123,
        "state": "ASSIGNED",
        "manifest_type": "DELIVERY"
    },
    {
        "testrail_case_id": 8124,
        "state": "ISSUED",
        "manifest_type": "RETURN"
    }

])
@pytest.mark.regression
def test_submit_manifest_without_permissions(mobile_api, permission_api, conditions, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = conditions["testrail_case_id"]
    Permissions.set_configured_user(mobile_api, Permissions.mobile_rfid_manifest("ENABLE", False))
    mra = MobileRfidApi(permission_api)
    ra = RfidApi(mobile_api)
    super_mra = MobileRfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    super_mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfids_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfids_labels[0]["id"], conditions["state"])
    updated_rfids_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    tag_state  = updated_rfids_labels[0]['state']

    initial_manifest = super_mra.create_manifest(conditions["manifest_type"])
    super_mra.add_to_manifest(updated_rfids_labels[0]["labelId"], initial_manifest["data"]["id"], response_location["shipto_id"])

    mra.submit_manifest(initial_manifest["data"]["id"], expected_status_code=400)
    manifest = super_mra.get_manifest(initial_manifest["device_id"])
    assert manifest["items"][0]["rfidLabel"]["labelId"] == updated_rfids_labels[0]["labelId"], f"RFID tag should be equal {updated_rfids_labels[0]['labelId']}"
    assert manifest["items"][0]["rfidLabel"]["state"] == tag_state , f"RFID tag should be in status {tag_state}"

@pytest.mark.parametrize("conditions", [
    {
        "testrail_case_id": 8125,
        "state": "ASSIGNED",
        "manifest_type": "DELIVERY"
    },
    {
        "testrail_case_id": 8126,
        "state": "ISSUED",
        "manifest_type": "RETURN"
    }

])
@pytest.mark.regression
def test_delete_items_from_manifest_without_permissions(mobile_api, permission_api, conditions, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = conditions["testrail_case_id"]
    Permissions.set_configured_user(mobile_api, Permissions.mobile_rfid_manifest("ENABLE", False))
    mra = MobileRfidApi(permission_api)
    ra = RfidApi(mobile_api)
    super_mra = MobileRfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    super_mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfids_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfids_labels[0]["id"], conditions["state"])
    updated_rfids_labels = super_mra.get_rfids_labels_by_location(response_location["location_id"])

    initial_manifest = super_mra.create_manifest(conditions["manifest_type"])
    super_mra.add_to_manifest(updated_rfids_labels[0]["labelId"], initial_manifest["data"]["id"], response_location["shipto_id"])
    manifest = super_mra.get_manifest(initial_manifest["device_id"])
    items_qty_before_delete = len(manifest["items"])
    item_id_before_delete = manifest["items"][0]["id"]
    rfid_label_before_delete = manifest["items"][0]["rfidLabel"]["labelId"]


    mra.delete_rfid_label_from_manifest(initial_manifest["data"]["id"], manifest["items"][0]["id"], expected_status_code=400)
    manifest_after_deleted_item = super_mra.get_manifest(initial_manifest["device_id"])
    assert len(manifest_after_deleted_item["items"]) == items_qty_before_delete, f"In Manifest with ID = {initial_manifest['data']['id']} should stay {items_qty_before_delete} item"
    assert manifest_after_deleted_item["items"][0]["id"] == item_id_before_delete, f"Item ID should be equal {item_id_before_delete}"
    assert manifest_after_deleted_item["items"][0]["rfidLabel"]["labelId"] == rfid_label_before_delete, f"RFID tag should be equal {rfid_label_before_delete}"

@pytest.mark.parametrize("conditions", [
    {
        "testrail_case_id": 8127,
        "state": "ASSIGNED",
        "manifest_type": "DELIVERY"
    }
    # {
    #     "testrail_case_id": 8126,
    #     "state": "ISSUED",
    #     "manifest_type": "RETURN"
    # }

])
@pytest.mark.regression
def test_replace_before_submit_in_manifest(mobile_api, conditions):
    mobile_api.testrail_case_id = conditions["testrail_case_id"]
    mra = MobileRfidApi(mobile_api)
    ra = RfidApi(mobile_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "RFID")
    response_location = setup_location.setup()

    mra.create_rfid_label(response_location["location_id"], response_location["shipto_id"], response_location["product"]["partSku"])
    rfids_labels = mra.get_rfids_labels_by_location(response_location["location_id"])
    ra.update_rfid_label(response_location["location_id"], rfids_labels[0]["id"], conditions["state"])
    updated_rfids_labels = mra.get_rfids_labels_by_location(response_location["location_id"])

    initial_manifest = mra.create_manifest(conditions["manifest_type"])

    mra.add_to_manifest(updated_rfids_labels[0]["labelId"], initial_manifest["data"]["id"], response_location["shipto_id"])
    manifest = mra.get_manifest(initial_manifest["device_id"])

    mra.replace_rfid_label_in_manifest(initial_manifest["data"]["id"], manifest["items"][0]["id"])
    manifest_after_replace = mra.get_manifest(initial_manifest["device_id"])
    print(manifest_after_replace["items"])
