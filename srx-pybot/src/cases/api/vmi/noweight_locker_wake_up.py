from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.location_api import LocationApi
from src.api.admin.admin_billing_api import AdminBillingApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.settings_api import SettingsApi
from src.api.admin.hardware_api import HardwareApi
from src.api.api_methods import ApiMethods as apim
from src.bases.locker_location_basis import locker_location_basis
import time
import copy

def noweight_locker_wake_up(case):
    case.log_name("NoWeight locker Wake Up")
    case.testrail_config(case.activity.variables.run_number, 1888)

    try:
        timestamp_another_day = 1736035200000
        sa = ShiptoApi(case)
        aba = AdminBillingApi(case)
        la = LocationApi(case)
        ta = TransactionApi(case)
        sta = SettingsApi(case)
        ha = HardwareApi(case)

        location_response = locker_location_basis(case, no_weight=True)
        new_shipto = location_response["shipto_id"]
        product_body = location_response["product"]

        checkout_settings_dto = apim.get_dto("checkout_settings_dto.json")
        sta.update_checkout_software_settings_shipto(checkout_settings_dto, new_shipto)

        aba.billing_transit(timestamp_another_day)
        aba.billing_transit(timestamp_another_day)

        location_body = la.get_location_by_sku(new_shipto, product_body["partSku"])
        location_id = location_body[0]["id"]
        assert location_body[0]["inventoryStatus"] == "FROZEN", "Location should be in FROZEN inventory status"

        location_body = copy.deepcopy(location_response["location"])
        location_dto = copy.deepcopy(location_body)
        location_dto["onHandInventory"] = 1
        location_dto["orderingConfig"]["lockerWithNoWeights"] = True
        location_dto["id"] = location_id
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, new_shipto)

        location_body = la.get_location_by_sku(new_shipto, product_body["partSku"])
        assert location_body[0]["inventoryStatus"] == "SLOW", "Location should be in SLOW inventory status"

        transaction_id = ta.get_transaction_id(sku=product_body["partSku"], shipto_id=new_shipto)
        ta.update_replenishment_item(transaction_id, product_body["roundBuy"], "DELIVERED")

        location_dto["onHandInventory"] = 0
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, new_shipto)

        location_body = la.get_location_by_sku(new_shipto, product_body["partSku"])
        assert location_body[0]["inventoryStatus"] == "MOVING", "Location should be in MOVING inventory status"

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        time.sleep(5)
        ha.delete_hardware(location_response["locker"]["id"])
        time.sleep(5)
        ha.delete_hardware(location_response["iothub"]["id"])
        sa.delete_shipto(new_shipto)
    except:
        case.print_traceback()

if __name__ == "__main__":
    noweight_locker_wake_up(Case(Activity(api_test=True)))