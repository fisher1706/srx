from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.admin.hardware_api import HardwareApi
from src.api.distributor.settings_api import SettingsApi
from src.bases.locker_location_basis import locker_location_basis
import time
import copy

def create_transaction_for_noweight_locker(case):
    case.log_name("Create transaction for NoWeight locker by changing OHI")
    case.testrail_config(1853)

    try:
        sha = ShiptoApi(case)
        ta = TransactionApi(case)
        la = LocationApi(case)
        ha = HardwareApi(case)
        sta = SettingsApi(case)

        location_response = locker_location_basis(case, no_weight=True)
        sta.set_checkout_software_settings_for_shipto(location_response["shipto_id"])

        location_id = la.get_location_by_sku(location_response["shipto_id"], location_response["product"]["partSku"])[0]["id"]
        location_body = copy.deepcopy(location_response["location"])
        location_dto = copy.deepcopy(location_body)
        location_dto["onHandInventory"] = 1
        location_dto["orderingConfig"]["lockerWithNoWeights"] = True
        location_dto["id"] = location_id
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, location_response["shipto_id"])
        transaction = ta.get_transaction(shipto_id=location_response["shipto_id"])["entities"]
        assert len(transaction) == 1, "The number of transactions should be equal to 1"
        assert transaction[0]["reorderQuantity"] == (location_response["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {location_response['product']['roundBuy']*3}"
        assert transaction[0]["product"]["partSku"] == location_response["product"]["partSku"]

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        time.sleep(5)
        ha.delete_hardware(location_response["locker"]["id"])
        time.sleep(5)
        ha.delete_hardware(location_response["iothub"]["id"])
        sha.delete_shipto(location_response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    create_transaction_for_noweight_locker(Case(Activity(api_test=True)))
