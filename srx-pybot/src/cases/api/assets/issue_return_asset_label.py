from src.resources.case import Case
from src.resources.activity import Activity
from src.pages.sub.login_page import LoginPage
from src.pages.customer.assets_page import AssetsPage
from src.bases.location_basis import location_basis
from src.api.customer.assets_api import AssetsApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.checkout.checkout_api import CheckoutApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.settings_api import SettingsApi
from src.resources.tools import Tools


def issue_return_assets_label(case):
    case.log_name("Issue/return asset as customer user, location type: label")
    #case.testrail_config(case.activity.variables.run_number, 1991)

    try:
        lp = LoginPage(case.activity)
        ap = AssetsPage(case.activity)
        aa = AssetsApi(case)
        sa = ShiptoApi(case)
        ca = CheckoutApi(case)
        la = LocationApi(case)
        sta = SettingsApi(case)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = "1"
        product_dto["assetFlag"] = True

        # create location with asset product
        response = location_basis(case, product_dto=product_dto)
        asset = response["product"]["partSku"]
        shipto = response["shipto"]["number"]

        total = response["location"]["orderingConfig"]["currentInventoryControls"]["max"]
        
        sta.set_checkout_software_settings_for_shipto(response["shipto_id"])
        lp.log_in_customer_portal()
        ap.sidebar_assets()
        ap.check_all_assets_tab(asset, shipto, total, total, 0)
        location_response = la.get_location_by_sku(shipto_id=response["shipto_id"], sku=asset)
        location_response[0]["quantity"] = 2
        print(location_response[0]["id"])
        # issue 2 assets
        ca.checkout_cart(location_response[0]["id"], 2, "LABEL")
        cart_response = ca.get_cart()
        location_response[0]["cartItemId"] = cart_response["items"][0]["cartItemId"]
        ca.issue_product(location_response[0])
        #lp.page_refresh()
        #lp.wait_until_progress_bar_loaded()
        #ap.check_all_assets_tab(asset, shipto, total, total-2, 2)
        #ap.check_checked_out_tab(asset, shipto, total-2, total, 2)


        case.finish_case()
    except:
        case.critical_finish_case()
    
    try:
        sa.delete_shipto(response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    issue_return_assets_label(Case(Activity()))