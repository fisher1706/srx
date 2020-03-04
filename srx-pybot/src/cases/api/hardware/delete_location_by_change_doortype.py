from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.location_api import LocationApi
from src.api.admin.hardware_api import HardwareApi
from src.bases.locker_location_basis import locker_location_basis
import time

def delete_location_by_change_doortype(case):
    case.log_name("Delete location by change doortype")
    case.testrail_config(case.activity.variables.run_number, 1852)

    try:
        sa = ShiptoApi(case)
        ha = HardwareApi(case)
        la = LocationApi(case)

        location_response = locker_location_basis(case)
        original_location_count = len(la.get_locations(location_response["shipto_id"]))
        assert original_location_count == 1, "The number of location should be 1"
        ha.update_locker_configuration(location_response["locker"]["id"], 1, True)
        new_location_count = len(la.get_locations(location_response["shipto_id"]))
        assert new_location_count == 0, "The number of location should be 0"

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        time.sleep(5)
        ha.delete_hardware(location_response["locker"]["id"])
        time.sleep(5)
        ha.delete_hardware(location_response["iothub"]["id"])
        sa.delete_shipto(location_response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    delete_location_by_change_doortype(Case(Activity(api_test=True)))