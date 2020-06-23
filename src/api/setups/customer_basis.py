from src.api.distributor.customer_api import CustomerApi
from src.api.distributor.warehouse_api import WarehouseApi
from src.resources.tools import Tools
import copy

def customer_basis(case, customer_dto=None, warehouse_id=None):
    if (warehouse_id is None):
        wa = WarehouseApi(case)
        warehouse_id = wa.get_first_warehouse_id()

    ca = CustomerApi(case)

    if (customer_dto is None):
        customer_dto = Tools.get_dto("customer_dto.json")
        customer_dto["name"] = Tools.random_string_l(10)
        customer_dto["warehouse"]["id"] = warehouse_id

    new_customer = ca.create_customer(copy.deepcopy(customer_dto), warehouse_id)

    response = {
        "customer": copy.deepcopy(customer_dto),
        "customerId": new_customer,
        "warehouseId": warehouse_id
    }

    return copy.deepcopy(response)