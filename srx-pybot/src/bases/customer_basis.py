from src.api.distributor.customer_api import CustomerApi
from src.api.distributor.warehouse_api import WarehouseApi
from src.api.api_methods import ApiMethods as apim
import random


def customer_basis(case, customer_dto=None, warehouse_id=None):
    if (warehouse_id is None):
        wa = WarehouseApi(case)
        warehouse_id = wa.get_first_warehouse_id()

    ca = CustomerApi(case)

    if (customer_dto is None):
        customer_dto = apim.get_dto("customer_dto.json")
        customer_dto["name"] = case.random_string_l(10)
        customer_dto["warehouse"]["id"] = warehouse_id

    new_customer = ca.create_customer(customer_dto.copy(), warehouse_id)

    response = {
        "customer": customer_dto.copy(),
        "customerId": new_customer,
        "warehouseId": warehouse_id
    }

    return response.copy()