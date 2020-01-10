from src.resources.case import Case
from src.resources.activity import Activity
from src.api.customer.customer_user_api import CustomerUserApi
from src.api.customer.checkout_user_api import CheckoutUserApi
from src.bases.customer_user_basis import customer_user_basis
from src.api.api_methods import ApiMethods as apim

def checkout_user_of_customer_user(case):
    case.log_name("Checkout user of customer user")
    case.testrail_config(case.activity.variables.run_number, 1850)

    try:
        cua = CustomerUserApi(case)
        chua = CheckoutUserApi(case)

        response_customer_user = customer_user_basis(case)
        customer_user_body = response_customer_user["customerUser"]
        customer_user_id = response_customer_user["customerUserId"]

        edit_customer_user_body = apim.get_dto("customer_user_dto.json")
        edit_customer_user_body["firstName"] = customer_user_body["firstName"]+"edit"
        edit_customer_user_body["lastName"] = customer_user_body["lastName"]+"edit"
        edit_customer_user_body["email"] = customer_user_body["email"]
        edit_customer_user_body["id"] = customer_user_id

        first_number = chua.checkout_user_should_be_present(customer_user_body.copy())
        cua.update_customer_user(edit_customer_user_body.copy())
        second_number = chua.checkout_user_should_be_present(edit_customer_user_body.copy())
        assert first_number == second_number, "The number of checkout users is changed after update"
        chua.checkout_user_should_not_be_present(customer_user_body.copy())
        cua.delete_customer_user(customer_user_id)
        third_number = chua.checkout_user_should_not_be_present(edit_customer_user_body.copy())
        assert third_number == second_number-1, "The number of checkout users after removing should be less by 1 than before"

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    checkout_user_of_customer_user(Case(Activity(api_test=True)))