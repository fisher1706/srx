import pytest
from src.api.setups.setup_customer_location import SetupCustomerLocation
from src.api.setups.setup_location import SetupLocation

@pytest.fixture(scope="function")
def customer_organization_location_preset():
    def wrapper(context, ohi="MAX", reorder_controls_settings="DEFAULT"):
        setup_customer_location = SetupCustomerLocation(context)
        setup_customer_location.add_option("ohi", ohi)
        setup_customer_location.setup_organization.add_option("site")
        setup_customer_location.setup_organization.add_option("subsite")
        setup_customer_location.setup_organization.add_option("supplier")
        setup_customer_location.setup_organization.add_option("shipto")
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
