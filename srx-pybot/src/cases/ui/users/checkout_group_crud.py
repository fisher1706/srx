from src.pages.sub.login_page import LoginPage
from src.pages.customer.checkout_groups_page import CheckoutGroupsPage
from src.resources.case import Case
from src.resources.activity import Activity

def checkout_group_crud(case):
    case.log_name("Checkout group CRUD")
    case.testrail_config(case.activity.variables.run_number, 1861)

    try:
        lp = LoginPage(case.activity)
        cgp = CheckoutGroupsPage(case.activity)
        checkout_group_body = cgp.checkout_group_body.copy()
        edit_checkout_group_body = cgp.checkout_group_body.copy()

        #-------------------
        checkout_group_body["name"] = f"Name {case.random_string_l()}"
        checkout_group_body["email"] = case.random_email()
        #-------------------
        edit_checkout_group_body["name"] = f"Edit name {case.random_string_l()}"
        #-------------------

        lp.log_in_customer_portal()
        cgp.sidebar_users_and_groups()
        cgp.click_xpath(case.activity.locators.xpath_button_tab_by_name("Checkout Groups"))
        cgp.create_checkout_group(checkout_group_body.copy())
        row = cgp.scan_table(checkout_group_body["name"], "Checkout Group Name", pagination=False)
        cgp.check_new_checkout_group(checkout_group_body.copy(), row)
        cgp.update_new_checkout_group(edit_checkout_group_body.copy(), row)
        cgp.sidebar_users_and_groups()
        cgp.click_xpath(case.activity.locators.xpath_button_tab_by_name("Checkout Groups"))
        cgp.wait_until_page_loaded()
        row = cgp.scan_table(edit_checkout_group_body["name"], "Checkout Group Name", pagination=False)
        cgp.check_new_checkout_group(edit_checkout_group_body.copy(), row)
        cgp.delete_new_checkout_group(row)

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    checkout_group_crud(Case(Activity()))