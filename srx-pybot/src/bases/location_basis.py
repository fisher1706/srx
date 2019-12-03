from src.api.distributor.location_api import LocationApi
from src.api.api_methods import ApiMethods as apim
from src.bases.shipto_basis import shipto_basis
from src.bases.product_basis import product_basis
import random


def location_basis(case, product_dto=None, shipto_dto=None, location_dto=None, location_type="LABEL"):
    la = LocationApi(case)

    product_dto = product_basis(case, product_dto)

    shipto_response = shipto_basis(case, shipto_dto)
    shipto_dto = shipto_response["shipto"].copy()
    new_shipto = shipto_response["shipto_number"]

    if (location_dto is None):
        location_dto = apim.get_dto("location_dto.json")
        location_dto["attributeName1"] = product_dto["partSku"]
        location_dto["attributeValue1"] = product_dto["partSku"]
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
    location_list = [location_dto.copy()]

    la.create_location(location_list.copy(), new_shipto)

    response = {
        "product": product_dto,
        "shipto": shipto_dto,
        "location": location_dto,
        "shipto_number": new_shipto
    }

    return response.copy()