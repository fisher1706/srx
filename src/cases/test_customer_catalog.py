import pytest
import copy
from src.resources.tools import Tools
from src.api.distributor.settings_api import SettingsApi
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

    @pytest.mark.regression
    def test_cannot_create_location_with_incorrect_min_max_with_clc(self, api, delete_customer):
        api.testrail_case_id = 7521

        la = LocationApi(api)
        pa = ProductApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("round_buy", 10)
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_shipto.setup_customer.add_option("clc")
        setup_location.add_option("min", 1)
        setup_location.add_option("max", 11)
        response_location = setup_location.setup()

        la.delete_location(response_location["location_id"], response_location["shipto_id"], customer_id=response_location["customer_id"])
        customer_product = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = customer_product.pop("id")
        customer_product["roundBuy"] = 11
        pa.update_customer_product(customer_product, product_id, customer_id=response_location["customer_id"])

        location_dto = Tools.get_dto("location_dto.json")
        location_dto["attributeName1"] = "loc1"
        location_dto["attributeValue1"] = "loc1"
        location_dto["orderingConfig"] = {
            "product": {
                "partSku": response_location["product"]["partSku"]
            },
            "type": "LABEL",
            "currentInventoryControls": {
                "min": 1,
                "max": 10
            }
        }
        location_list = [copy.deepcopy(location_dto)]
        la.create_location(location_list, response_location["shipto_id"], customer_id=response_location["customer_id"], expected_status_code=409)

    @pytest.mark.regression
    def test_cannot_update_customer_product_round_buy_with_incorrect_min_max(self, api, delete_customer):
        api.testrail_case_id = 7523

        pa = ProductApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("round_buy", 10)
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_shipto.setup_customer.add_option("clc")
        # setup_location.add_option("min", 1)
        # setup_location.add_option("max", 11)
        setup_location.set_options({"min": 1, "max": 11})
        response_location = setup_location.setup()

        customer_product = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = customer_product.pop("id")
        customer_product["roundBuy"] = 11
        pa.update_customer_product(customer_product, product_id, customer_id=response_location["customer_id"], expected_status_code=400)

    @pytest.mark.regression
    def test_update_distributor_product_round_by_when_incorrect_min_max_with_clc(self, api, delete_customer):
        api.testrail_case_id = 7524

        pa = ProductApi(api)
        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("round_buy", 10)
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_shipto.setup_customer.add_option("clc")
        setup_location.set_options({"min": 1, "max": 11})
        response_location = setup_location.setup()

        response_product = response_location["product"]
        product_id = response_product.pop("id")

        response_product["roundBuy"] = 2

        pa.update_product(dto=response_product, product_id=product_id)