from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.customer_api import CustomerApi
from src.api.setups.setup_customer import SetupCustomer
from src.api.distributor.location_api import LocationApi

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
        if customer["id"] > 6811:
            try:
                ca.delete_customer(customer["id"], warehouse_id=customer["warehouse"]["id"])
            except:
                print("FAIL")

def test_bulk_update_locations_ohi(api):
    la = LocationApi(api)
    shipto_id = 84769
    customer_id = 5360
    locations = la.get_locations(shipto_id=shipto_id, customer_id=customer_id)
    for location in locations:
        la.update_location([location], shipto_id=shipto_id, customer_id=customer_id)
