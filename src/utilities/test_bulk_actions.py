import random
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.customer_api import CustomerApi
from src.api.setups.setup_customer import SetupCustomer

def test_bulk_delete_shiptos(api):
    sa = ShiptoApi(api)

    shiptos = sa.get_shipto_by_number(None)["data"]["entities"]

    for shipto in shiptos:
        if shipto["id"] > 61733:
            try:
                sa.delete_shipto(shipto["id"])
            except:
                print("FAIL")

def test_bulk_create_customers(api):
    for _ in range(100):
        SetupCustomer(api).setup()

def test_bulk_delete_customers(api):
    ca = CustomerApi(api)

    customers = ca.get_customers()

    for customer in customers:
        if customer["id"] > 3046:
            try:
                ca.delete_customer(customer["id"])
            except:
                print("FAIL")
