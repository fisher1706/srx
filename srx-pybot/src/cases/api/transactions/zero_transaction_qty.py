from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.settings_api import SettingsApi
from src.bases.location_basis import location_basis

def zero_transaction_qty(case):
    case.log_name("Zero quantity of new transaction")
    case.testrail_config(case.activity.variables.run_number, 1841)

    try:
        sa = ShiptoApi(case)
        ta = TransactionApi(case)
        la = LocationApi(case)
        sta = SettingsApi(case)

        response = location_basis(case)
        product_dto = response["product"]
        shipto_dto = response["shipto"]
        new_shipto = response["shipto_number"]
        
        sta.set_checkout_software_settings_for_shipto(new_shipto)

        ordering_config_id = la.get_ordering_config_by_sku(new_shipto, product_dto["partSku"])
        ta.create_active_item(new_shipto, ordering_config_id)
        transaction_id = ta.get_transaction_id(sku=product_dto["partSku"], shipto_id=new_shipto)
        ta.update_replenishment_item(transaction_id, product_dto["roundBuy"], "QUOTED")

        ta.create_active_item(new_shipto, ordering_config_id)
        new_transaction_id, new_transaction_qty = ta.get_transaction_id_and_qty(sku=product_dto["partSku"], status="ACTIVE", shipto_id=new_shipto)
        assert new_transaction_qty == 0, "The quantity of new transaction should be 0"
        ta.update_replenishment_item(new_transaction_id, product_dto["roundBuy"], "DELIVERED")
        ta.update_replenishment_item(transaction_id, product_dto["roundBuy"], "ORDERED")

        ta.create_active_item(new_shipto, ordering_config_id)
        new_transaction_id, new_transaction_qty = ta.get_transaction_id_and_qty(sku=product_dto["partSku"], status="ACTIVE", shipto_id=new_shipto)
        assert new_transaction_qty == 0, "The quantity of new transaction should be 0"
        ta.update_replenishment_item(new_transaction_id, product_dto["roundBuy"], "DELIVERED")
        ta.update_replenishment_item(transaction_id, product_dto["roundBuy"], "SHIPPED")

        ta.create_active_item(new_shipto, ordering_config_id)
        new_transaction_id, new_transaction_qty = ta.get_transaction_id_and_qty(sku=product_dto["partSku"], status="ACTIVE", shipto_id=new_shipto)
        assert new_transaction_qty == 0, "The quantity of new transaction should be 0"

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        sa.delete_shipto(new_shipto)
    except:
        case.print_traceback()

if __name__ == "__main__":
    zero_transaction_qty(Case(Activity(api_test=True)))