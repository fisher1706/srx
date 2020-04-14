from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.admin.hardware_api import HardwareApi
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.transaction_api import TransactionApi
from src.bases.rfid_location_basis import rfid_location_basis
from src.bases.rfid_basis import rfid_basis

def create_rfid_transaction_as_issued(case):
    case.log_name("Create transaction for RFID location by RFID Read (as issued)")
    case.testrail_config(1914)

    try:
        sa = ShiptoApi(case)
        ha = HardwareApi(case)
        ra = RfidApi(case)
        sta = SettingsApi(case)
        ta = TransactionApi(case)

        rfid_location_response = rfid_location_basis(case, number_of_labels=3)
        ra.update_rfid_label(rfid_location_response["location_id"], rfid_location_response["labels"][0]["rfid_id"], "AVAILABLE")
        ra.update_rfid_label(rfid_location_response["location_id"], rfid_location_response["labels"][1]["rfid_id"], "AVAILABLE")
        ra.update_rfid_label(rfid_location_response["location_id"], rfid_location_response["labels"][2]["rfid_id"], "AVAILABLE")
        rfid_response = rfid_basis(case, rfid_location_response["shipto_id"])

        sta.set_checkout_software_settings_for_shipto(rfid_location_response["shipto_id"], reorder_controls="ISSUED")
        
        ra.rfid_issue(rfid_response["value"], rfid_location_response["labels"][0]["label"])

        transaction = ta.get_transaction(shipto_id=rfid_location_response["shipto_id"])["entities"]
        assert len(transaction) == 1, "The number of transactions should be equal to 1"
        assert transaction[0]["reorderQuantity"] == rfid_location_response["product"]["roundBuy"], f"Reorder quantity of transaction should be equal to {rfid_location_response['product']['roundBuy']}"
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
    create_rfid_transaction_as_issued(Case(Activity(api_test=True)))