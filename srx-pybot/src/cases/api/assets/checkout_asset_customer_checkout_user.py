from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.location_basis import location_basis
from src.bases.issue_return_basis import issue_return_basis
from src.api.customer.assets_api import AssetsApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.resources.tools import Tools


def checkout_asset_customer_checkout_user(case):
    case.log_name("User's assets checkouted as customer user and as checkout user")
    case.testrail_config(1988)

    try:
        aa = AssetsApi(case)
        sa = ShiptoApi(case)
        sta = SettingsApi(case)
        cha = CheckoutGroupApi(case)

        first_product_dto = Tools.get_dto("product_dto.json")
        first_product_dto["partSku"] = Tools.random_string_u(18)
        first_product_dto["shortDescription"] = f"{first_product_dto['partSku']} - short description"
        first_product_dto["roundBuy"] = 5
        first_product_dto["assetFlag"] = True

        second_product_dto = Tools.get_dto("product_dto.json")
        second_product_dto["partSku"] = Tools.random_string_u(18)
        second_product_dto["shortDescription"] = f"{second_product_dto['partSku']} - short description"
        second_product_dto["roundBuy"] = 5
        second_product_dto["assetFlag"] = True

        #create location with asset product
        first_response = location_basis(case, product_dto=first_product_dto)
        first_asset = first_response["product"]["partSku"]
        shipto_id = first_response["shipto_id"]

        #create location with asset product
        second_response = location_basis(case, shipto_dto=False, shipto_id=shipto_id, product_dto=second_product_dto)
        second_asset = second_response["product"]["partSku"]

        # enable checkout software for shipto
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        cha.add_shipto_to_checkout_group(shipto_id=shipto_id)

        issue_return_basis(case, shipto_id, first_asset, quantity=5, issue_product=True)
        issue_return_basis(case, shipto_id, second_asset, quantity=5, issue_product=True, passcode=case.activity.variables.customer_user_passcode)
        assets_list = aa.get_list_of_assets_by_user(case.activity.variables.customer_user_id)
        sku_list = []
        for item in assets_list:
            sku_list.append(item["partSku"])
            assert f"{item['user']['id']}" == case.activity.variables.customer_user_id, "There are assets that was issued NOT by current customer user"
        assert first_asset in sku_list, f"{first_asset} was not found in list of assets issued by user"
        assert second_asset in sku_list, f"{second_asset} was not found in list of assets issued by user"
        case.finish_case()
    except:
        case.critical_finish_case()
    
    try:
        sa.delete_shipto(shipto_id)
    except:
        case.print_traceback()

if __name__ == "__main__":
    checkout_asset_customer_checkout_user(Case(Activity(api_test=True)))