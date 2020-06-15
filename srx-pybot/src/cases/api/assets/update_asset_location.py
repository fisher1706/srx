from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.location_basis import location_basis
from src.bases.issue_return_basis import issue_return_basis
from src.api.customer.assets_api import AssetsApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.transaction_api import TransactionApi
from src.resources.tools import Tools
import copy

def update_asset_location(case):
    case.log_name("Update location for asset with OHI 0 (SRX-2008)")
    case.testrail_config(1990)

    try:
        aa = AssetsApi(case)
        sa = ShiptoApi(case)
        sta = SettingsApi(case)
        la = LocationApi(case)
        ta = TransactionApi(case)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        # create location with asset product
        response = location_basis(case, product_dto=product_dto)
        asset = response["product"]["partSku"]
        shipto_id = response["shipto_id"]
        max_quantity = response["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)

        issue_return_basis(case, shipto_id, asset, quantity=max_quantity, issue_product=True)
        location = la.get_location_by_sku(shipto_id, asset)
        assert location[0]["onHandInventory"] == 0, "OHI != 0"
        location_dto = copy.deepcopy(location)
        location_dto[0]["autoSubmit"] = True
        la.update_location(location_dto, shipto_id)
        location = la.get_location_by_sku(shipto_id, asset)
        transaction = ta.get_transaction(sku=asset, shipto_id=shipto_id)
        assert transaction["totalElements"] == 0, f"There should not be transactions with SKU: {asset}"

        case.finish_case()
    except:
        case.critical_finish_case()
    
    try:
        sa.delete_shipto(response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    update_asset_location(Case(Activity(api_test=True)))