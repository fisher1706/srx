import pytest
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.distributor.rfid_page import RfidPage
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_rfid import setup_rfid
from src.api.setups.setup_rfid_location import setup_rfid_location
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.settings_api import SettingsApi

class TestRfid():
    @pytest.mark.regression
    def test_rfid_label_crud(self, ui, delete_shipto):
        ui.testrail_case_id = 1918

        lp = LoginPage(ui)
        rp = RfidPage(ui)

        response_location = setup_location(ui, location_type="RFID")
        shipto_text = f"{ui.data.customer_name} - {response_location['shipto']['number']}"
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

    @pytest.mark.regression
    def test_create_rfid_transaction_as_issued(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1914

        ra = RfidApi(api)
        sta = SettingsApi(api)
        ta = TransactionApi(api)

        response_rfid_location = setup_rfid_location(api, number_of_labels=3)
        ra.update_rfid_label(response_rfid_location["location_id"], response_rfid_location["labels"][0]["rfid_id"], "AVAILABLE")
        ra.update_rfid_label(response_rfid_location["location_id"], response_rfid_location["labels"][1]["rfid_id"], "AVAILABLE")
        ra.update_rfid_label(response_rfid_location["location_id"], response_rfid_location["labels"][2]["rfid_id"], "AVAILABLE")

        response_rfid = setup_rfid(api, response_rfid_location["shipto_id"])

        sta.set_checkout_software_settings_for_shipto(response_rfid_location["shipto_id"], reorder_controls="ISSUED")
        
        ra.rfid_issue(response_rfid["value"], response_rfid_location["labels"][0]["label"])

        transaction = ta.get_transaction(shipto_id=response_rfid_location["shipto_id"])["entities"]
        assert len(transaction) == 1, "The number of transactions should be equal to 1"
        assert transaction[0]["reorderQuantity"] == response_rfid_location["product"]["roundBuy"], f"Reorder quantity of transaction should be equal to {response_rfid_location['product']['roundBuy']}"
        assert transaction[0]["product"]["partSku"] == response_rfid_location["product"]["partSku"]

    @pytest.mark.regression
    def test_create_rfid_transaction_at_min(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1913

        ra = RfidApi(api)
        sta = SettingsApi(api)
        ta = TransactionApi(api)

        response_rfid_location = setup_rfid_location(api, number_of_labels=1)
        test_label = response_rfid_location["labels"][0]["label"]
        ra.update_rfid_label(response_rfid_location["location_id"], response_rfid_location["labels"][0]["rfid_id"], "AVAILABLE")

        response_rfid = setup_rfid(api, response_rfid_location["shipto_id"])

        sta.set_checkout_software_settings_for_shipto(response_rfid_location["shipto_id"])
        
        ra.rfid_issue(response_rfid["value"], test_label)
        rfid_labels_response = ra.get_rfid_labels(response_rfid_location["location_id"])
        test_label_body = rfid_labels_response[0]

        assert test_label_body["state"] == "ISSUED", f"RFID label should be in AVAILABLE status, now {test_label_body['state']}"

        transaction = ta.get_transaction(shipto_id=response_rfid_location["shipto_id"])["entities"]
        assert len(transaction) == 1, "The number of transactions should be equal to 1"
        assert transaction[0]["reorderQuantity"] == (response_rfid_location["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_rfid_location['product']['roundBuy']*3}"
        assert transaction[0]["product"]["partSku"] == response_rfid_location["product"]["partSku"]

    @pytest.mark.regression
    def test_full_return_rfid_available_flow(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1912

        ra = RfidApi(api)

        response_rfid_location = setup_rfid_location(api, number_of_labels=1)
        test_label = response_rfid_location["labels"][0]["label"]
        ra.update_rfid_label(response_rfid_location["location_id"], response_rfid_location["labels"][0]["rfid_id"], "ISSUED")

        response_rfid = setup_rfid(api, response_rfid_location["shipto_id"])

        initial_manifest_body = ra.create_return_manifest()
        ra.add_to_manifest(test_label, initial_manifest_body["data"]["id"], response_rfid_location["shipto_id"])
        manifest_body_1 = ra.get_manifest(initial_manifest_body["device_id"])

        assert len(manifest_body_1["items"]) == 1, f"Only 1 RFID label should being in the manifest, now {len(manifest_body_1['items'])}"
        assert str(manifest_body_1["items"][0]["rfidLabel"]["id"]) == str(response_rfid_location["labels"][0]["rfid_id"])
        assert manifest_body_1["items"][0]["rfidLabel"]["labelId"] == test_label
        assert manifest_body_1["items"][0]["rfidLabel"]["state"] == "ISSUED", f"RFID label should be in ISSUED status, now {manifest_body_1['items'][0]['rfidLabel']['state']}"

        ra.submit_manifest(initial_manifest_body["data"]["id"])
        manifest_body_2 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_2["items"][0]["rfidLabel"]["state"] == "RETURN_MANIFEST", f"RFID label should be in RETURN_MANIFEST status, now {manifest_body_2['items'][0]['rfidLabel']['state']}"

        ra.rfid_issue(response_rfid["value"], test_label)
        manifest_body_3 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_3["items"][0]["rfidLabel"]["state"] == "RETURN_CHECK_IN", f"RFID label should be in RETURN_CHECK_IN status, now {manifest_body_3['items'][0]['rfidLabel']['state']}"

        ra.close_manifest(initial_manifest_body["data"]["id"])
        ra.rfid_put_away(response_rfid_location["shipto_id"], response_rfid_location["labels"][0]["rfid_id"])
        rfid_labels_response = ra.get_rfid_labels(response_rfid_location["location_id"])

        assert len(rfid_labels_response) == 1, f"Location with ID = '{response_rfid_location['location_id']}' should contain only 1 RFID label, now {len(rfid_labels_response)}"
        
        test_label_body = rfid_labels_response[0]

        assert test_label_body["state"] == "AVAILABLE", f"RFID label should be in AVAILABLE status, now {test_label_body['state']}"
        assert test_label_body["returned"] == True, "'returned' flag of RFID label should be TRUE"

    @pytest.mark.regression
    def test_full_rfid_available_flow(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1911

        ra = RfidApi(api)

        response_rfid_location = setup_rfid_location(api, number_of_labels=1)
        test_label = response_rfid_location["labels"][0]["label"]

        response_rfid = setup_rfid(api, response_rfid_location["shipto_id"])

        initial_manifest_body = ra.get_new_delivery_manifest()
        ra.add_to_manifest(test_label, initial_manifest_body["data"]["id"], response_rfid_location["shipto_id"])
        manifest_body_1 = ra.get_manifest(initial_manifest_body["device_id"])

        assert len(manifest_body_1["items"]) == 1, "Only 1 RFID label should being in the manifest"
        assert str(manifest_body_1["items"][0]["rfidLabel"]["id"]) == str(response_rfid_location["labels"][0]["rfid_id"])
        assert manifest_body_1["items"][0]["rfidLabel"]["labelId"] == test_label
        assert manifest_body_1["items"][0]["rfidLabel"]["state"] == "ASSIGNED", f"RFID label should be in ASSIGNED status, now {manifest_body_1['items'][0]['rfidLabel']['state']}"

        ra.submit_manifest(initial_manifest_body["data"]["id"])
        manifest_body_2 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_2["items"][0]["rfidLabel"]["state"] == "MANIFEST", f"RFID label should be in MANIFEST status, now {manifest_body_2['items'][0]['rfidLabel']['state']}"

        ra.rfid_issue(response_rfid["value"], test_label)
        manifest_body_3 = ra.get_manifest(initial_manifest_body["device_id"])

        assert manifest_body_3["items"][0]["rfidLabel"]["state"] == "CHECK_IN", f"RFID label should be in CHECK_IN status, now {manifest_body_3['items'][0]['rfidLabel']['state']}"

        ra.close_manifest(initial_manifest_body["data"]["id"])
        ra.rfid_put_away(response_rfid_location["shipto_id"], response_rfid_location["labels"][0]["rfid_id"])
        rfid_labels_response = ra.get_rfid_labels(response_rfid_location["location_id"])

        assert len(rfid_labels_response) == 1, f"Location with ID = '{response_rfid_location['location_id']}' should contain only 1 RFID label, now {len(rfid_labels_response)}"
        
        test_label_body = rfid_labels_response[0]

        assert test_label_body["state"] == "AVAILABLE", f"RFID label should be in AVAILABLE status, now {test_label_body['state']}"
        assert test_label_body["returned"] == False, "'returned' flag of RFID label should be FALSE"