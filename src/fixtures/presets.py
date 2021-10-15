import pytest
from src.api.setups.setup_customer_location import SetupCustomerLocation
from src.api.setups.setup_location import SetupLocation

@pytest.fixture(scope="function")
def customer_organization_location_preset():
    def wrapper(api, ohi="MAX", reorder_controls_settings="DEFAULT"):
        setup_customer_location = SetupCustomerLocation(api)
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
    def wrapper(api, round_buy=1, serialization_settings=None):
        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", round_buy)
        if serialization_settings is not None:
            setup_location.setup_shipto.add_option("serialization_settings", serialization_settings)
        return setup_location.setup()
    return wrapper
