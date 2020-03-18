from src.pages.sub.login_page import LoginPage
from src.pages.distributor.rfid_page import RfidPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.location_basis import location_basis
from src.api.distributor.shipto_api import ShiptoApi

def rfid_label_crud(case):
    case.log_name("RFID label CRUD")
    #case.testrail_config(case.activity.variables.run_number, 28)

    try:
        lp = LoginPage(case.activity)
        rp = RfidPage(case.activity)
        sa = ShiptoApi(case)

        location_response = location_basis(case, location_type="RFID")
        shipto_text = f"{case.activity.variables.customer_name} - {location_response['shipto']['number']}"
        product_sku = location_response["product"]["partSku"]

        lp.log_in_distributor_portal()
        rp.sidebar_rfid()
        rp.select_shipto_sku(shipto_text, product_sku)
        rfid_label = rp.add_rfid_label()
        rp.check_last_rfid_label(rfid_label, "ASSIGNED")
        rp.update_last_rfid_label_status("ISSUED")
        rp.should_be_disabled_xpath(rp.locators.xpath_by_count(rp.locators.title_unassign, rp.get_table_rows_number()))
        new_status = "AVAILABLE"
        rp.update_last_rfid_label_status(new_status)
        rp.check_last_rfid_label(rfid_label, new_status)
        rp.unassign_last_rfid_label()
        
        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        sa.delete_shipto(location_response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    rfid_label_crud(Case(Activity()))