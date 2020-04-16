from src.resources.case import Case
from src.resources.activity import Activity
from src.pages.sub.login_page import LoginPage
from src.pages.customer.assets_page import AssetsPage
from src.bases.location_basis import location_basis
from src.bases.issue_return_basis import issue_return_basis
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.resources.tools import Tools


def issue_return_assets_label(case):
    case.log_name("Issue/return asset as customer user, location type: label")
    case.testrail_config(1991)

    try:
        lp = LoginPage(case.activity)
        ap = AssetsPage(case.activity)
        sa = ShiptoApi(case)
        sta = SettingsApi(case)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = "1"
        product_dto["assetFlag"] = True

        #create location with asset product
        response = location_basis(case, product_dto=product_dto)
        asset = response["product"]["partSku"]
        shipto_name = response["shipto"]["number"]
        shipto_id = response["shipto_id"]
        total = response["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        
        lp.log_in_customer_portal()
        ap.sidebar_assets()
        ap.check_all_assets_tab(asset, shipto_name, total, total, 0)
        # issue 2 assets
        issue_return_basis(case, shipto_id, asset, 2, issue_product=True)
        lp.page_refresh()
        lp.wait_until_progress_bar_loaded()
        ap.check_all_assets_tab(asset, shipto_name, int(total)-2, total,  2)
        ap.check_checked_out_tab(asset, shipto_name, int(total)-2, total, 2)
        # return 1 asset
        issue_return_basis(case, shipto_id, asset, 1, return_product=True)
        lp.page_refresh()
        lp.wait_until_progress_bar_loaded()
        ap.check_all_assets_tab(asset, shipto_name, int(total)-1, total, 1)
        ap.check_checked_out_tab(asset, shipto_name, int(total)-1, total, 1)
        # return 1 asset
        issue_return_basis(case, shipto_id, asset, 1, return_product=True)
        lp.page_refresh()
        lp.wait_until_progress_bar_loaded()
        ap.check_all_assets_tab(asset, shipto_name, total, total, 0)
        ap.checked_out_tab_should_not_contain(asset)

        case.finish_case()
    except:
        case.critical_finish_case()
    
    try:
        sa.delete_shipto(shipto_id)
    except:
        case.print_traceback()

if __name__ == "__main__":
    issue_return_assets_label(Case(Activity()))