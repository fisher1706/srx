import pytest
import copy
from src.api.setups.setup_product import setup_product
from src.api.setups.setup_location import setup_location
from src.api.distributor.location_api import LocationApi
from src.api.distributor.product_api import ProductApi

class TestSerialization():
    @pytest.mark.regression
    def test_location_of_serialized_product(self, api, delete_shipto):
        api.testrail_case_id = 2028

        la = LocationApi(api)

        response_product = setup_product(api, is_serialized=True, is_lot=True)
        response_location = setup_location(api, response_product=response_product, checkout_settings_shipto="DEFAULT")

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

        setup_product(api, is_lot=True, expected_status_code=400)

    @pytest.mark.regression
    def test_lot_location_should_be_serializable(self, api, delete_shipto):
        api.testrail_case_id = 2082

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("lot")
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["lot"], "Location should be a lot"
        assert locations[0]["serialized"], "Location should be serialized"

    @pytest.mark.regression
    def test_package_conversion_of_serialized_product(self, api):
        api.testrail_case_id = 2031

        setup_product(api, is_serialized=True, package_conversion=2, expected_status_code=400)

    @pytest.mark.regression
    def test_package_conversion_of_serialized_location(self, api, delete_shipto):
        api.testrail_case_id = 2084

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("package_conversion", 2)
        setup_location.setup(expected_status_code=409)

    @pytest.mark.regression
    def test_disable_serialization_for_catalog_and_check_location(self, api, delete_shipto):
        api.testrail_case_id = 2032

        la = LocationApi(api)
        pa = ProductApi(api)

        response_product = setup_product(api, is_serialized=True)
        response_location = setup_location(api, response_product=response_product, checkout_settings_shipto="DEFAULT")
        product_id = response_product.pop("id")

        products = pa.get_product(response_product["partSku"])
        assert len(products) == 1
        assert products[0]["serialized"]

        locations = la.get_locations(response_location["shipto_id"])
        assert not locations[0]["lot"], "Location should not be a lot"
        assert locations[0]["serialized"], "Location of the serialized product should be serialized"

        response_product["serialized"] = False
        pa.update_product(dto=response_product, product_id=product_id)

        products = pa.get_product(response_location["product"]["partSku"])
        assert not products[0]["serialized"]

        locations = la.get_locations(response_location["shipto_id"])
        assert not locations[0]["lot"], "Location should not be a lot"
        assert locations[0]["serialized"], "Location should be still serialized after disabling a serialization for the product"

    @pytest.mark.regression
    def test_serialization_default_product_values(self, api):
        api.testrail_case_id = 2033

        pa = ProductApi(api)

        response_product = setup_product(api)

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

    @pytest.mark.regression
    def test_update_package_conversion_of_serialized_product(self, api):
        api.testrail_case_id = 2034

        pa = ProductApi(api)

        response_product = setup_product(api, is_serialized=True)
        product_id = response_product.pop("id")

        response_product["packageConversion"] = 2

        pa.update_product(dto=response_product, product_id=product_id, expected_status_code=400)

    @pytest.mark.regression
    def test_update_package_conversion_of_location_with_serialized_product(self, api, delete_shipto):
        api.testrail_case_id = 2053

        pa = ProductApi(api)

        response_location = setup_location(api, is_serialized=True, checkout_settings_shipto="DEFAULT")

        response_product = response_location["product"]
        product_id = response_product.pop("id")

        response_product["packageConversion"] = 2

        pa.update_product(dto=response_product, product_id=product_id, expected_status_code=400)

    @pytest.mark.regression
    def test_ohi_of_created_serialized_product_location(self, api, delete_shipto):
        api.testrail_case_id = 2035

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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
        setup_location.add_option("ohi", 10)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

    @pytest.mark.regression
    def test_ohi_location_updated_to_serialized(self, api, delete_shipto):
        api.testrail_case_id = 2036

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("ohi", 10)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = location_id
        location_dto["serialized"] = True
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])

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
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

    @pytest.mark.regression
    def test_ohi_of_updated_serialized_product_location(self, api, delete_shipto):
        api.testrail_case_id = 2038

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = location_id
        location_dto["onHandInventory"] = 10
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "OHI of serialized location should not be available for the manually updating"

    @pytest.mark.regression
    def test_ohi_of_updated_serialized_location(self, api, delete_shipto):
        api.testrail_case_id = 2051

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = location_id
        location_dto["onHandInventory"] = 10
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "OHI of serialized location should not be available for the manually updating"

    def test_update_location_to_serialized_with_package_conversion(self, api, delete_shipto):
        api.testrail_case_id = 2086

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        setup_location.setup_product.add_option("package_conversion", 2)
        response_location = setup_location.setup()

        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = response_location["location_id"]
        location_dto["serialized"] = True
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"], expected_status_code=409)