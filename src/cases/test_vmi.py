import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.distributor.vmi_page import VmiPage
from src.api.setups.setup_product import SetupProduct
from src.api.setups.setup_shipto import SetupShipto

class TestVmi():
    @pytest.mark.regression
    def test_vmi_list_partial_sku_match(self, ui):
        ui.testrail_case_id = 1838

        lp = LoginPage(ui)
        vp = VmiPage(ui)

        lp.log_in_distributor_portal()

        product_sku = f"{Tools.random_string_u(7)} {Tools.random_string_u(7)}"

        setup_product = SetupProduct(ui)
        setup_product.add_option("sku", product_sku)
        setup_product.setup()

        vp.follow_location_url()
        vp.wait_until_page_loaded()
        vp.click_id(Locator.id_add_button)
        vp.input_data_xpath(product_sku, Locator.xpath_dialog+Locator.xpath_select_box+"//input")
        vp.wait_until_dropdown_list_loaded(1)
        vp.check_found_dropdown_list_item(Locator.xpath_dropdown_list_item, product_sku)

    @pytest.mark.regression
    def test_location_crud(self, ui, delete_shipto):
        ui.testrail_case_id = 2288

        lp = LoginPage(ui)
        vp = VmiPage(ui)
        location_body = vp.location_body.copy()
        edit_location_body = vp.location_body.copy()

        response_product = SetupProduct(ui).setup()
        response_shipto = SetupShipto(ui).setup()

        #-------------------
        location_body["sku"] = response_product["partSku"]
        location_body["orderingConfig.currentInventoryControls.min"] = response_product["roundBuy"]
        location_body["orderingConfig.currentInventoryControls.max"] = response_product["roundBuy"]*3
        location_body["attributeName1"] = "loc1"
        location_body["attributeValue1"] = "loc1"
        location_body["customerSku"] = Tools.random_string_l()
        #-------------------
        edit_location_body["customerSku"] = Tools.random_string_l()
        #-------------------

        lp.log_in_distributor_portal()
        vp.follow_location_url(shipto_id=response_shipto["shipto_id"])
        vp.wait_until_page_loaded()
        vp.create_location(location_body.copy())
        vp.check_last_location(location_body.copy())