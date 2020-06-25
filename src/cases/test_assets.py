import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.customer.assets_page import AssetsPage
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_issue_return import setup_issue_return
from src.api.setups.setup_rfid_location import setup_rfid_location
from src.api.setups.setup_rfid import setup_rfid
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.api.customer.assets_api import AssetsApi
import copy

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

    @pytest.mark.regression
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

    @pytest.mark.regression
    def test_check_asstes_of_checkout_user(self, api, delete_shipto):
        api.testrail_case_id = 1995

        aa = AssetsApi(api)
        sta = SettingsApi(api)
        cha = CheckoutGroupApi(api)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        #create location with asset product
        response_location = setup_location(api, product_dto=product_dto)
        asset = response_location["product"]["partSku"]
        shipto_name = response_location["shipto"]["number"]
        shipto_id = response_location["shipto_id"]
        total = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        cha.add_shipto_to_checkout_group(shipto_id=shipto_id)

        # issue 5 assets
        setup_issue_return(api, shipto_id, asset, quantity=5, issue_product=True, passcode=api.data.passcode)
        # check list of assets of checkout user
        list_of_assets = aa.get_list_of_assets_by_user(api.data.checkout_user_id)
        for item in list_of_assets:
            assert f"{item['user']['id']}" == api.data.checkout_user_id, "There are assets that was issued NOT by checkout user"

    @pytest.mark.regression
    def test_checkout_asset_customer_checkout_user(self, api, delete_shipto):
        api.testrail_case_id = 1995

        aa = AssetsApi(api)
        sta = SettingsApi(api)
        cha = CheckoutGroupApi(api)

        first_product_dto = Tools.get_dto("product_dto.json")
        first_product_dto["partSku"] = Tools.random_string_u(18)
        first_product_dto["shortDescription"] = f"{first_product_dto['partSku']} - short description"
        first_product_dto["roundBuy"] = 5
        first_product_dto["assetFlag"] = True

        second_product_dto = Tools.get_dto("product_dto.json")
        second_product_dto["partSku"] = Tools.random_string_u(18)
        second_product_dto["shortDescription"] = f"{second_product_dto['partSku']} - short description"
        second_product_dto["roundBuy"] = 5
        second_product_dto["assetFlag"] = True

        #create location with asset product
        first_response_location = setup_location(api, product_dto=first_product_dto)
        first_asset = first_response_location["product"]["partSku"]
        shipto_id = first_response_location["shipto_id"]

        #create location with asset product
        second_response_location = setup_location(api, shipto_dto=False, shipto_id=shipto_id, product_dto=second_product_dto)
        second_asset = second_response_location["product"]["partSku"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        cha.add_shipto_to_checkout_group(shipto_id=shipto_id)

        setup_issue_return(api, shipto_id, first_asset, quantity=5, issue_product=True)
        setup_issue_return(api, shipto_id, second_asset, quantity=5, issue_product=True, passcode=api.data.customer_user_passcode)
        assets_list = aa.get_list_of_assets_by_user(api.data.customer_user_id)
        sku_list = []
        for item in assets_list:
            sku_list.append(item["partSku"])
            assert f"{item['user']['id']}" == api.data.customer_user_id, "There are assets that was issued NOT by current customer user"
        assert first_asset in sku_list, f"{first_asset} was not found in list of assets issued by user"
        assert second_asset in sku_list, f"{second_asset} was not found in list of assets issued by user"

    @pytest.mark.regression
    def test_create_location_for_asset(self, api, delete_shipto):
        api.testrail_case_id = 1990

        aa = AssetsApi(api)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 1
        product_dto["assetFlag"] = True

        # create location with asset product
        response_location = setup_location(api, product_dto=product_dto)
        # check assetFlag 
        assert response_location["product"]["assetFlag"] == True, f"Location {response_location['product']['partSku']} does not have asset flag = true"
        aa.check_asset_in_all_assets_list(response_location["product"]["partSku"])

    @pytest.mark.regression
    def test_delete_location_for_asset(self, api, delete_shipto):
        api.testrail_case_id = 1996

        aa = AssetsApi(api)
        la = LocationApi(api)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        # create location with asset product
        response_location = setup_location(api, product_dto=product_dto)
        asset = response_location["product"]["partSku"]
        shipto_id = response_location["shipto_id"]
        location = la.get_location_by_sku(shipto_id, asset)
        location_id = location[0]["id"]

        aa.check_asset_in_all_assets_list(asset)
        la.delete_location(location_id, shipto_id)
        aa.check_asset_in_all_assets_list(asset, should_be=False)

    @pytest.mark.regression
    @pytest.mark.test778
    def test_issue_return_assets_rfid(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1999

        sta = SettingsApi(api)
        ra = RfidApi(api)
        aa = AssetsApi(api)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        #create location of type RFID with asset product
        response_location_rfid = setup_rfid_location(api, number_of_labels=1, product_dto=product_dto)
        asset = response_location_rfid["location"]["product"]["partSku"]
        response_rfid = setup_rfid(api, response_location_rfid["shipto_id"])

        shipto_id = response_location_rfid["shipto_id"]
        location_id = response_location_rfid["location_id"]
        rfid_id = response_rfid["id"]

        rfid_labels = ra.get_rfid_labels(location_id)
        label_id = rfid_labels[0]["id"]
        epc = rfid_labels[0]["labelId"]

        ra.update_rfid_label(location_id, label_id, "AVAILABLE")

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)

        setup_issue_return(api, shipto_id, asset, epc=epc, issue_product=True)
        result_checked_out = aa.check_asset_in_checked_out_list(asset)
        assert result_checked_out["credit"] == product_dto["roundBuy"], f"QTY of cheked out asset is NOT correct"
        assert result_checked_out["location"]["onHandInventory"] == 0, f"OHI of cheked out asset is NOT correct"
        result_all_assets = aa.check_asset_in_all_assets_list(asset)
        assert result_all_assets["onHandInventory"] == 0, f"OHI of cheked out asset is NOT correct"
        rfid_labels = ra.get_rfid_labels(location_id)
        assert rfid_labels[0]["state"] == "ISSUED", f"RFID label has incorrect status {rfid_labels[0]['state']}"

        setup_issue_return(api, shipto_id, asset, epc=epc, return_product=True)
        aa.check_asset_in_checked_out_list(asset, should_be=False)
        #get status of RFID label
        rfid_labels = ra.get_rfid_labels(location_id)
        assert rfid_labels[0]["state"] == "RETURN_CHECK_IN", f"RFID label has incorrect status {rfid_labels[0]['state']}"

    @pytest.mark.regression
    @pytest.mark.test777
    def test_update_asset_location(self, api, delete_shipto):
        api.testrail_case_id = 2008

        aa = AssetsApi(api)
        sta = SettingsApi(api)
        la = LocationApi(api)
        ta = TransactionApi(api)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        # create location with asset product
        response_location = setup_location(api, product_dto=product_dto)
        asset = response_location["product"]["partSku"]
        shipto_id = response_location["shipto_id"]
        max_quantity = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)

        setup_issue_return(api, shipto_id, asset, quantity=max_quantity, issue_product=True)
        location = la.get_location_by_sku(shipto_id, asset)
        assert location[0]["onHandInventory"] == 0, "OHI != 0"
        location_dto = copy.deepcopy(location)
        location_dto[0]["autoSubmit"] = True
        la.update_location(location_dto, shipto_id)
        location = la.get_location_by_sku(shipto_id, asset)
        transaction = ta.get_transaction(sku=asset, shipto_id=shipto_id)
        assert transaction["totalElements"] == 0, f"There should not be transactions with SKU: {asset}"
