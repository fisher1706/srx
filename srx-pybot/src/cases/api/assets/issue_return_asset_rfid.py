from src.resources.case import Case
from src.resources.activity import Activity
from src.pages.sub.login_page import LoginPage
from src.bases.location_basis import location_basis
from src.bases.issue_return_basis import issue_return_basis
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.api.admin.hardware_api import HardwareApi
from src.api.distributor.rfid_api import RfidApi
from src.api.customer.assets_api import AssetsApi
from src.bases.rfid_location_basis import rfid_location_basis
from src.bases.rfid_basis import rfid_basis
from src.resources.tools import Tools


def issue_return_assets_rfid(case):
    case.log_name("Issue/return asset as customer user, location type: rfid")
    case.testrail_config(1999)

    try:
        sa = ShiptoApi(case)
        sta = SettingsApi(case)
        ha = HardwareApi(case)
        ra = RfidApi(case)
        aa = AssetsApi(case)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        #create location of type RFID with asset product
        rfid_location_response = rfid_location_basis(case, number_of_labels=1, product_dto=product_dto)
        asset = rfid_location_response["location"]["product"]["partSku"]
        rfid_response = rfid_basis(case, rfid_location_response["shipto_id"])

        shipto_id = rfid_location_response["shipto_id"]
        location_id = rfid_location_response["location_id"]
        rfid_id = rfid_response["id"]

        rfid_labels = ra.get_rfid_labels(location_id)
        label_id = rfid_labels[0]["id"]
        epc = rfid_labels[0]["labelId"]

        ra.update_rfid_label(location_id, label_id, "AVAILABLE")

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)

        issue_return_basis(case, shipto_id, asset, epc=epc, issue_product=True)
        result_checked_out = aa.check_asset_in_checked_out_list(asset)
        assert result_checked_out["credit"] == product_dto["roundBuy"], f"QTY of cheked out asset is NOT correct"
        assert result_checked_out["location"]["onHandInventory"] == 0, f"OHI of cheked out asset is NOT correct"
        result_all_assets = aa.check_asset_in_all_assets_list(asset)
        assert result_all_assets["onHandInventory"] == 0, f"OHI of cheked out asset is NOT correct"
        rfid_labels = ra.get_rfid_labels(location_id)
        assert rfid_labels[0]["state"] == "ISSUED", f"RFID label has incorrect status {rfid_labels[0]['state']}"

        issue_return_basis(case, shipto_id, asset, epc=epc, return_product=True)
        aa.check_asset_in_checked_out_list(asset, should_be=False)
        #get status of RFID label
        rfid_labels = ra.get_rfid_labels(location_id)
        assert rfid_labels[0]["state"] == "RETURN_CHECK_IN", f"RFID label has incorrect status {rfid_labels[0]['state']}"

        case.finish_case()
    except:
        case.critical_finish_case()
    
    try:
        ha.delete_hardware(rfid_response["id"])
        sa.delete_shipto(shipto_id)
    except:
        case.print_traceback()

if __name__ == "__main__":
    issue_return_assets_rfid(Case(Activity(api_test=True)))