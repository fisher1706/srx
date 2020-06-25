import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.customer.assets_page import AssetsPage
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_issue_return import setup_issue_return
from src.api.distributor.settings_api import SettingsApi
from src.api.customer.checkout_group_api import CheckoutGroupApi

class TestAssets():
    
    @pytest.mark.regression
    def test_issue_return_assets_label(self, ui, delete_shipto):
        ui.testrail_case_id = 1993

        lp = LoginPage(ui)
        ap = AssetsPage(ui)
        sta = SettingsApi(ui)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = "1"
        product_dto["assetFlag"] = True

        #create location with asset product
        response_location = setup_location(ui, product_dto=product_dto)
        asset = response_location["product"]["partSku"]
        shipto_name = response_location["shipto"]["number"]
        shipto_id = response_location["shipto_id"]
        total = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        
        lp.log_in_customer_portal()
        ap.sidebar_assets()
        ap.check_all_assets_tab(asset, shipto_name, total, total, 0)
        # issue 2 assets
        setup_issue_return(ui, shipto_id, asset, quantity=2, issue_product=True)
        lp.page_refresh()
        lp.wait_until_progress_bar_loaded()
        ap.check_all_assets_tab(asset, shipto_name, int(total)-2, total,  2)
        ap.check_checked_out_tab(asset, shipto_name, int(total)-2, total, 2)
        # return 1 asset
        setup_issue_return(ui, shipto_id, asset, quantity=1, return_product=True)
        lp.page_refresh()
        lp.wait_until_progress_bar_loaded()
        ap.check_all_assets_tab(asset, shipto_name, int(total)-1, total, 1)
        ap.check_checked_out_tab(asset, shipto_name, int(total)-1, total, 1)
        # return 1 asset
        setup_issue_return(ui, shipto_id, asset, quantity=1, return_product=True)
        lp.page_refresh()
        lp.wait_until_progress_bar_loaded()
        ap.check_all_assets_tab(asset, shipto_name, total, total, 0)
        ap.checked_out_tab_should_not_contain(asset)

    @pytest.mark.test777
    def test_ping_to_return_asset(self, ui, delete_shipto):
        ui.testrail_case_id = 1991

        lp = LoginPage(ui)
        ap = AssetsPage(ui)
        sta = SettingsApi(ui)
        cha = CheckoutGroupApi(ui)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        #create location with asset product
        response_location = setup_location(ui, product_dto=product_dto)
        asset = response_location["product"]["partSku"]
        #shipto_name = response_location["shipto"]["number"]
        shipto_id = response_location["shipto_id"]
        total = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        cha.add_shipto_to_checkout_group(shipto_id=shipto_id)

        lp.log_in_customer_portal()
        ap.sidebar_assets()
        # issue 2 assets
        setup_issue_return(ui, shipto_id, asset, quantity=5, issue_product=True, passcode=ui.data.passcode)
        lp.page_refresh()
        lp.wait_until_progress_bar_loaded()
        ap.ping_to_return_last_asset()
