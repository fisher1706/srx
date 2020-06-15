from src.resources.case import Case
from src.resources.activity import Activity
from src.pages.sub.login_page import LoginPage
from src.pages.customer.assets_page import AssetsPage
from src.bases.location_basis import location_basis
from src.bases.issue_return_basis import issue_return_basis
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.resources.tools import Tools


def ping_to_return_asset(case):
    case.log_name("Request return asset")
    case.testrail_config(1993)

    try:
        lp = LoginPage(case.activity)
        ap = AssetsPage(case.activity)
        sa = ShiptoApi(case)
        sta = SettingsApi(case)
        cha = CheckoutGroupApi(case)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        #create location with asset product
        response = location_basis(case, product_dto=product_dto)
        asset = response["product"]["partSku"]
        #shipto_name = response["shipto"]["number"]
        shipto_id = response["shipto_id"]
        total = response["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        cha.add_shipto_to_checkout_group(shipto_id=shipto_id)

        lp.log_in_customer_portal()
        ap.sidebar_assets()
        # issue 2 assets
        issue_return_basis(case, shipto_id, asset, quantity=5, issue_product=True, passcode=case.activity.variables.passcode)
        lp.page_refresh()
        lp.wait_until_progress_bar_loaded()
        ap.ping_to_return_last_asset()

        case.finish_case()
    except:
        case.critical_finish_case()
    
    try:
        sa.delete_shipto(shipto_id)
    except:
        case.print_traceback()

if __name__ == "__main__":
    ping_to_return_asset(Case(Activity()))