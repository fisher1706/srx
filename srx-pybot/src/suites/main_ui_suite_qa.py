from src.resources.case import Case
from src.resources.activity import Activity
from src.cases.ui import *

if __name__ == "__main__":
    #ui tests
    activity = Activity()

    invalid_admin_login(Case(activity,'SUITE'))
    valid_admin_login(Case(activity,'SUITE'))
    reset_admin_password(Case(activity,'SUITE'))
    iothub_crud(Case(activity,'SUITE'))
    common_set_of_hubs_for_locker_and_vending(Case(activity,'SUITE'))
    vmi_list_partial_sku_match(Case(activity,'SUITE'))
    distributor_user_crud(Case(activity,'SUITE'))
    distributor_super_user_crud(Case(activity,'SUITE'))
    warehouse_crud(Case(activity,'SUITE'))
    customer_crud(Case(activity,'SUITE'))
    shipto_crud(Case(activity,'SUITE'))
    product_crud(Case(activity, 'SUITE'))
    product_import(Case(activity, 'SUITE'))
    pricing_import(Case(activity, 'SUITE'))
    usage_history_import(Case(activity, 'SUITE'))
    document_import(Case(activity, 'SUITE'))
    customer_user_crud(Case(activity, 'SUITE'))
    different_multiple_po_number(Case(activity, 'SUITE'))
    general_multiple_po_number(Case(activity, 'SUITE'))
    allocation_code_crud(Case(activity, 'SUITE'))
    checkout_user_crud(Case(activity, 'SUITE'))

    activity.logger.output_suite_result()
    activity.finish_activity()