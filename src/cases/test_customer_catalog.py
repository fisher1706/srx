from src.api.distributor.settings_api import SettingsApi
from src.resources.tools import Tools
import pytest
from src.api.setups.setup_product import SetupProduct
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.distributor.product_api import ProductApi

class TestCustomerCatalog():
    @pytest.mark.regression
    def test_csku_is_copied_into_clc_after_clc_on(self, api, delete_customer):
        api.testrail_case_id = 7494

        pa = ProductApi(api)
        sa = SettingsApi(api)
        csku = Tools.random_string_u(10)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.setup_customer.add_option("clc", False)
        setup_location.setup_shipto.add_option("customer")
        setup_location.add_option("customer_sku", csku)
        response_location = setup_location.setup()

        sa.set_customer_level_catalog_flag(True, response_location["customer_id"])

        product = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        assert product["customerSku"] == csku