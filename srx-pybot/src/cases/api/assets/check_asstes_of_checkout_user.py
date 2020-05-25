from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.location_basis import location_basis
from src.bases.issue_return_basis import issue_return_basis
from src.api.customer.assets_api import AssetsApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.resources.tools import Tools


def check_asstes_of_checkout_user(case):
    case.log_name("Do not see assets of another user when look to the checkout user assets (SRX-8324)")
    case.testrail_config(1995)

    try:
        aa = AssetsApi(case)
        sa = ShiptoApi(case)
        sta = SettingsApi(case)
        cha = CheckoutGroupApi(case)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = 5
        product_dto["assetFlag"] = True

        #create location with asset product
        response = location_basis(case, product_dto=product_dto)
        asset = response["product"]["partSku"]
        shipto_name = response["shipto"]["number"]
        shipto_id = response["shipto_id"]
        total = response["location"]["orderingConfig"]["currentInventoryControls"]["max"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        cha.add_shipto_to_checkout_group(shipto_id=shipto_id)

        # issue 5 assets
        issue_return_basis(case, shipto_id, asset, quantity=5, issue_product=True, passcode=case.activity.variables.passcode)
        # check list of assets of checkout user
        list_of_assets = aa.get_list_of_assets_by_user(case.activity.variables.checkout_user_id)
        for item in list_of_assets:
            assert f"{item['user']['id']}" == case.activity.variables.checkout_user_id, "There are assets that was issued NOT by checkout user"

        case.finish_case()
    except:
        case.critical_finish_case()
    
    try:
        sa.delete_shipto(response["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    check_asstes_of_checkout_user(Case(Activity(api_test=True)))