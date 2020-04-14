from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.location_api import LocationApi
from src.api.admin.admin_billing_api import AdminBillingApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.settings_api import SettingsApi
from src.bases.location_basis import location_basis

def label_wake_up(case):
    case.log_name("Label Wake Up")
    case.testrail_config(1887)

    try:
        timestamp_another_day = 1736035200000
        sa = ShiptoApi(case)
        aba = AdminBillingApi(case)
        la = LocationApi(case)
        ta = TransactionApi(case)
        sta = SettingsApi(case)

        response = location_basis(case)
        new_shipto = response["shipto_id"]
        product_body = response["product"]

        sta.set_checkout_software_settings_for_shipto(new_shipto)

        aba.billing_transit(timestamp_another_day)
        aba.billing_transit(timestamp_another_day)

        location_body = la.get_location_by_sku(new_shipto, product_body["partSku"])
        ordering_config_id = location_body[0]["orderingConfig"]["id"]
        assert location_body[0]["inventoryStatus"] == "FROZEN", f"Location should be in FROZEN inventory status, now {location_body[0]['inventoryStatus']}"

        ta.create_active_item(new_shipto, ordering_config_id)
        location_body = la.get_location_by_sku(new_shipto, product_body["partSku"])
        assert location_body[0]["inventoryStatus"] == "SLOW", f"Location should be in SLOW inventory status, now {location_body[0]['inventoryStatus']}"

        transaction_id = ta.get_transaction_id(sku=product_body["partSku"], shipto_id=new_shipto)
        ta.update_replenishment_item(transaction_id, product_body["roundBuy"], "DELIVERED")

        ta.create_active_item(new_shipto, ordering_config_id)
        location_body = la.get_location_by_sku(new_shipto, product_body["partSku"])
        assert location_body[0]["inventoryStatus"] == "MOVING", f"Location should be in MOVING inventory status, now {location_body[0]['inventoryStatus']}"

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        sa.delete_shipto(new_shipto)
    except:
        case.print_traceback()

if __name__ == "__main__":
    label_wake_up(Case(Activity(api_test=True)))