from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.distributor_billing_api import DistributorBillingApi
from src.api.admin.admin_billing_api import AdminBillingApi
from src.bases.location_basis import location_basis
import time

def total_triggers_include_all_movement_statuses(case):
    case.log_name("Total Triggers include all movement statuses")
    case.testrail_config(case.activity.variables.run_number, 1886)

    try:
        timestamp_first_day = 1735689600000
        timestamp_another_day = 1736035200000
        sa = ShiptoApi(case)
        dba = DistributorBillingApi(case)
        aba = AdminBillingApi(case)
        la = LocationApi(case)

        aba.billing_calculate(timestamp_another_day)
        aba.billing_calculate(timestamp_first_day)
        aba.billing_calculate(timestamp_first_day)

        start_total_triggers = dba.get_distributor_fees()["totalTriggers"]

        response = location_basis(case)
        new_shipto = response["shipto_number"]
        product_body = response["product"]

        aba.billing_calculate(timestamp_another_day)
        aba.billing_calculate(timestamp_first_day)

        moving_total_triggers = dba.get_distributor_fees()["totalTriggers"]
        assert moving_total_triggers == start_total_triggers + 1, "The number of triggers should be increased by 1"

        location_body = la.get_location_by_sku(new_shipto, product_body["partSku"])
        assert location_body[0]["inventoryStatus"] == "MOVING", "New location should be created in MOVING inventory status"

        aba.billing_transit(timestamp_another_day)
        aba.billing_calculate(timestamp_another_day)
        aba.billing_calculate(timestamp_first_day)

        slow_total_triggers = dba.get_distributor_fees()["totalTriggers"]
        assert slow_total_triggers == start_total_triggers + 1, "The number of triggers should be increased by 1"

        location_body = la.get_location_by_sku(new_shipto, product_body["partSku"])
        assert location_body[0]["inventoryStatus"] == "SLOW", "New location should be in SLOW inventory status"

        aba.billing_transit(timestamp_another_day)
        aba.billing_calculate(timestamp_another_day)
        aba.billing_calculate(timestamp_first_day)

        frozen_total_triggers = dba.get_distributor_fees()["totalTriggers"]
        assert slow_total_triggers == start_total_triggers + 1, "The number of triggers should be increased by 1"

        location_body = la.get_location_by_sku(new_shipto, product_body["partSku"])
        assert location_body[0]["inventoryStatus"] == "FROZEN", "New location should be in FROZEN inventory status"

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        sa.delete_shipto(new_shipto)
    except:
        case.print_traceback()

if __name__ == "__main__":
    total_triggers_include_all_movement_statuses(Case(Activity(api_test=True)))