import pytest
import copy
from src.api.setups.setup_product import SetupProduct
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.distributor.product_api import ProductApi
from src.api.distributor.settings_api import SettingsApi


class TestSerialization():
    @pytest.mark.regression
    def test_location_of_serialized_product(self, api, delete_shipto):
        api.testrail_case_id = 2028

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
        setup_location.setup_product.add_option("lot")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["lot"] == True, "Location of the serialized product should be serialized"
        assert locations[0]["serialized"] == True, "Location of the serialized product should be serialized"

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = location_id
        location_dto["serialized"] = False
        location_dto["lot"] = False
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["lot"] == True, "Location of the serialized product should be serialized"
        assert locations[0]["serialized"] == True, "Location of the serialized product should be serialized"

    @pytest.mark.regression
    def test_lot_should_be_serializable(self, api):
        api.testrail_case_id = 2029

        setup_product = SetupProduct(api)
        setup_product.add_option("lot")
        setup_product.setup(expected_status_code=400)

    @pytest.mark.regression
    def test_package_conversion_of_serialized_product(self, api):
        api.testrail_case_id = 2031

        setup_product = SetupProduct(api)
        setup_product.add_option("serialized")
        setup_product.add_option("package_conversion", 2)
        setup_product.setup(expected_status_code=400)

    @pytest.mark.regression
    def test_disable_serialization_for_catalog_and_check_location(self, api, delete_shipto):
        api.testrail_case_id = 2032

        la = LocationApi(api)
        pa = ProductApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        products = pa.get_product(response_location["product"]["partSku"])
        assert len(products) == 1
        assert products[0]["serialized"] == True

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["lot"] == False, "Location should not be a lot"
        assert locations[0]["serialized"] == True, "Location of the serialized product should be serialized"

        response_location["product"]["serialized"] = False
        pa.update_product(dto=response_location["product"], product_id=response_location["product"]["id"])

        products = pa.get_product(response_location["product"]["partSku"])
        assert products[0]["serialized"] == False

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["lot"] == False, "Location should not be a lot"
        assert locations[0]["serialized"] == True, "Location should be still serialized after disabling a serialization for the product"

    @pytest.mark.regression
    def test_serialization_default_values(self, api):
        api.testrail_case_id = 2033

        pa = ProductApi(api)

        response_product = SetupProduct(api).setup()

        products = pa.get_product(response_product["partSku"])
        assert products[0]["serialized"] == False
        assert products[0]["lot"] == False

    @pytest.mark.regression
    def test_update_package_conversion_of_serialized_product(self, api):
        api.testrail_case_id = 2034

        pa = ProductApi(api)

        setup_product = SetupProduct(api)
        setup_product.add_option("serialized")
        response_product = setup_product.setup()
        product_id = response_product.pop("id")

        response_product["packageConversion"] = 2

        pa.update_product(dto=response_product, product_id=product_id, expected_status_code=400)

    @pytest.mark.regression
    def test_update_package_conversion_of_product_with_serialized_location(self, api, delete_shipto):
        api.testrail_case_id = 2053

        pa = ProductApi(api)
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        setup_location.add_option("serialized")
        response_location = setup_location.setup()

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
        la.update_location(location_list, response_location["shipto_id"], expected_status_code=400)

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
        la.update_location(location_list, response_location["shipto_id"], expected_status_code=400)

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "OHI of serialized location should not be available for the manually updating"