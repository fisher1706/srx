from src.api.distributor.product_api import ProductApi
from src.api.setups.setup_product import SetupProduct
import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.customer.assets_page import AssetsPage
from src.api.setups.setup_location import SetupLocation
from src.api.setups.setup_issue_return import setup_issue_return
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
        ui.testrail_case_id = 1991

        lp = LoginPage(ui)
        ap = AssetsPage(ui)

        setup_location = SetupLocation(ui)
        setup_location.setup_product.add_option("asset")
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        #create location with asset product
        asset = response_location["product"]["partSku"]
        shipto_name = response_location["shipto"]["number"]
        shipto_id = response_location["shipto_id"]
        total = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]
        
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
        ui.testrail_case_id = 1993

        lp = LoginPage(ui)
        ap = AssetsPage(ui)
        cha = CheckoutGroupApi(ui)

        setup_location = SetupLocation(ui)
        setup_location.setup_product.add_option("asset")
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        asset = response_location["product"]["partSku"]
        #shipto_name = response_location["shipto"]["number"]
        shipto_id = response_location["shipto_id"]
        total = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        cha.add_shipto_to_checkout_group(shipto_id=shipto_id)

        lp.log_in_customer_portal()
        ap.sidebar_assets()
        # issue 2 assets
        setup_issue_return(ui, shipto_id, asset, quantity=5, issue_product=True, passcode=ui.data.passcode)
        lp.page_refresh()
        lp.wait_until_progress_bar_loaded()
        ap.ping_to_return_last_asset()

    @pytest.mark.regression
    def test_checkout_asset_customer_checkout_user(self, api, delete_shipto):
        api.testrail_case_id = 1995

        aa = AssetsApi(api)
        cha = CheckoutGroupApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("asset")
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")

        #create location with asset product
        first_response_location = setup_location.setup()
        first_asset = first_response_location["product"]["partSku"]
        shipto_id = first_response_location["shipto_id"]

        #create location with asset product
        setup_location.add_option("shipto_id", shipto_id)
        second_response_location = setup_location.setup()
        second_asset = second_response_location["product"]["partSku"]

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

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("asset")
        response_location = setup_location.setup()

        # check assetFlag 
        assert response_location["product"]["assetFlag"], f"Location {response_location['product']['partSku']} does not have asset flag = true"
        aa.check_asset_in_all_assets_list(response_location["product"]["partSku"])

    @pytest.mark.regression
    def test_delete_location_for_asset(self, api, delete_shipto):
        api.testrail_case_id = 1996

        aa = AssetsApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("asset")
        response_location = setup_location.setup()

        asset = response_location["product"]["partSku"]
        shipto_id = response_location["shipto_id"]
        location = la.get_location_by_sku(shipto_id, asset)
        location_id = location[0]["id"]

        aa.check_asset_in_all_assets_list(asset)
        la.delete_location(location_id, shipto_id)
        aa.check_asset_in_all_assets_list(asset, should_be=False)

    @pytest.mark.regression
    def test_issue_return_assets_rfid(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1999

        sta = SettingsApi(api)
        ra = RfidApi(api)
        aa = AssetsApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("asset")
        setup_location.add_option("rfid_location")
        setup_location.add_option("rfid_labels", 1)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        asset = response_location["product"]["partSku"]

        shipto_id = response_location["shipto_id"]
        location_id = response_location["location_id"]
        rfid_id = response_location["rfid"]["id"]

        label_id = response_location["rfid_labels"][0]["rfid_id"]
        epc = response_location["rfid_labels"][0]["label"]

        ra.update_rfid_label(location_id, label_id, "AVAILABLE")

        setup_issue_return(api, shipto_id, asset, epc=epc, issue_product=True)
        result_checked_out = aa.check_asset_in_checked_out_list(asset)
        assert result_checked_out["credit"] == response_location["product"]["roundBuy"], f"QTY of cheked out asset is NOT correct"
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
    def test_update_asset_location(self, api, delete_shipto):
        api.testrail_case_id = 2008

        aa = AssetsApi(api)
        la = LocationApi(api)
        ta = TransactionApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("asset")
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        asset = response_location["product"]["partSku"]
        shipto_id = response_location["shipto_id"]
        max_quantity = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        setup_issue_return(api, shipto_id, asset, quantity=max_quantity, issue_product=True)
        location = la.get_location_by_sku(shipto_id, asset)
        assert location[0]["onHandInventory"] == 0, "OHI != 0"
        location_dto = copy.deepcopy(location)
        location_dto[0]["autoSubmit"] = True
        la.update_location(location_dto, shipto_id)
        location = la.get_location_by_sku(shipto_id, asset)
        transaction = ta.get_transaction(sku=asset, shipto_id=shipto_id)
        assert transaction["totalElements"] == 0, f"There should not be transactions with SKU: {asset}"

    @pytest.mark.parametrize("conditions", [
        {
            "package_conversion": 2,
            "round_buy": 1,
            "issue_quantity": 1,
            "testrail_case_id": 7497
        },
        {
            "package_conversion": 1,
            "round_buy": 2,
            "issue_quantity": 1,
            "testrail_case_id": 7495
        },
        {
            "package_conversion": 1,
            "round_buy": 1,
            "issue_quantity": 2,
            "testrail_case_id": 7496
        }
        ])
    @pytest.mark.regression
    def test_create_asset_product_with_package_conversion_and_round_buy_and_issue_quantity(self, api, conditions):
        api.testrail_case_id = conditions["testrail_case_id"]

        setup_product = SetupProduct(api)
        setup_product.add_option("asset")
        setup_product.add_option("package_conversion", conditions["package_conversion"])
        setup_product.add_option("round_buy", conditions["round_buy"])
        setup_product.add_option("issue_quantity", conditions["issue_quantity"])
        setup_product.setup(expected_status_code=400)

    @pytest.mark.parametrize("conditions", [
        {
            "field": "packageConversion",
            "testrail_case_id": 7500
        },
        {
            "field": "roundBuy",
            "testrail_case_id": 7498
        },
        {
            "field": "issueQuantity",
            "testrail_case_id": 7499
        },
        ])
    @pytest.mark.regression
    def test_update_asset_product_with_package_conversion_and_round_buy_and_issue_quantity(self, conditions, api):
        api.testrail_case_id = conditions["testrail_case_id"]

        pa = ProductApi(api)

        setup_product = SetupProduct(api)
        setup_product.add_option("asset")
        setup_product.add_option("round_buy", 1)
        response_product = setup_product.setup()
        product_id = response_product.pop("id")

        response_product[conditions["field"]] = 2

        pa.update_product(dto=response_product, product_id=product_id, expected_status_code=400)

    @pytest.mark.parametrize("conditions", [
        {
            "field": "packageConversion",
            "testrail_case_id": 7503
        },
        {
            "field": "roundBuy",
            "testrail_case_id": 7501
        },
        {
            "field": "issueQuantity",
            "testrail_case_id": 7502
        }
        ])
    @pytest.mark.regression
    def test_update_asset_product_with_package_conversion_and_round_buy_and_issue_quantity_with_clc(self, api, conditions, delete_customer):
        api.testrail_case_id = conditions["testrail_case_id"]

        pa = ProductApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.setup_customer.add_option("clc", True)
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.setup_product.add_option("asset")
        response_location = setup_location.setup()

        customer_product = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = customer_product.pop("id")
        customer_product[conditions["field"]] = 2

        pa.update_customer_product(dto=customer_product, product_id=product_id, customer_id=response_location["customer_id"], expected_status_code=400)
