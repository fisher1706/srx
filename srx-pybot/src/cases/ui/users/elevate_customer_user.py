from src.pages.sub.login_page import LoginPage
from src.pages.distributor.distributor_customer_users_page import DistributorCustomerUsersPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.email import Email
from src.api.distributor.customer_api import CustomerApi
from src.bases import customer_basis

def elevate_customer_user(case):
    case.log_name("Elevate customer user")
    #case.testrail_config(case.activity.variables.run_number, 28)

    try:
        lp = LoginPage(case.activity)
        dcup = DistributorCustomerUsersPage(case.activity)
        ca = CustomerApi(case)
        
        #email = Email(case)
        #email.mark_all_emails_as_seen()
        #ca.get_distributor_token(lp.variables.secondary_distributor_email, lp.variables.secondary_distributor_password)
        #customer_response = customer_basis(case)


        #lp.log_in_distributor_portal(lp.variables.secondary_distributor_email, lp.variables.secondary_distributor_password)
        #dcup.follow_customer_users_url(customer_response["customerId"])
        
        #lp.accept_invite(email.get_accept_invite_url_from_last_email())

        #ca.delete_customer(customer_response["warehouseId"], customer_response["customerId"])

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    distributor_user_crud(Case(Activity()))