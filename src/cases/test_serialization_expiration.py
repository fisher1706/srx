import pytest
import copy
import time
from src.resources.tools import Tools
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.serial_number_api import SerialNumberApi

class TestSerializationExpiration():
    in_3_days_timestamp = (time.time() + 3*24*3600)*1000
    current_date_timestamp = time.time()*1000

    @pytest.mark.regression
    def test_sn_expires_when_enable_auto_expire(self, api, delete_shipto):
        api.testrail_case_id = 2146

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", "OFF")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sta = SettingsApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration": self.in_3_days_timestamp})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

        sta.set_serialization_settings_shipto(response_location["shipto_id"], expiration=5)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

    @pytest.mark.regression
    def test_sn_created_in_expired_status_when_auto_expire_enabled(self, api, delete_shipto):
        api.testrail_case_id = 2147

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", {"expiration": 5})
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration": self.in_3_days_timestamp})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

    @pytest.mark.regression
    def test_sn_expires_when_update_doe_if_auto_expire_enabled(self, api, delete_shipto):
        api.testrail_case_id = 2148

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", {"expiration": 5})
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sta = SettingsApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

    @pytest.mark.regression
    def test_create_sn_in_expired_status_without_settings(self, api, delete_shipto):
        api.testrail_case_id = 2154

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", "OFF")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration": self.current_date_timestamp})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

    @pytest.mark.regression
    def test_update_sn_to_expired_status_without_settings(self, api, delete_shipto):
        api.testrail_case_id = 2157

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", "OFF")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto["dateExpiration"] = self.current_date_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

    @pytest.mark.regression
    def test_return_sn_to_assigned_from_expired_when_create_in_expired_and_disabled_setting(self, api, delete_shipto):
        api.testrail_case_id = 2155

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", "OFF")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration":self.current_date_timestamp})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

    @pytest.mark.regression
    def test_return_sn_to_assigned_from_expired_when_create_in_assigned_and_disabled_setting(self, api, delete_shipto):
        api.testrail_case_id = 2156

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", "OFF")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

        sn_dto["dateExpiration"] = self.current_date_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

    @pytest.mark.regression
    def test_return_sn_to_available_from_expired_when_disabled_setting(self, api, delete_shipto):
        api.testrail_case_id = 2158

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", "OFF")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"
        
        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

        sn_dto["dateExpiration"] = self.current_date_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

