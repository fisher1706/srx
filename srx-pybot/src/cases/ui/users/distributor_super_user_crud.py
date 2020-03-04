from src.pages.sub.login_page import LoginPage
from src.pages.distributor.distributor_users_page import DistributorUsersPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.tools import Tools

def distributor_super_user_crud(case):
    case.log_name("Distributor super user CRUD")
    case.testrail_config(case.activity.variables.run_number, 30)

    try:
        lp = LoginPage(case.activity)
        dup = DistributorUsersPage(case.activity)

        #-------------------
        email = Tools.random_email()
        first_name = "my Super First"
        last_name = "my Super Last"
        #-------------------
        edit_first_name = "my Super Edit First"
        edit_last_name = "my Super Edit Last"
        #-------------------

        lp.log_in_distributor_portal()
        dup.sidebar_users()
        dup.click_xpath(case.activity.locators.xpath_button_tab_by_name("Super Users"))
        dup.create_distributor_super_user(email=email, first_name=first_name, last_name=last_name)
        dup.check_last_distributor_super_user(email=email, first_name=first_name, last_name=last_name)
        dup.update_last_distributor_super_user(first_name=edit_first_name, last_name=edit_last_name)
        dup.check_last_distributor_super_user(email=email, first_name=edit_first_name, last_name=edit_last_name)
        dup.delete_last_distributor_super_user()
        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    distributor_super_user_crud(Case(Activity()))