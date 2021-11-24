import time
import pytest
from src.api.setups.setup_customer_location import SetupCustomerLocation
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.mocks_api import MocksApi

@pytest.fixture(scope="function")
def customer_organization_location_preset():
    def wrapper(context, ohi="MAX", reorder_controls_settings="DEFAULT", price=None):
        setup_customer_location = SetupCustomerLocation(context)
        setup_customer_location.add_option("ohi", ohi)
        setup_customer_location.setup_organization.add_option("site")
        setup_customer_location.setup_organization.add_option("subsite")
        setup_customer_location.setup_organization.add_option("supplier")
        setup_customer_location.setup_organization.add_option("shipto")
        setup_customer_location.setup_customer_product.add_option("price", price)
        setup_customer_location.setup_organization.setup_customer_shipto.add_option("reorder_controls_settings", reorder_controls_settings)
        return setup_customer_location.setup()
    return wrapper

@pytest.fixture(scope="function")
def serialized_location_preset():
    def wrapper(context, round_buy=1, serialization_settings=None, lot=None):
        setup_location = SetupLocation(context)
        setup_location.add_option("serialized")
        setup_location.add_option("lot", lot)
        setup_location.setup_product.add_option("round_buy", round_buy)
        setup_location.setup_shipto.add_option("serialization_settings", serialization_settings)
        return setup_location.setup()
    return wrapper

@pytest.fixture(scope="function")
def sync_order_location_preset():
    def wrapper(context, sync_endpoint):
        sa = SettingsApi(context)
        ma = MocksApi(context)
        la = LocationApi(context)
        ta = TransactionApi(context)

        endpoints_list = ["quoteOrders", "salesOrders"]
        endpoints_list.append(sync_endpoint)
        ma.set_list_of_available_endpoints(endpoints_list)
        sa.sync_erp_connection_settings()

        setup_location = SetupLocation(context)
        setup_location.add_option("min", 10)
        setup_location.add_option("max", 100)
        setup_location.add_option("ohi", 100)
        setup_location.setup_product.add_option("round_buy", 10)
        setup_location.setup_shipto.add_option("rl_submit_integration")
        setup_location.setup_shipto.add_option("customer_id", "lowest")
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True, "track_ohi": True, "reorder_controls": "ISSUED"})
        preset = setup_location.setup()

        #create ACTIVE transaction
        location = la.get_locations(shipto_id=preset["shipto_id"], customer_id=preset["customer_id"])[0]
        location["onHandInventory"] = 0
        la.update_location([location], preset["shipto_id"], customer_id=preset["customer_id"])
        time.sleep(5)
        transaction = ta.get_transaction(sku=preset["product"]["partSku"], shipto_id=preset["shipto_id"], status="ACTIVE")
        preset["transaction"] = {
            "transaction_id": transaction["entities"][0]["id"],
            "reorder_quantity": transaction["entities"][0]["reorderQuantity"]
        }
        return preset
    return wrapper
