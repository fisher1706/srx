import pytest
import copy
from src.api.setups.setup_product import SetupProduct
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.distributor.product_api import ProductApi

class TestSerialization():
    @pytest.mark.regression
    def test_location_of_serialized_product(self, api, delete_shipto):
        api.testrail_case_id = 2028

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
        setup_location.setup_product.add_option("lot")
        setup_location.setup_product.add_option("round_buy", 1)
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["lot"], "Location of the serialized product should be serialized"
        assert locations[0]["serialized"], "Location of the serialized product should be serialized"

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = location_id
        location_dto["serialized"] = False
        location_dto["lot"] = False
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["lot"], "Location of the serialized product should be serialized"
        assert locations[0]["serialized"], "Location of the serialized product should be serialized"

    @pytest.mark.regression
    def test_lot_product_should_be_serializable(self, api):
        api.testrail_case_id = 2029

        setup_product = SetupProduct(api)
        setup_product.add_option("lot")
        setup_product.add_option("round_buy", 1)
        setup_product.setup(expected_status_code=400)

    @pytest.mark.regression
    def test_lot_location_should_be_serializable(self, api, delete_shipto):
        api.testrail_case_id = 2082

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("lot")
        setup_location.setup_product.add_option("round_buy", 1)
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["lot"], "Location should be a lot"
        assert locations[0]["serialized"], "Location should be serialized"

    @pytest.mark.parametrize("conditions", [
        {
            "package_conversion": 2,
            "round_buy": 1,
            "testrail_case_id": 2031
        },
        {
            "package_conversion": 1,
            "round_buy": 2,
            "testrail_case_id": 2209
        }
        ])
    @pytest.mark.regression
    def test_package_conversion_and_round_buy_of_serialized_product(self, api, conditions):
        api.testrail_case_id = conditions["testrail_case_id"]

        setup_product = SetupProduct(api)
        setup_product.add_option("serialized")
        setup_product.add_option("package_conversion", conditions["package_conversion"])
        setup_product.add_option("round_buy", conditions["round_buy"])
        setup_product.setup(expected_status_code=400)

    @pytest.mark.parametrize("conditions", [
        {
            "package_conversion": 2,
            "round_buy": 1,
            "testrail_case_id": 2084
        },
        {
            "package_conversion": 1,
            "round_buy": 2,
            "testrail_case_id": 2211
        }
        ])
    @pytest.mark.regression
    def test_package_conversion_and_round_buy_of_serialized_location(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("package_conversion", conditions["package_conversion"])
        setup_location.setup_product.add_option("round_buy", conditions["round_buy"])
        setup_location.setup(expected_status_code=409)

    @pytest.mark.regression
    def test_disable_serialization_for_catalog_and_check_location(self, api, delete_shipto):
        api.testrail_case_id = 2032

        la = LocationApi(api)
        pa = ProductApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", 1)
        response_location = setup_location.setup()

        products = pa.get_product(response_location["product"]["partSku"])
        assert len(products) == 1
        assert products[0]["serialized"]

        locations = la.get_locations(response_location["shipto_id"])
        assert not locations[0]["lot"], "Location should not be a lot"
        assert locations[0]["serialized"], "Location of the serialized product should be serialized"

        response_location["product"]["serialized"] = False
        pa.update_product(dto=response_location["product"], product_id=response_location["product"]["id"])

        products = pa.get_product(response_location["product"]["partSku"])
        assert not products[0]["serialized"]

        locations = la.get_locations(response_location["shipto_id"])
        assert not locations[0]["lot"], "Location should not be a lot"
        assert locations[0]["serialized"], "Location should be still serialized after disabling a serialization for the product"

    @pytest.mark.regression
    def test_serialization_default_product_values(self, api):
        api.testrail_case_id = 2033

        pa = ProductApi(api)

        response_product = SetupProduct(api).setup()

        products = pa.get_product(response_product["partSku"])
        assert not products[0]["serialized"]
        assert not products[0]["lot"]

    @pytest.mark.regression
    def test_serialization_default_location_values(self, api, delete_shipto):
        api.testrail_case_id = 2085

        la = LocationApi(api)

        response_location = SetupLocation(api).setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert not locations[0]["serialized"]
        assert not locations[0]["lot"]

    @pytest.mark.parametrize("conditions", [
        {
            "field": "packageConversion",
            "testrail_case_id": 2034
        },
        {
            "field": "roundBuy",
            "testrail_case_id": 2212
        }
        ])
    @pytest.mark.regression
    def test_update_package_conversion_and_round_buy_of_serialized_product(self, conditions, api):
        api.testrail_case_id = conditions["testrail_case_id"]

        pa = ProductApi(api)

        setup_product = SetupProduct(api)
        setup_product.add_option("serialized")
        setup_product.add_option("round_buy", 1)
        response_product = setup_product.setup()
        product_id = response_product.pop("id")

        response_product[conditions["field"]] = 2

        pa.update_product(dto=response_product, product_id=product_id, expected_status_code=400)

    # @pytest.mark.parametrize("conditions", [
    #     {
    #         "field": "packageConversion",
    #         "testrail_case_id": 6997
    #     },
    #     {
    #         "field": "roundBuy",
    #         "testrail_case_id": 6998
    #     }
    #     ])
    # @pytest.mark.regression
    # def test_update_package_conversion_and_round_buy_of_serialized_product_with_clc(self, conditions, api):
    #     api.testrail_case_id = conditions["testrail_case_id"]

    #     pa = ProductApi(api)

    #     setup_product = SetupProduct(api)
    #     setup_product.add_option("serialized")
    #     setup_product.add_option("round_buy", 1)
    #     response_product = setup_product.setup()
    #     product_id = response_product.pop("id")

    #     response_product[conditions["field"]] = 2

    #     pa.update_product(dto=response_product, product_id=product_id, expected_status_code=400)

    @pytest.mark.parametrize("conditions", [
        {
            "field": "packageConversion",
            "testrail_case_id": 2053
        },
        {
            "field": "roundBuy",
            "testrail_case_id": 2213
        }
        ])
    @pytest.mark.regression
    def test_update_package_conversion_and_round_buy_of_product_with_serialized_location(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        pa = ProductApi(api)
        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.add_option("serialized")
        response_location = setup_location.setup()

        response_product = response_location["product"]
        product_id = response_product.pop("id")

        response_product[conditions["field"]] = 2

        pa.update_product(dto=response_product, product_id=product_id, expected_status_code=400)

    @pytest.mark.parametrize("conditions", [
        {
            "field": "packageConversion",
            "testrail_case_id": 7001
        },
        {
            "field": "roundBuy",
            "testrail_case_id": 7003
        }
        ])
    @pytest.mark.regression
    def test_update_package_conversion_and_round_buy_of_product_with_serialized_location_with_clc(self, api, conditions, delete_customer):
        api.testrail_case_id = conditions["testrail_case_id"]

        pa = ProductApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.setup_customer.add_option("clc", True)
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.add_option("serialized")
        response_location = setup_location.setup()

        customer_product = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = customer_product.pop("id")
        customer_product[conditions["field"]] = 2

        pa.update_customer_product(dto=customer_product, product_id=product_id, customer_id=response_location["customer_id"], expected_status_code=400)

    @pytest.mark.regression
    def test_ohi_of_created_serialized_product_location(self, api, delete_shipto):
        api.testrail_case_id = 2035

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.add_option("ohi", 10)
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["serialized"], "Location should be serialized"
        assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

    @pytest.mark.regression
    def test_ohi_of_created_serialized_location(self, api, delete_shipto):
        api.testrail_case_id = 2049

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.add_option("ohi", 10)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

    @pytest.mark.regression
    def test_ohi_location_updated_to_serialized(self, api, delete_shipto):
        api.testrail_case_id = 2036

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.add_option("ohi", 10)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        response_location = setup_location.setup()

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location_dto["serialized"] = True
        location_dto["id"] = location_id
        la.update_location([location_dto],response_location["shipto_id"])           
      
        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["serialized"], "Location should be serialized"
        assert locations[0]["onHandInventory"] == 0, "OHI should becomes equal to 0 after updating location to serialized"

    @pytest.mark.regression
    def test_ohi_product_location_updated_to_serialized(self, api, delete_shipto):
        api.testrail_case_id = 2052

        la = LocationApi(api)
        pa = ProductApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("ohi", 10)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.setup_product.add_option("round_buy", 1)
        response_location = setup_location.setup()

        response_product = response_location["product"]
        product_id = response_product.pop("id")

        response_product["serialized"] = True

        pa.update_product(dto=response_product, product_id=product_id)

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["serialized"], "Location should be serialized"
        assert locations[0]["onHandInventory"] == 0, "OHI should becomes equal to 0 after updating product to serialized"

    @pytest.mark.regression
    def test_ohi_of_serialized_asset_product_location(self, api, delete_shipto):
        api.testrail_case_id = 2037

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
        setup_location.setup_product.add_option("asset")
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.add_option("ohi", 10)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

    @pytest.mark.regression
    def test_ohi_of_serialized_asset_location(self, api, delete_shipto):
        api.testrail_case_id = 2050

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("asset")
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.add_option("ohi", 10)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

    @pytest.mark.regression
    def test_ohi_of_updated_serialized_product_location(self, api, delete_shipto):
        api.testrail_case_id = 2038

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        response_location = setup_location.setup()

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location_dto["id"] = location_id
        location_dto["onHandInventory"] = 10
        la.update_location([location_dto],response_location["shipto_id"])           

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "OHI of serialized location should not be available for the manually updating"

    @pytest.mark.regression
    def test_ohi_of_updated_serialized_location(self, api, delete_shipto):
        api.testrail_case_id = 2051

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", 1)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        response_location = setup_location.setup()

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location_dto["id"] = location_id
        location_dto["onHandInventory"] = 10
        la.update_location([location_dto],response_location["shipto_id"])

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "OHI of serialized location should not be available for the manually updating"

    @pytest.mark.parametrize("conditions", [
        {
            "package_conversion": 2,
            "round_buy": 1,
            "testrail_case_id": 2214
        },
        {
            "package_conversion": 1,
            "round_buy": 2,
            "testrail_case_id": 2086
        }
        ])
    @pytest.mark.regression
    def test_update_location_to_serialized_with_package_conversion_and_round_buy(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("round_buy", conditions["round_buy"])
        setup_location.setup_product.add_option("package_conversion", conditions["package_conversion"])
        response_location = setup_location.setup()

        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = response_location["location_id"]
        location_dto["serialized"] = True
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"], expected_status_code=409)

    @pytest.mark.parametrize("conditions", [
        {
            "package_conversion": 2,
            "round_buy": 1,
            "testrail_case_id": 6999
        },
        {
            "package_conversion": 1,
            "round_buy": 2,
            "testrail_case_id": 7000
        }
        ])
    @pytest.mark.regression
    def test_update_location_to_serialized_with_package_conversion_and_round_buy_with_clc(self, api, conditions, delete_customer):
        api.testrail_case_id = conditions["testrail_case_id"]

        la = LocationApi(api)
        pa = ProductApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.setup_customer.add_option("clc", True)
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_product.add_option("round_buy", 1)
        response_location = setup_location.setup()

        customer_product = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = customer_product.pop("id")
        customer_product["packageConversion"] = conditions["package_conversion"]
        customer_product["roundBuy"] = conditions["round_buy"]
        pa.update_customer_product(dto=customer_product, product_id=product_id, customer_id=response_location["customer_id"])

        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = response_location["location_id"]
        location_dto["serialized"] = True
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"], expected_status_code=409, customer_id=response_location["customer_id"])