import pytest
import time
from src.api.customer.customer_user_api import CustomerUserApi
from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.admin.admin_hardware_api import AdminHardwareApi

@pytest.fixture(scope="function")
def delete_customer_user(context): #delete_customer_user_id
    yield
    context.is_teardown = True
    cua = CustomerUserApi(context)
    customer_user_id_list = context.dynamic_context["delete_customer_user_id"]
    for customer_user_id in customer_user_id_list:
        cua.delete_customer_user(customer_user_id)
    
@pytest.fixture(scope="function")
def delete_checkout_group(context): #delete_checkout_group_id
    yield
    context.is_teardown = True
    cga = CheckoutGroupApi(context)
    checkout_group_id_list = context.dynamic_context["delete_checkout_group_id"]
    for checkout_group_id in checkout_group_id_list:
        cga.delete_checkout_group(checkout_group_id)

@pytest.fixture(scope="function") #delete_shipto_id
def delete_shipto(context):
    yield
    context.is_teardown = True
    sa = ShiptoApi(context)
    shipto_id_list = context.dynamic_context["delete_shipto_id"]
    for shipto_id in shipto_id_list:
        sa.delete_shipto(shipto_id)

@pytest.fixture(scope="function") #delete_hardware_id OR delete_hardware_id_list
def delete_hardware(context):
    yield
    context.is_teardown = True
    aha = AdminHardwareApi(context)
    hardware_id_list = context.dynamic_context["delete_hardware_id"]
    for hardware_id in hardware_id_list:
        time.sleep(5)
        aha.delete_hardware(hardware_id)
