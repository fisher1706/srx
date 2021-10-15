import pytest
from src.api.setups.setup_customer_location import SetupCustomerLocation

@pytest.fixture(scope="function")
def customer_full_organization_location_preset():
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
