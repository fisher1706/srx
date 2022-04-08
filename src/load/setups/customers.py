from src.api.setups.setup_customer import SetupCustomer
from src.api.distributor.warehouse_api import WarehouseApi

def test_customer_setup(load_api):
    wa = WarehouseApi(load_api)
    warehouses = wa.get_warehouses()["entities"]
    for index in range(10):
        if index > 5:
            break
        setup_customer = SetupCustomer(load_api)
        setup_customer.add_option("warehouse_id", warehouses[index]["id"])
        if index%5 == 0:
            setup_customer.add_option("clc")
        setup_customer.setup()
