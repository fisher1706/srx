from src.pages.sub.login_page import LoginPage
from src.pages.customer.checkout_groups_page import CheckoutGroupsPage
from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.api.distributor.shipto_api import ShiptoApi
from src.bases.checkout_group_basis import checkout_group_basis
from src.bases.shipto_basis import shipto_basis
from src.resources.case import Case
from src.resources.activity import Activity

def checkout_group_assign_shipto(case):
    case.log_name("Assign shipto to the checkout group")
    case.testrail_config(case.activity.variables.run_number, 1863)

    try:
        lp = LoginPage(case.activity)
        cgp = CheckoutGroupsPage(case.activity)
        cga = CheckoutGroupApi(case)
        sa = ShiptoApi(case)

        checkout_group = checkout_group_basis(case)
        shipto = shipto_basis(case)

        lp.log_in_customer_portal()
        cgp.sidebar_users_and_groups()
        cgp.click_xpath(cgp.locators.xpath_button_tab_by_name("Checkout Groups"))
        row = cgp.scan_table(checkout_group["name"], "Checkout Group Name", pagination=False)
        cgp.click_xpath(cgp.locators.xpath_by_count(cgp.locators.title_associated_shiptos, row))
        cgp.assign_shipto(shipto["shipto"]["number"])
        cgp.check_assigned_shipto(shipto["shipto"], 1)
        cgp.unassign_shipto(1)
        cgp.should_be_present_xpath(cgp.locators.xpath_no_data_found)

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        cga.delete_checkout_group(checkout_group["id"])
        sa.delete_shipto(shipto["shipto_number"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    checkout_group_assign_shipto(Case(Activity()))