import pytest
import copy
from src.resources.tools import Tools
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.distributor.serial_number_api import SerialNumberApi

class TestSerializationSN():
    @pytest.mark.regression
    def test_cannot_create_sn_for_not_serialized_location(self, api, delete_shipto):
        api.testrail_case_id = 2105

        response_location = SetupLocation(api).setup()

        sna = SerialNumberApi(api)

        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], Tools.random_string_u(), expected_status_code=400)

    def test_cannot_create_2_same_SNs(self, api, delete_shipto):
        api.testrail_case_id = 2117
        
        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        response_location_1 = setup_location.setup()

        setup_location.add_option("product", response_location_1["product"])
        response_location_2 = setup_location.setup()

        sna = SerialNumberApi(api)

        sn = Tools.random_string_u()

        sna.create_serial_number(response_location_1["location_id"], response_location_1["shipto_id"], sn)
        sna.create_serial_number(response_location_2["location_id"], response_location_2["shipto_id"], sn, expected_status_code=400)

    def test_ohi_serialized_location_equal_to_sn_in_available_status(self, api, delete_shipto):
        api.testrail_case_id = 2106

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        la = LocationApi(api)

        sn = Tools.random_string_u()

        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 1
