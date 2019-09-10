from src.resources.case import Case
from src.resources.activity import Activity
from src.cases import *

if __name__ == "__main__":
    activity = Activity()

    #tests
    invalid_admin_login(Case(activity,'SUITE'))
    valid_admin_login(Case(activity,'SUITE'))
    reset_admin_password(Case(activity,'SUITE'))
    distributor_users_crud(Case(activity,'SUITE'))

    activity.logger.output_suite_result()
    activity.finish_activity()