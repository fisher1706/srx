from src.pages.sub.login_page import LoginPage
from src.pages.distributor.vmi_page import VmiPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.shipto_basis import shipto_basis
from src.bases.product_basis import product_basis
from src.api.distributor.shipto_api import ShiptoApi
import time

def vmi_list_partial_sku_match(case):
    case.log_name("A partial SKU match during create location")
    case.testrail_config(case.activity.variables.run_number, 1838)

    try:
        lp = LoginPage(case.activity)
        vp = VmiPage(case.activity)
        sa = ShiptoApi(case)

        lp.log_in_distributor_portal()

        shipto_response = shipto_basis(case)
        shipto_id = shipto_response["shipto_id"]
        product_dto = product_basis(case)
        product_sku = product_dto["partSku"]


        vp.follow_location_url()
        vp.click_id(vp.locators.id_add_button)
        vp.input_data_xpath(product_sku, vp.locators.xpath_dialog+vp.locators.xpath_select_box+"//input")
        vp.wait_until_dropdown_list_loaded(1)
        vp.check_found_dropdown_list_item(vp.locators.xpath_dropdown_list_item, product_sku)

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        sa.delete_shipto(shipto_id)
    except:
        case.print_traceback()

if __name__ == "__main__":
    vmi_list_partial_sku_match(Case(Activity()))