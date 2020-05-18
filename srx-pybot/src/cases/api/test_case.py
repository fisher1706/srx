from src.resources.case import Case
from src.resources.activity import Activity
from src.api.checkout.checkout_api import CheckoutApi


def create_location_for_asset(case):
    case.log_name("test")

    try:
        ca = CheckoutApi(case)

        print(ca.get_cart(passcode=case.activity.variables.passcode))
        #print(ca.get_cart())
        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    create_location_for_asset(Case(Activity(api_test=True)))