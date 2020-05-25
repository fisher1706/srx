from src.api.distributor.location_api import LocationApi
from src.api.distributor.shipto_api import ShiptoApi
from src.bases.shipto_basis import shipto_basis
from src.bases.product_basis import product_basis
from src.resources.tools import Tools
import copy

def location_basis(case, product_dto=None, shipto_dto=None, shipto_id=None, location_dto=None, location_pairs=None, location_type="LABEL"):
    la = LocationApi(case)
    sha = ShiptoApi(case)

    product_dto = product_basis(case, product_dto)

    if (shipto_dto is None):
        shipto_response = shipto_basis(case, shipto_dto)
        shipto_dto = copy.deepcopy(shipto_response["shipto"])
        shipto_id = shipto_response["shipto_id"]

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