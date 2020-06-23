import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.distributor.vmi_page import VmiPage
from src.api.setups.setup_product import setup_product
from src.api.setups.setup_shipto import setup_shipto

class TestVmi():
    @pytest.mark.regression
    def test_vmi_list_partial_sku_match(self, ui, delete_shipto):
        ui.testrail_case_id = 1838

        lp = LoginPage(ui)
        vp = VmiPage(ui)

        lp.log_in_distributor_portal()

        response_shipto = setup_shipto(ui)
        
        product_sku = f"{Tools.random_string_u(7)} {Tools.random_string_u(7)}"
        setup_product(ui, sku=product_sku)


        vp.follow_location_url()
        vp.click_id(Locator.id_add_button)
        vp.input_data_xpath(product_sku, Locator.xpath_dialog+Locator.xpath_select_box+"//input")
        vp.wait_until_dropdown_list_loaded(1)
        vp.check_found_dropdown_list_item(Locator.xpath_dropdown_list_item, product_sku)
