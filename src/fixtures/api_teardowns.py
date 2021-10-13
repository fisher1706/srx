import time
import pytest
from src.api.customer.customer_user_api import CustomerUserApi
from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.api.customer.organization_api import OrganizationApi
from src.api.distributor.user_api import UserApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.customer_api import CustomerApi
from src.api.admin.admin_hardware_api import AdminHardwareApi
from src.api.admin.smart_shelves_api import SmartShelvesApi

@pytest.fixture(scope="function")
def delete_customer_user(context):
    yield
    context.is_teardown = True
    cua = CustomerUserApi(context)
    customer_user_id_list = context.dynamic_context["delete_customer_user_id"]
    for customer_user_id in customer_user_id_list:
        cua.delete_customer_user(customer_user_id)

@pytest.fixture(scope="function")
def delete_distributor_user(context):
    yield
    context.is_teardown = True
    ua = UserApi(context)
    distributor_user_id_list = context.dynamic_context["delete_distributor_user_id"]
    for distributor_user_id in distributor_user_id_list:
        ua.delete_distributor_user(distributor_user_id)

@pytest.fixture(scope="function")
def delete_distributor_security_group(context):
    yield
    context.is_teardown = True
    ua = UserApi(context)
    distributor_security_group_id_list = context.dynamic_context["delete_distributor_security_group_id"]
    for distributor_security_group_id in distributor_security_group_id_list:
        ua.delete_security_group(distributor_security_group_id, context.data.default_security_group_id)

@pytest.fixture(scope="function")
def delete_checkout_group(context):
    yield
    context.is_teardown = True
    cga = CheckoutGroupApi(context)
    checkout_group_id_list = context.dynamic_context["delete_checkout_group_id"]
    for checkout_group_id in checkout_group_id_list:
        cga.delete_checkout_group(checkout_group_id)

@pytest.fixture(scope="function")
def delete_shipto(context):
    yield
    context.is_teardown = True
    sa = ShiptoApi(context)
    shipto_id_list = context.dynamic_context["delete_shipto_id"]
    for shipto_id in shipto_id_list:
        sa.delete_shipto(shipto_id)

@pytest.fixture(scope="function")
def delete_customer(context):
    yield
    context.is_teardown = True
    ca = CustomerApi(context)
    customer_id_list = context.dynamic_context["delete_customer_id"]
    for customer_id in customer_id_list:
        ca.delete_customer(customer_id)

@pytest.fixture(scope="function")
def delete_hardware(context):
    yield
    context.is_teardown = True
    aha = AdminHardwareApi(context)
    hardware_id_list = context.dynamic_context["delete_hardware_id"]
    for hardware_id in hardware_id_list:
        time.sleep(5)
        aha.delete_hardware(hardware_id)

@pytest.fixture(scope="function")
def delete_smart_shelf(context):
    yield
    context.is_teardown = True
    ssa = SmartShelvesApi(context)
    smart_shelf_id_list = context.dynamic_context["delete_smart_shelf_id"]
    for smart_shelf_id in smart_shelf_id_list:
        time.sleep(3)
        ssa.delete_smart_shelves(smart_shelf_id)

@pytest.fixture(scope="function")
def delete_site(context):
    yield
    context.is_teardown = True
    oa = OrganizationApi(context)
    site_id_list = context.dynamic_context["delete_site_id"]
    for site_id in site_id_list:
        oa.delete_site(site_id)

@pytest.fixture(scope="function")
def delete_subsite(context):
    yield
    context.is_teardown = True
    oa = OrganizationApi(context)
    subsite_id_list = context.dynamic_context["delete_subsite_id"]
    for subsite_id in subsite_id_list:
        oa.delete_subsite(subsite_id)

@pytest.fixture(scope="function")
def delete_supplier(context):
    yield
    context.is_teardown = True
    oa = OrganizationApi(context)
    supplier_id_list = context.dynamic_context["delete_supplier_id"]
    for supplier_id in supplier_id_list:
        oa.delete_supplier(supplier_id)

@pytest.fixture(scope="function")
def delete_customer_shipto(context):
    yield
    context.is_teardown = True
    oa = OrganizationApi(context)
    shipto_id_list = context.dynamic_context["delete_customer_shipto_id"]
    for shipto_id in shipto_id_list:
        oa.delete_shipto(shipto_id)