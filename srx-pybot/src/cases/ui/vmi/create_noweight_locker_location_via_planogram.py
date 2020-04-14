from src.pages.sub.login_page import LoginPage
from src.pages.distributor.locker_planogram_page import LockerPlanogramPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.shipto_basis import shipto_basis
from src.bases.product_basis import product_basis
from src.bases.locker_basis import locker_basis
from src.api.distributor.shipto_api import ShiptoApi
from src.api.admin.hardware_api import HardwareApi
from src.api.distributor.location_api import LocationApi
import time

def create_noweight_locker_location_via_planogram(case):
    try:
        case.log_name("Create NoWeight locker location via planogram")
        case.testrail_config(1856)

        lp = LoginPage(case.activity)
        lpp = LockerPlanogramPage(case.activity)
        sa = ShiptoApi(case)
        ha = HardwareApi(case)
        la = LocationApi(case)

        lp.log_in_distributor_portal()

        shipto_response = shipto_basis(case)
        shipto_id = shipto_response["shipto_id"]
        product_response = product_basis(case)
        product_sku = product_response["partSku"]
        round_buy = product_response["roundBuy"]
        locker_response = locker_basis(case, shipto=shipto_id, no_weight=True)

        lpp.follow_locker_planogram_url(shipto_id=shipto_id)
        lpp.create_location_via_planogram(1, 1, product_sku, round_buy, round_buy*3)
        locations = la.get_location_by_sku(shipto_id, product_sku)
        assert len(locations) == 1, "There should be 1 location with SKU = '{product_sku}'"
        assert locations[0]["orderingConfig"]["lockerWithNoWeights"] == True, "Locations should be with NoWeight flag"

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        time.sleep(5)
        ha.delete_hardware(locker_response["locker"]["id"])
        time.sleep(5)
        ha.delete_hardware(locker_response["iothub"]["id"])
        sa.delete_shipto(shipto_id)
    except:
        case.print_traceback()

if __name__ == "__main__":
    create_noweight_locker_location_via_planogram(Case(Activity()))