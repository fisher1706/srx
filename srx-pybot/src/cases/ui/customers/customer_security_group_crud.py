from src.pages.sub.login_page import LoginPage
from src.pages.customer.users_and_groups_page import UsersGroups
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.tools import Tools

def customer_security_group_crud(case):
    case.log_name("Customer security group CRUD")
    case.testrail_config(2007)

    try:
        lp = LoginPage(case.activity)
        ug = UsersGroups(case.activity)
        security_group_body = ug.security_group_body.copy()
        edit_security_group_body = ug.security_group_body.copy()

        #-------------------
        security_group_body["name"] = Tools.random_string_l(10)
        security_group_body["checked"] = True

        #-------------------
        edit_security_group_body["name"] = Tools.random_string_l(10)
        edit_security_group_body["checked"] = False

        lp.log_in_customer_portal()
        ug.open_security_groups()
        ug.create_security_group(security_group_body)
        row = ug.get_row_of_table_item_by_column(security_group_body["name"], 1)
        ug.check_security_group(security_group_body, row)
        ug.update_security_group(edit_security_group_body, row)
        ug.check_security_group(edit_security_group_body, row)
        ug.delete_security_group(edit_security_group_body, row)

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    customer_security_group_crud(Case(Activity()))