from src.api.customer.customer_user_api import CustomerUserApi
from src.resources.tools import Tools
import copy

def setup_customer_user(context, customer_user_dto=None):
    cua = CustomerUserApi(context)

    if (customer_user_dto is None):
        customer_user_dto = Tools.get_dto("customer_user_dto.json")
        customer_user_dto["firstName"] = Tools.random_string_u()
        customer_user_dto["lastName"] = Tools.random_string_u()
        customer_user_dto["email"] = Tools.random_email()

    customer_user_id = cua.create_customer_user(copy.deepcopy(customer_user_dto))

    context.dynamic_context["delete_customer_user_id"].append(customer_user_id)
    response = {
        "customerUser": copy.deepcopy(customer_user_dto),
        "customerUserId": customer_user_id
    }

    return copy.deepcopy(response)