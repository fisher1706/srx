from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.location_basis import location_basis
from src.api.customer.assets_api import AssetsApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.location_api import LocationApi
from src.resources.tools import Tools


def delete_location_for_asset(case):
    case.log_name(" Delete location and check assets in 'Checked Out' tab (SRX-7852)")
    case.testrail_config(1996)

    try:
        aa = AssetsApi(case)
        sa = ShiptoApi(case)
        la = LocationApi(case)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        # create location with asset product
        response = location_basis(case, product_dto=product_dto)
        asset = response["product"]["partSku"]
        shipto_id = response["shipto_id"]
        location = la.get_location_by_sku(shipto_id, asset)
        location_id = location[0]["id"]

        aa.check_asset_in_all_assets_list(asset)
        la.delete_location(location_id, shipto_id)
        aa.check_asset_in_all_assets_list(asset, should_be=False)

        case.finish_case()
    except:
        case.critical_finish_case()
    
    try:
        sa.delete_shipto(response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    delete_location_for_asset(Case(Activity(api_test=True)))