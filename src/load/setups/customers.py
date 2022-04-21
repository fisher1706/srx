import copy
from src.api.setups.setup_customer import SetupCustomer
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.warehouse_api import WarehouseApi
from src.api.distributor.product_api import  ProductApi
from src.api.distributor.location_api import LocationApi
from src.resources.tools import Tools

def test_customer_setup(load_api):
    wa = WarehouseApi(load_api)
    sa = ShiptoApi(load_api)
    pa = ProductApi(load_api)
    la = LocationApi(load_api)
    customers = list()
    shiptos = list()
    ###########################
    total_customers = 2
    shiptos_per_customer = 2
    locations_per_shipto = 100
    create_location_step = 50
    start_customer = 7
    ###########################

    warehouses = wa.get_warehouses()["entities"]
    products = pa.get_product(size=locations_per_shipto)
    ###############################################
    #           CREATE CUSTOMERS                  #
    ###############################################
    for index_customer in range(total_customers):
        setup_customer = SetupCustomer(load_api)
        setup_customer.add_option("warehouse_id", warehouses[index_customer]["id"])
        customer_name_number = f"{start_customer + index_customer}"
        if index_customer%5 == 0:
            setup_customer.add_option("clc")
            customer_name_number += " + CLC"
        setup_customer.add_option("name", customer_name_number)
        setup_customer.add_option("number", customer_name_number)
        customer_response = setup_customer.setup()
        customer_id = customer_response["customer_id"]
        customer_data = {
            "id": customer_id,
            "number": customer_name_number
        }
        customers.append(customer_data)
        ###############################################
        #           CREATE SHIPTOS                    #
        ###############################################
        shipto = Tools.get_dto("shipto_dto.json")
        for index_shipto in range(shiptos_per_customer):
            shipto["number"] = f"{index_shipto}"
            shipto["poNumbers"].append({
                "value": Tools.random_string_l(10),
                "default": True,
                "expectedSpend": ""
            })
            shipto["apiWarehouse"] = {
                "id": warehouses[index_customer]["id"]
            }
            shipto_id = sa.create_shipto(dto=shipto, customer_id=customer_id)
            shipto_data = {
                "id": shipto_id,
                "number": shipto["number"]
            }
            shiptos.append(shipto_data)
            ###############################################
            #           CREATE LOCATIONS                  #
            ###############################################
            location_list = list()
            for product in products:
                location = Tools.get_dto("location_dto.json")
                location["attributeName1"] = product["partSku"]
                location["attributeValue1"] = product["partSku"]
                location["orderingConfig"] = {
                    "product": {
                        "partSku": product["partSku"],
                    },
                    "type": "LABEL",
                    "currentInventoryControls": {
                        "min": product["roundBuy"],
                        "max": product["roundBuy"]*3
                    },
                }
                location_list.append(location)
            for start_index in range(0, locations_per_shipto, create_location_step):
                la.create_location(copy.deepcopy(location_list[start_index:start_index+create_location_step]), shipto_id, customer_id=customer_id)
