from src.resources.case import Case
from src.resources.activity import Activity
from src.cases.api import *

if __name__ == "__main__":
    #api tests
    api_activity = Activity(api_test=True)

    zero_transaction_qty(Case(api_activity, 'SUITE'))
    checkout_user_of_customer_user(Case(api_activity, 'SUITE'))
    delete_location_by_change_doortype(Case(api_activity, 'SUITE'))
    create_transaction_for_noweight_locker(Case(api_activity, 'SUITE'))
    universal_catalog_by_distributor_catalog(Case(api_activity, 'SUITE'))

    api_activity.logger.output_suite_result()
    api_activity.finish_activity()