from src.api.distributor.location_api import LocationApi
from src.api.setups.setup_shipto import setup_shipto
from src.api.setups.setup_product import setup_product
from src.api.distributor.shipto_api import ShiptoApi
from src.resources.tools import Tools
import copy

def setup_location(context, product_dto=None, shipto_dto=None, shipto_id=None, location_dto=None, location_pairs=None, location_type="LABEL"):
    la = LocationApi(context)
    sha = ShiptoApi(context)

    product_dto = setup_product(context, product_dto)

    if (shipto_dto is None):
        shipto_response = setup_shipto(context, shipto_dto)
        shipto_dto = copy.deepcopy(shipto_response["shipto"])
        shipto_id = shipto_response["shipto_id"]
        context.dynamic_context["delete_hardware_id"].append(shipto_id)

    if (shipto_id is not None):
        shipto_dto = sha.get_shipto_by_id(shipto_id)

    if (location_dto is None):
        location_dto = Tools.get_dto("location_dto.json")
        if (location_pairs is None):
            location_dto["attributeName1"] = product_dto["partSku"]
            location_dto["attributeValue1"] = product_dto["partSku"]
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
                "partSku": product_dto["partSku"]
            },
            "type": location_type,
            "currentInventoryControls": {
                "min": product_dto["roundBuy"],
                "max": product_dto["roundBuy"]*3
            }
        }
    location_list = [copy.deepcopy(location_dto)]


    la.create_location(copy.deepcopy(location_list), shipto_id)

    response = {
        "product": product_dto,
        "shipto": shipto_dto,
        "location": location_dto,
        "shipto_id": shipto_id
    }

    return copy.deepcopy(response)