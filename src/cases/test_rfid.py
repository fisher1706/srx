import pytest
from src.resources.locator import Locator
from src.resources.tools import Tools
from src.resources.permissions import Permissions
from src.pages.general.login_page import LoginPage
from src.pages.distributor.rfid_page import RfidPage
from src.api.setups.setup_location import SetupLocation
from src.api.setups.setup_rfid import SetupRfid
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.settings_api import SettingsApi

class TestRfid():
    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": 1918
        },
        { 
            "user": Permissions.rfids("EDIT"),
            "testrail_case_id": 2245
        }
        ])
    @pytest.mark.acl
    @pytest.mark.regression
    def test_rfid_label_crud(self, ui, permission_ui, permissions, delete_shipto, delete_distributor_security_group):
        ui.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

        lp = LoginPage(context)
        rp = RfidPage(context)

        setup_location = SetupLocation(ui)
        setup_location.add_option("type", "RFID")
        response_location = setup_location.setup()

        shipto_text = f"{context.data.customer_name} - {response_location['shipto']['number']}"
        product_sku = response_location["product"]["partSku"]

        lp.log_in_distributor_portal()
        rp.sidebar_rfid()
        rp.select_shipto_sku(shipto_text, product_sku)
        rfid_label = rp.add_rfid_label()
        rp.check_last_rfid_label(rfid_label, "ASSIGNED")
        rp.update_last_rfid_label_status("ISSUED")
        rp.should_be_disabled_xpath(Locator.xpath_by_count(Locator.xpath_unassign_button, rp.get_table_rows_number()))
        new_status = "AVAILABLE"
        rp.page_refresh()
        rp.select_shipto_sku(shipto_text, product_sku)
        rp.update_last_rfid_label_status(new_status)
        rp.check_last_rfid_label(rfid_label, new_status)
        rp.unassign_last_rfid_label()

    @pytest.mark.acl
    @pytest.mark.regression
    def test_rfid_crud_view_permission(self, api, permission_api, delete_distributor_security_group, delete_shipto):
        api.testrail_case_id = 2261

        Permissions.set_configured_user(api, Permissions.rfids("VIEW"))

        ra = RfidApi(permission_api)

        setup_location = SetupLocation(api)
        setup_location.add_option("type", "RFID")
        response_location = setup_location.setup()

        ra.create_rfid(response_location["location_id"], expected_status_code=400) #cannot create RFID label

        rfid_info = RfidApi(api).create_rfid(response_location["location_id"])
        rfid = ra.get_rfid_labels(response_location["location_id"])[0] #can read RFID labels
        assert rfid_info["label"] == rfid["labelId"] #--//--//--

        ra.update_rfid_label(response_location["location_id"], rfid_info["rfid_id"], "AVAILABLE", expected_status_code=400) #cannot update RFID label
        ra.delete_rfid_label(response_location["location_id"], rfid_info["rfid_id"], expected_status_code=400) #cannot delete RFID label

    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": 2243
        },
        { 
            "user": Permissions.rfids("EDIT"),
            "testrail_case_id": 2244
        }
        ])
    @pytest.mark.acl
    @pytest.mark.regression
    def test_rfid_label_import_as_available(self, ui, permission_ui, permissions, delete_shipto, delete_distributor_security_group):
        ui.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

        lp = LoginPage(context)
        rp = RfidPage(context)

        setup_location = SetupLocation(ui)
        setup_location.add_option("type", "RFID")
        response_location = setup_location.setup()

        shipto_text = f"{context.data.customer_name} - {response_location['shipto']['number']}"
        product_sku = response_location["product"]["partSku"]
        rfid = Tools.random_string_u()
        rfids = [
            [rfid, product_sku, None]
        ]
        lp.log_in_distributor_portal()
        rp.sidebar_rfid()
        rp.select_shipto_sku(shipto_text, product_sku)
        rp.import_rfid_as_available(rfids)
        rp.check_last_rfid_label(rfid, "AVAILABLE")

    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": 2254
        },
        { 
            "user": Permissions.rfids("EDIT"),
            "testrail_case_id": 2255
        }
        ])
    @pytest.mark.acl
    @pytest.mark.regression
    def test_rfid_label_import_csv(self, ui, permission_ui, permissions, delete_shipto, delete_distributor_security_group):
        ui.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

        lp = LoginPage(context)
        rp = RfidPage(context)

        setup_location = SetupLocation(ui)
        setup_location.add_option("type", "RFID")
        response_location = setup_location.setup()

        shipto_text = f"{context.data.customer_name} - {response_location['shipto']['number']}"
        product_sku = response_location["product"]["partSku"]
        rfid = Tools.random_string_u()
        rfids = [
            [rfid]
        ]
        lp.log_in_distributor_portal()
        rp.sidebar_rfid()
        rp.select_shipto_sku(shipto_text, product_sku)
        rp.import_rfid(rfids)
        rp.check_last_rfid_label(rfid, "ASSIGNED")

    @pytest.mark.regression
    def test_create_rfid_transaction_as_issued(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1914

        ra = RfidApi(api)
        sta = SettingsApi(api)
        ta = TransactionApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("rfid_location")
        setup_location.add_option("rfid_labels", 3)
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": False})
        response_location = setup_location.setup()
        
        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][0]["rfid_id"], "AVAILABLE")
        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][1]["rfid_id"], "AVAILABLE")
        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][2]["rfid_id"], "AVAILABLE")

        sta.set_reorder_controls_settings_for_shipto(response_location["shipto_id"], reorder_controls="ISSUED")

        ra.rfid_issue(response_location["rfid"]["value"], response_location["rfid_labels"][0]["label"])

        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])
        transaction_count = transaction["totalElements"]
        assert transaction_count == 1, "The number of transactions should be equal to 1"
        assert transaction["entities"][0]["reorderQuantity"] == response_location["product"]["roundBuy"], f"Reorder quantity of transaction should be equal to {response_location['product']['roundBuy']}"
        assert transaction["entities"][0]["product"]["partSku"] == response_location["product"]["partSku"]

    @pytest.mark.regression
    def test_create_rfid_transaction_at_min(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1913

        ra = RfidApi(api)
        sta = SettingsApi(api)
        ta = TransactionApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("rfid_location")
        setup_location.add_option("rfid_labels", 1)
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": False})
        response_location = setup_location.setup()

        test_label = response_location["rfid_labels"][0]["label"]
        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][0]["rfid_id"], "AVAILABLE")

        sta.set_reorder_controls_settings_for_shipto(response_location["shipto_id"])
        
        ra.rfid_issue(response_location["rfid"]["value"], test_label)
        rfid_labels_response = ra.get_rfid_labels(response_location["location_id"])
        test_label_body = rfid_labels_response[0]

        assert test_label_body["state"] == "ISSUED", f"RFID label should be in AVAILABLE status, now {test_label_body['state']}"

        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert len(transaction) == 1, "The number of transactions should be equal to 1"
        assert transaction[0]["reorderQuantity"] == (response_location["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_location['product']['roundBuy']*3}"
        assert transaction[0]["product"]["partSku"] == response_location["product"]["partSku"]

    @pytest.mark.regression
    def test_full_return_rfid_available_flow(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1912

        ra = RfidApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("rfid_location")
        setup_location.add_option("rfid_labels", 1)
        response_location = setup_location.setup()

        test_label = response_location["rfid_labels"][0]["label"]
        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][0]["rfid_id"], "ISSUED")

        initial_manifest_body = ra.create_return_manifest()
        ra.add_to_manifest(test_label, initial_manifest_body["data"]["id"], response_location["shipto_id"])
        manifest_body_1 = ra.get_manifest(initial_manifest_body["device_id"])

        assert len(manifest_body_1["items"]) == 1, f"Only 1 RFID label should being in the manifest, now {len(manifest_body_1['items'])}"
        assert str(manifest_body_1["items"][0]["rfidLabel"]["id"]) == str(response_location["rfid_labels"][0]["rfid_id"])
        assert manifest_body_1["items"][0]["rfidLabel"]["labelId"] == test_label
        assert manifest_body_1["items"][0]["rfidLabel"]["state"] == "ISSUED", f"RFID label should be in ISSUED status, now {manifest_body_1['items'][0]['rfidLabel']['state']}"

        ra.submit_manifest(initial_manifest_body["data"]["id"])
        manifest_body_2 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_2["items"][0]["rfidLabel"]["state"] == "RETURN_MANIFEST", f"RFID label should be in RETURN_MANIFEST status, now {manifest_body_2['items'][0]['rfidLabel']['state']}"

        ra.rfid_issue(response_location["rfid"]["value"], test_label)
        manifest_body_3 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_3["items"][0]["rfidLabel"]["state"] == "RETURN_CHECK_IN", f"RFID label should be in RETURN_CHECK_IN status, now {manifest_body_3['items'][0]['rfidLabel']['state']}"

        ra.close_manifest(initial_manifest_body["data"]["id"])
        ra.rfid_put_away(response_location["shipto_id"], response_location["rfid_labels"][0]["rfid_id"])
        rfid_labels_response = ra.get_rfid_labels(response_location["location_id"])

        assert len(rfid_labels_response) == 1, f"Location with ID = '{response_location['location_id']}' should contain only 1 RFID label, now {len(rfid_labels_response)}"
        
        test_label_body = rfid_labels_response[0]

        assert test_label_body["state"] == "AVAILABLE", f"RFID label should be in AVAILABLE status, now {test_label_body['state']}"
        assert test_label_body["returned"], "'returned' flag of RFID label should be TRUE"

    @pytest.mark.regression
    def test_full_rfid_available_flow(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1911

        ra = RfidApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("rfid_location")
        setup_location.add_option("rfid_labels", 1)
        response_location = setup_location.setup()
        test_label = response_location["rfid_labels"][0]["label"]

        initial_manifest_body = ra.get_new_delivery_manifest()
        ra.add_to_manifest(test_label, initial_manifest_body["data"]["id"], response_location["shipto_id"])
        manifest_body_1 = ra.get_manifest(initial_manifest_body["device_id"])

        assert len(manifest_body_1["items"]) == 1, "Only 1 RFID label should being in the manifest"
        assert str(manifest_body_1["items"][0]["rfidLabel"]["id"]) == str(response_location["rfid_labels"][0]["rfid_id"])
        assert manifest_body_1["items"][0]["rfidLabel"]["labelId"] == test_label
        assert manifest_body_1["items"][0]["rfidLabel"]["state"] == "ASSIGNED", f"RFID label should be in ASSIGNED status, now {manifest_body_1['items'][0]['rfidLabel']['state']}"

        ra.submit_manifest(initial_manifest_body["data"]["id"])
        manifest_body_2 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_2["items"][0]["rfidLabel"]["state"] == "MANIFEST", f"RFID label should be in MANIFEST status, now {manifest_body_2['items'][0]['rfidLabel']['state']}"

        ra.rfid_issue(response_location["rfid"]["value"], test_label)
        manifest_body_3 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_3["items"][0]["rfidLabel"]["state"] == "CHECK_IN", f"RFID label should be in CHECK_IN status, now {manifest_body_3['items'][0]['rfidLabel']['state']}"

        ra.close_manifest(initial_manifest_body["data"]["id"])
        ra.rfid_put_away(response_location["shipto_id"], response_location["rfid_labels"][0]["rfid_id"])
        rfid_labels_response = ra.get_rfid_labels(response_location["location_id"])

        assert len(rfid_labels_response) == 1, f"Location with ID = '{response_location['location_id']}' should contain only 1 RFID label, now {len(rfid_labels_response)}"
        
        test_label_body = rfid_labels_response[0]

        assert test_label_body["state"] == "AVAILABLE", f"RFID label should be in AVAILABLE status, now {test_label_body['state']}"
        assert not test_label_body["returned"], "'returned' flag of RFID label should be FALSE"