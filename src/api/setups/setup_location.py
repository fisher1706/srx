from src.api.distributor.location_api import LocationApi
from src.api.setups.setup_shipto import setup_shipto
from src.api.setups.setup_product import setup_product
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.resources.tools import Tools
import copy

def setup_location(context, product_dto=None, ohi=None, shipto_dto=None, shipto_id=None, location_dto=None, location_pairs=None, location_type="LABEL", response_product=None, is_serialized=None, is_lot=None, is_autosubmit=None, checkout_settings_shipto=None):
    la = LocationApi(context)
    sha = ShiptoApi(context)
    sta = SettingsApi(context)

    if (response_product is None):
        response_product = setup_product(context, product_dto)

    if (shipto_id is not None):
        shipto_dto = sha.get_shipto_by_id(shipto_id)
    elif (shipto_dto is None):
        shipto_response = setup_shipto(context, shipto_dto)
        shipto_dto = copy.deepcopy(shipto_response["shipto"])
        shipto_id = shipto_response["shipto_id"]
        
    if (checkout_settings_shipto is not None):
        if (checkout_settings_shipto == "DEFAULT"):
            sta.set_checkout_software_settings_for_shipto(shipto_id)
        else:
            context.logger.warning(f"Unknown 'checkout_settings_shipto' option for Location Setup: '{checkout_settings_shipto}'")

    if (location_dto is None):
        location_dto = Tools.get_dto("location_dto.json")
        if (location_pairs is None):
            location_dto["attributeName1"] = response_product["partSku"]
            location_dto["attributeValue1"] = response_product["partSku"]
        else:
            location_dto["attributeName1"] = location_pairs["attributeName1"]
            location_dto["attributeValue1"] = location_pairs["attributeValue1"]
            location_dto["attributeName2"] = location_pairs["attributeName2"]
            location_dto["attributeValue2"] = location_pairs["attributeValue2"]
            location_dto["attributeName3"] = location_pairs["attributeName3"]
            location_dto["attributeValue3"] = location_pairs["attributeValue3"]
            location_dto["attributeName4"] = location_pairs["attributeName4"]
            location_dto["attributeValue4"] = location_pairs["attributeValue4"]
        location_dto["orderingConfig"] = {
            "product": {
                "partSku": response_product["partSku"]
            },
            "type": location_type,
            "currentInventoryControls": {
                "min": response_product["roundBuy"],
                "max": response_product["roundBuy"]*3
            }
        }
        if (ohi is not None):
            location_dto["onHandInventory"] = ohi
        if (is_serialized is not None):
            location_dto["serialized"] = bool(is_serialized)
        if (is_lot is not None):
            location_dto["lot"] = bool(is_lot)
        if (is_autosubmit is not None):
            location_dto["autoSubmit"] = bool(is_autosubmit)
    location_list = [copy.deepcopy(location_dto)]


    la.create_location(copy.deepcopy(location_list), shipto_id)

    response = {
        "product": response_product,
        "shipto": shipto_dto,
        "location": location_dto,
        "shipto_id": shipto_id
    }

    return copy.deepcopy(response)