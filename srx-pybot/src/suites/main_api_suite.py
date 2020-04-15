from src.resources.case import Case
from src.resources.activity import Activity
from src.cases.api import *
import traceback

if __name__ == "__main__":
    #api tests
    try:
        api_activity = Activity(api_test=True)

        zero_transaction_qty(Case(api_activity, 'SUITE'))
        checkout_user_of_customer_user(Case(api_activity, 'SUITE'))
        delete_location_by_change_doortype(Case(api_activity, 'SUITE'))
        create_transaction_for_noweight_locker(Case(api_activity, 'SUITE'))
        universal_catalog_by_distributor_catalog(Case(api_activity, 'SUITE'))
        no_empty_products_in_universal_catalog(Case(api_activity, 'SUITE'))
        total_triggers_include_all_movement_statuses(Case(api_activity, 'SUITE'))
        label_wake_up(Case(api_activity, 'SUITE'))
        noweight_locker_wake_up(Case(api_activity, 'SUITE'))
        full_rfid_available_flow(Case(api_activity, 'SUITE'))
        full_return_rfid_available_flow(Case(api_activity, 'SUITE'))
        create_rfid_transaction_as_issued(Case(api_activity, 'SUITE'))
        create_rfid_transaction_at_min(Case(api_activity, 'SUITE'))
        smart_shelves_change_door(Case(api_activity, 'SUITE'))
        remove_locker_from_smart_shelf(Case(api_activity, 'SUITE'))
        smart_shelves_delete_check_locker(Case(api_activity, 'SUITE'))
        create_location_for_asset(Case(api_activity, 'SUITE'))

        api_activity.logger.output_suite_result()
        api_activity.finish_activity()
    except:
        print(str(traceback.format_exc()))