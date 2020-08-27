import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.distributor.vmi_page import VmiPage
from src.api.setups.setup_product import SetupProduct

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
