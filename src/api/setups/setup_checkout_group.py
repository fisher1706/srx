from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.api.customer.customer_user_api import CustomerUserApi
from src.resources.tools import Tools
import copy

def setup_checkout_group(context, checkout_group_dto=None):
    cga = CheckoutGroupApi(context)
    ca = CustomerUserApi(context)

    if (checkout_group_dto is None):
        customer_user_id = ca.get_customer_users()[0]["id"]
        checkout_group_dto = {
            "name": "Name " + Tools.random_string_l(),
            "email": Tools.random_email(),
            "owner": {
                "id": customer_user_id
            },
        }
    new_checkout_group = cga.create_checkout_group(checkout_group_dto)
    context.dynamic_context["delete_checkout_group_id"].append(new_checkout_group["id"])

    return copy.deepcopy(new_checkout_group)