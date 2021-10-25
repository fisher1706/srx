import time
import pytest
from src.resources.tools import Tools
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.serial_number_api import SerialNumberApi

in_3_days_timestamp = (time.time() + 3*24*3600)*1000
in_4_days_timestamp = (time.time() + 4*24*3600)*1000
in_7_days_timestamp = (time.time() + 7*24*3600)*1000
current_date_timestamp = time.time()*1000

@pytest.mark.regression
def test_sn_expires_when_enable_auto_expire(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2146

    preset = serialized_location_preset(api, serialization_settings="OFF")

    sna = SerialNumberApi(api)
    sta = SettingsApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": in_3_days_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sta.set_serialization_settings_shipto(preset["shipto_id"], expiration=5, sleep=3)
    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

@pytest.mark.regression
def test_sn_created_in_expired_status_when_auto_expire_enabled(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2147

    preset = serialized_location_preset(api, serialization_settings={"expiration": 5})

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": in_3_days_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

@pytest.mark.regression
def test_sn_expires_when_update_doe_if_auto_expire_enabled(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2148

    preset = serialized_location_preset(api, serialization_settings={"expiration": 5})

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["dateExpiration"] = in_3_days_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

@pytest.mark.regression
def test_create_sn_in_expired_status_without_settings(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2154

    preset = serialized_location_preset(api, serialization_settings="OFF")

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": current_date_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

@pytest.mark.regression
def test_update_sn_to_expired_status_without_settings(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2157

    preset = serialized_location_preset(api, serialization_settings="OFF")

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    sn_dto["dateExpiration"] = current_date_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

@pytest.mark.parametrize("conditions", [
    {
        "doe": in_3_days_timestamp,
        "testrail_case_id": 2155
    },
    {
        "doe": None,
        "testrail_case_id": 2216
    }
    ])
@pytest.mark.regression
def test_return_sn_to_assigned_from_expired_when_create_in_expired_and_disabled_setting(api, serialized_location_preset, conditions, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    preset = serialized_location_preset(api, serialization_settings="OFF")

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration":current_date_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sn_dto["dateExpiration"] = conditions["doe"]
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

@pytest.mark.regression
def test_return_sn_to_assigned_from_expired_when_create_in_assigned_and_disabled_setting(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2156

    preset = serialized_location_preset(api, serialization_settings="OFF")

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["dateExpiration"] = current_date_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sn_dto["dateExpiration"] = in_3_days_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

@pytest.mark.parametrize("conditions", [
    {
        "doe": in_3_days_timestamp,
        "testrail_case_id": 2158
    },
    {
        "doe": None,
        "testrail_case_id": 2217
    }
    ])
@pytest.mark.regression
def test_return_sn_to_available_from_expired_when_disabled_setting(api, serialized_location_preset, conditions, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    preset = serialized_location_preset(api, serialization_settings="OFF")

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

    sn_dto["dateExpiration"] = current_date_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sn_dto["dateExpiration"] = conditions["doe"]
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

@pytest.mark.parametrize("conditions", [
    {
        "status": "ISSUED",
        "testrail_case_id": 2162
    },
    {
        "status": "DISPOSED",
        "testrail_case_id": 2191
    }
    ])
@pytest.mark.regression
def test_no_expiration_alarm_when_update_to_issued(api, conditions, serialized_location_preset, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    preset = serialized_location_preset(api, serialization_settings={"alarm": 5})

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": in_3_days_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"
    assert sn_dto["expirationAlarm"], "Expiration alarm should be present"

    sn_dto["status"] = conditions["status"]
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == conditions["status"]
    assert not sn_dto["expirationAlarm"], f"{conditions['status']} Serial Numbers cannot have expiration alarm"

@pytest.mark.parametrize("conditions", [
    {
        "status": "ISSUED",
        "testrail_case_id": 2164
    },
    {
        "status": "DISPOSED",
        "testrail_case_id": 2194
    }
    ])
@pytest.mark.regression
def test_no_expiration_alarm_when_update_doe(api, conditions, serialized_location_preset, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    preset = serialized_location_preset(api, serialization_settings={"alarm": 5})

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"
    assert not sn_dto["expirationAlarm"], "Expiration alarm should not be present"

    sn_dto["status"] = conditions["status"]
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == conditions["status"]
    assert not sn_dto["expirationAlarm"], "Expiration alarm should not be present"

    sn_dto["dateExpiration"] = in_3_days_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert not sn_dto["expirationAlarm"], f"{conditions['status']} Serial Numbers cannot have expiration alarm"
    assert sn_dto["status"] == conditions["status"]

@pytest.mark.parametrize("conditions", [
    {
        "status": "ISSUED",
        "testrail_case_id": 2165
    },
    {
        "status": "DISPOSED",
        "testrail_case_id": 2195
    }
    ])
@pytest.mark.regression
def test_issued_sn_cannot_be_expired_when_update_doe_without_auto_expire(conditions, serialized_location_preset, api, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    preset = serialized_location_preset(api, serialization_settings="OFF")

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["status"] = conditions["status"]
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == conditions["status"]

    sn_dto["dateExpiration"] = current_date_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == conditions["status"]

@pytest.mark.parametrize("conditions", [
    {
        "status": "ISSUED",
        "testrail_case_id": 2166
    },
    {
        "status": "DISPOSED",
        "testrail_case_id": 2196
    }
    ])
@pytest.mark.regression
def test_issued_sn_cannot_be_expired_when_update_doe_with_auto_expire(conditions, api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    preset = serialized_location_preset(api, serialization_settings={"expiration": 5})

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["status"] = conditions["status"]
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == conditions["status"]

    sn_dto["dateExpiration"] = in_3_days_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == conditions["status"]

@pytest.mark.parametrize("conditions", [
    {
        "status": "ISSUED",
        "testrail_case_id": 2168
    },
    {
        "status": "DISPOSED",
        "testrail_case_id": 2197
    }
    ])
@pytest.mark.regression
def test_issued_sn_cannot_be_expired_when_turn_on_auto_expire(conditions, api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    preset = serialized_location_preset(api, serialization_settings="OFF")

    sna = SerialNumberApi(api)
    sta = SettingsApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": in_3_days_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["status"] = conditions["status"]
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == conditions["status"]

    sta.set_serialization_settings_shipto(preset["shipto_id"], expiration=5, sleep=3)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == conditions["status"]

@pytest.mark.parametrize("conditions", [
    {
        "doe": in_7_days_timestamp,
        "testrail_case_id": 2170
    },
    {
        "doe": None,
        "testrail_case_id": 2218
    }
    ])
@pytest.mark.regression
def test_return_sn_to_assigned_from_expired_when_update_doe_and_enabled_setting(api, conditions, serialized_location_preset, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    preset = serialized_location_preset(api, serialization_settings={"expiration": 5})

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": in_3_days_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sn_dto["dateExpiration"] = conditions["doe"]
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

@pytest.mark.regression
def test_return_sn_to_available_from_expired_when_update_doe_and_enabled_setting(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2172

    preset = serialized_location_preset(api, serialization_settings={"expiration": 5})

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

    sn_dto["dateExpiration"] = in_3_days_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sn_dto["dateExpiration"] = in_7_days_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

@pytest.mark.regression
def test_return_sn_to_assigned_from_expired_when_turn_off_settings(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2171

    preset = serialized_location_preset(api, serialization_settings={"expiration": 5})

    sna = SerialNumberApi(api)
    sta = SettingsApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": in_3_days_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sta.set_serialization_settings_shipto(preset["shipto_id"], sleep=3)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

@pytest.mark.regression
def test_return_sn_to_available_from_expired_when_turn_off_settings(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2173

    preset = serialized_location_preset(api, serialization_settings={"expiration": 5})

    sna = SerialNumberApi(api)
    sta = SettingsApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

    sn_dto["dateExpiration"] = in_3_days_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sta.set_serialization_settings_shipto(preset["shipto_id"], sleep=3)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

@pytest.mark.regression
def test_return_sn_to_assigned_from_expired_when_update_days_for_settings(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2174

    preset = serialized_location_preset(api, serialization_settings={"expiration": 5})

    sna = SerialNumberApi(api)
    sta = SettingsApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": in_3_days_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sta.set_serialization_settings_shipto(preset["shipto_id"], expiration=1, sleep=3)
    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

@pytest.mark.regression
def test_return_sn_to_available_from_expired_when_update_days_for_settings(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2175

    preset = serialized_location_preset(api, serialization_settings={"expiration": 5})

    sna = SerialNumberApi(api)
    sta = SettingsApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

    sn_dto["dateExpiration"] = in_3_days_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sta.set_serialization_settings_shipto(preset["shipto_id"], expiration=1, sleep=3)
    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

@pytest.mark.regression
def test_full_expire_in_alarm_flow(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2176

    preset = serialized_location_preset(api, serialization_settings={"alarm": 5})

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    sta = SettingsApi(api)
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": in_4_days_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["dateExpirationAlarmCountDown"] == 4
    assert sn_dto["expirationAlarm"]

    sta.set_serialization_settings_shipto(preset["shipto_id"], expiration=1, alarm=5, sleep=3)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["dateExpirationAlarmCountDown"] == 3
    assert sn_dto["expirationAlarm"]

    sn_dto["dateExpiration"] = in_3_days_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["dateExpirationAlarmCountDown"] == 2
    assert sn_dto["expirationAlarm"]

    sta.set_serialization_settings_shipto(preset["shipto_id"], alarm=5, sleep=3)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["dateExpirationAlarmCountDown"] == 3
    assert sn_dto["expirationAlarm"]

@pytest.mark.regression
def test_return_sn_to_assigned_from_expired_when_turn_on_settings_and_update_doe(api, serialized_location_preset, delete_shipto):
    api.testrail_case_id = 2177

    preset = serialized_location_preset(api, serialization_settings="OFF")

    sna = SerialNumberApi(api)
    sta = SettingsApi(api)
    sn = Tools.random_string_u()
    sna.create_serial_number(preset["location_id"], preset["shipto_id"], sn, additional_options={"dateExpiration": in_3_days_timestamp})

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

    sn_dto["dateExpiration"] = current_date_timestamp
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    sta.set_serialization_settings_shipto(preset["shipto_id"], alarm=3)

    sn_dto["dateExpiration"] = in_3_days_timestamp
    sna.update_serial_number(sn_dto)
    time.sleep(5)

    sn_dto = sna.get_serial_number(shipto_id=preset["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"
