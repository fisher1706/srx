from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.admin.hardware_api import HardwareApi
from src.api.distributor.rfid_api import RfidApi
from src.bases.rfid_location_basis import rfid_location_basis
from src.bases.rfid_basis import rfid_basis
import time

def full_rfid_available_flow(case):
    case.log_name("Full workflow of RFID label from ASSIGNED to AVAILABLE")
    case.testrail_config(1911)

    try:
        sa = ShiptoApi(case)
        ha = HardwareApi(case)
        ra = RfidApi(case)

        rfid_location_response = rfid_location_basis(case, number_of_labels=1)
        test_label = rfid_location_response["labels"][0]["label"]
        rfid_response = rfid_basis(case, rfid_location_response["shipto_id"])

        initial_manifest_body = ra.get_new_delivery_manifest()
        ra.add_to_manifest(test_label, initial_manifest_body["data"]["id"], rfid_location_response["shipto_id"])
        manifest_body_1 = ra.get_manifest(initial_manifest_body["device_id"])

        assert len(manifest_body_1["items"]) == 1, "Only 1 RFID label should being in the manifest"
        assert str(manifest_body_1["items"][0]["rfidLabel"]["id"]) == str(rfid_location_response["labels"][0]["rfid_id"])
        assert manifest_body_1["items"][0]["rfidLabel"]["labelId"] == test_label
        assert manifest_body_1["items"][0]["rfidLabel"]["state"] == "ASSIGNED", f"RFID label should be in ASSIGNED status, now {manifest_body_1['items'][0]['rfidLabel']['state']}"

        ra.submit_manifest(initial_manifest_body["data"]["id"])
        manifest_body_2 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_2["items"][0]["rfidLabel"]["state"] == "MANIFEST", f"RFID label should be in MANIFEST status, now {manifest_body_2['items'][0]['rfidLabel']['state']}"

        ra.rfid_issue(rfid_response["value"], test_label)
        manifest_body_3 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_3["items"][0]["rfidLabel"]["state"] == "CHECK_IN", f"RFID label should be in CHECK_IN status, now {manifest_body_3['items'][0]['rfidLabel']['state']}"

        ra.close_manifest(initial_manifest_body["data"]["id"])
        ra.rfid_put_away(rfid_location_response["shipto_id"], rfid_location_response["labels"][0]["rfid_id"])
        rfid_labels_response = ra.get_rfid_labels(rfid_location_response["location_id"])

        assert len(rfid_labels_response) == 1, f"Location with ID = '{rfid_location_response['location_id']}' should contain only 1 RFID label, now {len(rfid_labels_response)}"
        
        test_label_body = rfid_labels_response[0]

        assert test_label_body["state"] == "AVAILABLE", f"RFID label should be in AVAILABLE status, now {test_label_body['state']}"
        assert test_label_body["returned"] == False, "'returned' flag of RFID label should be FALSE"

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(rfid_response["id"])
        sa.delete_shipto(rfid_location_response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    full_rfid_available_flow(Case(Activity(api_test=True)))