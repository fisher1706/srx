from src.api.distributor.shipto_api import ShiptoApi
from src.resources.tools import Tools
import copy

def setup_shipto(context, shipto_dto=None):
    sa = ShiptoApi(context)

    if (shipto_dto is None):
        shipto_dto = Tools.get_dto("shipto_dto.json")
        shipto_dto["number"] = Tools.random_string_l(10)
        shipto_dto["address"] = {
            "zipCode": "12345",
            "line1": "addressLn1",
            "line2": "addressLn1",
            "city": "Ct",
            "state": "AL"
        }
        shipto_dto["poNumber"] = Tools.random_string_l(10)
        shipto_dto["apiWarehouse"] = {
            "id": context.data.warehouse_id
        }

    new_shipto = sa.create_shipto(copy.deepcopy(shipto_dto))

    context.dynamic_context["delete_shipto_id"].append(new_shipto)

    response = {
        "shipto": copy.deepcopy(shipto_dto),
        "shipto_id": new_shipto
    }

    return copy.deepcopy(response)