from src.pages.sub.login_page import LoginPage
from src.pages.distributor.distributor_users_page import DistributorUsersPage
from src.resources.case import Case
from src.resources.activity import Activity

def distributor_users_crud(case):
    case.log_name("Distributor users CRUD")
    case.testrail_config(case.activity.variables.run_number, 28)
    lp = LoginPage(case.activity)
    dup = DistributorUsersPage(case.activity)

    email = case.random_email()
    first_name = "my First"
    last_name = "my Last"
    role = "User"
    warehouses = ["Z_Warehouse (9999)", "A_Warehouse (1138)"]
    edit_first_name = "my Edit First"
    edit_last_name = "my Edit Last"
    edit_role = "Static Group"
    edit_warehouses = ["A_Warehouse (1138)"]

    lp.log_in_distributor_portal()
    dup.sidebar_users()
    dup.create_distributor_user(email=email, first_name=first_name, last_name=last_name, role=role, warehouses=warehouses)
    dup.check_last_distributor_user(email=email, first_name=first_name, last_name=last_name, role=role, warehouses=warehouses)
    dup.update_distributor_user(first_name=edit_first_name, last_name=edit_last_name, role=edit_role, warehouses=edit_warehouses)
    dup.check_last_distributor_user(email=email, first_name=edit_first_name, last_name=edit_last_name, role=edit_role, warehouses=edit_warehouses)
    dup.delete_last_distributor_user()
    case.finish_case()

if __name__ == "__main__":
    distributor_users_crud(Case(Activity()))