from src.api.distributor.shipto_api import ShiptoApi
from src.api.api_methods import ApiMethods as apim
import random
import copy

def shipto_basis(case, shipto_dto=None):
    sa = ShiptoApi(case)

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

    new_shipto = sa.create_shipto(copy.deepcopy(shipto_dto))

    response = {
        "shipto": copy.deepcopy(shipto_dto),
        "shipto_id": new_shipto
    }

    return copy.deepcopy(response)