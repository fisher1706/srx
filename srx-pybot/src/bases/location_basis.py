from src.api.distributor.product_api import ProductApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.location_api import LocationApi
from src.api.api_methods import ApiMethods as apim
import random


def location_basis(case, product_dto=None, shipto_dto=None, location_dto=None, location_type="LABEL"):
    pa = ProductApi(case)
    sa = ShiptoApi(case)
    la = LocationApi(case)

    if (product_dto is None):
        product_dto = apim.get_dto("product_dto.json")
        product_dto["partSku"] = case.random_string_u(18)
        product_dto["shortDescription"] = product_dto["partSku"] + " - short description"
        product_dto["roundBuy"] = random.choice(range(100))

    if (shipto_dto is None):
        shipto_dto = apim.get_dto("shipto_dto.json")
        shipto_dto["number"] = case.random_string_l(10)
        shipto_dto["address"] = {
            "zipCode": "12345",
            "line1": "addressLn1",
            "line2": "addressLn1",
            "city": "Ct",
            "state": "AL"
        }
        shipto_dto["poNumber"] = case.random_string_l(10)

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

    pa.create_product(product_dto.copy())
    new_shipto = sa.create_shipto(shipto_dto.copy())
    la.create_location(location_list.copy(), new_shipto)

    response = {
        "product": product_dto,
        "shipto": shipto_dto,
        "location": location_dto,
        "shipto_number": new_shipto
    }

    return response.copy()