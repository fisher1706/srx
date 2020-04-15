from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.location_basis import location_basis
from src.api.customer.assets_api import AssetsApi
from src.api.distributor.shipto_api import ShiptoApi
from src.resources.tools import Tools


def create_location_for_asset(case):
    case.log_name("Create location for asset product ")
    case.testrail_config(case.activity.variables.run_number, 1990)

    try:
        aa = AssetsApi(case)
        sa = ShiptoApi(case)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = "1"
        product_dto["assetFlag"] = True

        # create location with asset product
        response = location_basis(case, product_dto=product_dto)
        # check assetFlag 
        assert response["product"]["assetFlag"] == True, f"Location {response['product']['partSku']} does not have asset flag = true"
        t = aa.check_asset_in_all_assets_list(response["product"]["partSku"])

        case.finish_case()
    except:
        case.critical_finish_case()
    
    try:
        sa.delete_shipto(response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    create_location_for_asset(Case(Activity(api_test=True)))