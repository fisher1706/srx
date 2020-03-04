from src.pages.sub.login_page import LoginPage
from src.pages.customer.reorder_list_page import ReorderListPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.settings_api import SettingsApi
from src.bases.location_basis import location_basis

def general_multiple_po_number(case):
    case.log_name("General multiple PO numbers")
    case.testrail_config(case.activity.variables.run_number, 106)

    try:
        lp = LoginPage(case.activity)
        rlp = ReorderListPage(case.activity)
        sa = ShiptoApi(case)
        ta = TransactionApi(case)
        la = LocationApi(case)
        sta = SettingsApi(case)

        response_1 = location_basis(case)
        response_2 = location_basis(case)
        product_1_dto = response_1["product"]
        product_2_dto = response_2["product"]
        shipto_1_dto = response_1["shipto"]
        shipto_2_dto = response_2["shipto"]
        new_shipto_1 = response_1["shipto_id"]
        new_shipto_2 = response_2["shipto_id"]
        
        sta.set_checkout_software_settings_for_shipto(new_shipto_1)
        sta.set_checkout_software_settings_for_shipto(new_shipto_1)

        ta.create_active_item(new_shipto_1, la.get_ordering_config_by_sku(new_shipto_1, product_1_dto["partSku"]))
        ta.create_active_item(new_shipto_2, la.get_ordering_config_by_sku(new_shipto_2, product_2_dto["partSku"]))

        lp.log_in_customer_portal()
        rlp.sidebar_orders_and_quotes()
        rlp.unselect_all()
        rlp.select_by_sku(product_1_dto["partSku"])
        rlp.select_by_sku(product_2_dto["partSku"])

        new_po_number = case.random_string_l(10)
        rlp.submit_replenishment_list_general_po(new_po_number)

        sa.check_po_number_by_number(shipto_1_dto["number"], new_po_number)
        sa.check_po_number_by_number(shipto_2_dto["number"], new_po_number)

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        sa.delete_shipto(new_shipto_1)
        sa.delete_shipto(new_shipto_2)
    except:
        case.print_traceback()

if __name__ == "__main__":
    general_multiple_po_number(Case(Activity()))