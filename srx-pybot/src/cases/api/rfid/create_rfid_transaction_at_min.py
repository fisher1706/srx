from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.admin.hardware_api import HardwareApi
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.transaction_api import TransactionApi
from src.bases.rfid_location_basis import rfid_location_basis
from src.bases.rfid_basis import rfid_basis
from src.api.api_methods import ApiMethods as apim

def create_rfid_transaction_at_min(case):
    case.log_name("Create transaction for RFID location by RFID Read (at min)")
    case.testrail_config(case.activity.variables.run_number, 1913)

    try:
        sa = ShiptoApi(case)
        ha = HardwareApi(case)
        ra = RfidApi(case)
        sta = SettingsApi(case)
        ta = TransactionApi(case)

        rfid_location_response = rfid_location_basis(case, number_of_labels=1)
        test_label = rfid_location_response["labels"][0]["label"]
        ra.update_rfid_label(rfid_location_response["location_id"], rfid_location_response["labels"][0]["rfid_id"], "AVAILABLE")
        rfid_response = rfid_basis(case, rfid_location_response["shipto_id"])

        checkout_settings_dto = apim.get_dto("checkout_settings_dto.json")
        sta.update_checkout_software_settings_shipto(checkout_settings_dto, rfid_location_response["shipto_id"])

        
        ra.rfid_issue(rfid_response["value"], test_label)
        rfid_labels_response = ra.get_rfid_labels(rfid_location_response["location_id"])
        test_label_body = rfid_labels_response[0]

        assert test_label_body["state"] == "ISSUED", f"RFID label should be in AVAILABLE status, now {test_label_body['state']}"

        transaction = ta.get_transaction(shipto_id=rfid_location_response["shipto_id"])["entities"]
        assert len(transaction) == 1, "The number of transactions should be equal to 1"
        assert transaction[0]["reorderQuantity"] == (rfid_location_response["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {rfid_location_response['product']['roundBuy']*3}"
        assert transaction[0]["product"]["partSku"] == rfid_location_response["product"]["partSku"]

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(rfid_response["id"])
        sa.delete_shipto(rfid_location_response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    create_rfid_transaction_at_min(Case(Activity(api_test=True)))