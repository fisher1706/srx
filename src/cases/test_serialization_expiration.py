import pytest
import copy
import time
from src.resources.tools import Tools
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.serial_number_api import SerialNumberApi

class TestSerializationExpiration():
    in_3_days_timestamp = (time.time() + 3*24*3600)*1000
    in_4_days_timestamp = (time.time() + 4*24*3600)*1000
    in_7_days_timestamp = (time.time() + 7*24*3600)*1000
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

    @pytest.mark.regression
    def test_no_expiration_alarm_when_update_to_issued(self, api, delete_shipto):
        api.testrail_case_id = 2162

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", {"alarm": 5})
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration": self.in_3_days_timestamp})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"
        assert sn_dto["expirationAlarm"], "Expiration alarm should be present"

        sn_dto["status"] = "ISSUED"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ISSUED"
        assert not sn_dto["expirationAlarm"], "ISSUED Serial Numbers cannot have expiration alarm"

    @pytest.mark.regression
    def test_no_expiration_alarm_when_update_doe(self, api, delete_shipto):
        api.testrail_case_id = 2164

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", {"alarm": 5})
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"
        assert not sn_dto["expirationAlarm"], "Expiration alarm should not be present"

        sn_dto["status"] = "ISSUED"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ISSUED"
        assert not sn_dto["expirationAlarm"], "Expiration alarm should not be present"

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert not sn_dto["expirationAlarm"], "ISSUED Serial Numbers cannot have expiration alarm"
        assert sn_dto["status"] == "ISSUED"

    @pytest.mark.regression
    def test_sn_cannot_be_expired_when_update_doe_without_auto_expire(self, api, delete_shipto):
        api.testrail_case_id = 2165

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", "OFF")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

        sn_dto["status"] = "ISSUED"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ISSUED"

        sn_dto["dateExpiration"] = self.current_date_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ISSUED"

    @pytest.mark.regression
    def test_sn_cannot_be_expired_when_update_doe_with_auto_expire(self, api, delete_shipto):
        api.testrail_case_id = 2166

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", {"expiration": 5})
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

        sn_dto["status"] = "ISSUED"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ISSUED"

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ISSUED"

    @pytest.mark.regression
    def test_sn_cannot_be_expired_when_turn_on_auto_expire(self, api, delete_shipto):
        api.testrail_case_id = 2168

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

        sn_dto["status"] = "ISSUED"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ISSUED"

        sta.set_serialization_settings_shipto(response_location["shipto_id"], expiration=5)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ISSUED"

    @pytest.mark.regression
    def test_return_sn_to_assigned_from_expired_when_update_doe_and_enabled_setting(self, api, delete_shipto):
        api.testrail_case_id = 2170

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", {"expiration": 5})
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sta = SettingsApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration": self.in_3_days_timestamp})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sn_dto["dateExpiration"] = self.in_7_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

    @pytest.mark.regression
    def test_return_sn_to_available_from_expired_when_update_doe_and_enabled_setting(self, api, delete_shipto):
        api.testrail_case_id = 2172

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

        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sn_dto["dateExpiration"] = self.in_7_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

    @pytest.mark.regression
    def test_return_sn_to_assigned_from_expired_when_turn_off_settings(self, api, delete_shipto):
        api.testrail_case_id = 2171

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", {"expiration": 5})
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sta = SettingsApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration": self.in_3_days_timestamp})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sta.set_serialization_settings_shipto(response_location["shipto_id"])

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

    @pytest.mark.regression
    def test_return_sn_to_available_from_expired_when_turn_off_settings(self, api, delete_shipto):
        api.testrail_case_id = 2173

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

        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sta.set_serialization_settings_shipto(response_location["shipto_id"])

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

    @pytest.mark.regression
    def test_return_sn_to_assigned_from_expired_when_update_days_for_settings(self, api, delete_shipto):
        api.testrail_case_id = 2174

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", {"expiration": 5})
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sta = SettingsApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration": self.in_3_days_timestamp})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sta.set_serialization_settings_shipto(response_location["shipto_id"], expiration=1)
        time.sleep(1)
        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

    @pytest.mark.regression
    def test_return_sn_to_available_from_expired_when_turn_off_settings(self, api, delete_shipto):
        api.testrail_case_id = 2173

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

        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sta.set_serialization_settings_shipto(response_location["shipto_id"], expiration=1)
        time.sleep(1)
        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

    @pytest.mark.regression
    def test_no_expiration_alarm_when_update_doe(self, api, delete_shipto):
        api.testrail_case_id = 2176

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_shipto.add_option("serialization_settings", {"alarm": 5})
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sta = SettingsApi(api)
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration": self.in_4_days_timestamp})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["dateExpirationAlarmCountDown"] == 4
        assert sn_dto["expirationAlarm"]

        sta.set_serialization_settings_shipto(response_location["shipto_id"], expiration=1, alarm=5)
        time.sleep(1)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["dateExpirationAlarmCountDown"] == 3
        assert sn_dto["expirationAlarm"]

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["dateExpirationAlarmCountDown"] == 2
        assert sn_dto["expirationAlarm"]

        sta.set_serialization_settings_shipto(response_location["shipto_id"], alarm=5)
        time.sleep(1)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["dateExpirationAlarmCountDown"] == 3
        assert sn_dto["expirationAlarm"]

    @pytest.mark.regression
    def test_return_sn_to_assigned_from_expired_when_turn_on_settings_and_update_doe(self, api, delete_shipto):
        api.testrail_case_id = 2177

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

        sn_dto["dateExpiration"] = self.current_date_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        sta.set_serialization_settings_shipto(response_location["shipto_id"], alarm=3)
        time.sleep(1)

        sn_dto["dateExpiration"] = self.in_3_days_timestamp
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"