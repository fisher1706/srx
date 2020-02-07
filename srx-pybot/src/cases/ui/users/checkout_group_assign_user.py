from src.pages.sub.login_page import LoginPage
from src.pages.customer.checkout_groups_page import CheckoutGroupsPage
from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.api.customer.customer_user_api import CustomerUserApi
from src.bases.checkout_group_basis import checkout_group_basis
from src.bases.customer_user_basis import customer_user_basis
from src.resources.case import Case
from src.resources.activity import Activity

def checkout_group_assign_user(case):
    case.log_name("Assign user to the checkout group")
    case.testrail_config(case.activity.variables.run_number, 1890)

    try:
        lp = LoginPage(case.activity)
        cgp = CheckoutGroupsPage(case.activity)
        cga = CheckoutGroupApi(case)
        ua = CustomerUserApi(case)

        checkout_group = checkout_group_basis(case)
        customer_user = customer_user_basis(case)

        lp.log_in_customer_portal()
        cgp.sidebar_users_and_groups()
        cgp.click_xpath(cgp.locators.xpath_button_tab_by_name("Checkout Groups"))
        row = cgp.scan_table(checkout_group["name"], "Checkout Group Name", pagination=False)
        cgp.click_xpath(cgp.locators.xpath_by_count(cgp.locators.title_associated_users, row))
        cgp.assign_user(customer_user["customerUser"]["email"])
        cgp.check_assigned_user(customer_user["customerUser"], 1)

        cgp.sidebar_users_and_groups()
        cgp.click_xpath(cgp.locators.xpath_button_tab_by_name("Fobs & Passcodes"))
        row = cgp.scan_table(customer_user["customerUser"]["email"], "Email", pagination=False)
        cgp.wait_until_page_loaded()
        cgp.check_table_item_by_header(row, "Checkout Group", checkout_group["name"])

        cgp.click_xpath(cgp.locators.xpath_button_tab_by_name("Checkout Groups"))
        row = cgp.scan_table(checkout_group["name"], "Checkout Group Name", pagination=False)
        cgp.click_xpath(cgp.locators.xpath_by_count(cgp.locators.title_associated_users, row))
        cgp.unassign_user(1)
        cgp.should_be_present_xpath(cgp.locators.xpath_no_data_found)

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        cga.delete_checkout_group(checkout_group["id"])
        ua.delete_customer_user(customer_user["customerUserId"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    checkout_group_assign_user(Case(Activity()))