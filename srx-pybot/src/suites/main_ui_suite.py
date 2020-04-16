from src.resources.case import Case
from src.resources.activity import Activity
from src.cases.ui import *
import traceback

if __name__ == "__main__":
    #ui tests
    try:
        activity = Activity()

        invalid_admin_login(Case(activity))
        valid_admin_login(Case(activity))
        # reset_admin_password(Case(activity))
        # iothub_crud(Case(activity))
        # common_set_of_hubs_for_locker_and_vending(Case(activity))
        # vmi_list_partial_sku_match(Case(activity))
        # distributor_user_crud(Case(activity))
        # distributor_super_user_crud(Case(activity))
        # warehouse_crud(Case(activity))
        # customer_crud(Case(activity))
        # shipto_crud(Case(activity))
        # product_crud(Case(activity))
        # product_import(Case(activity))
        # pricing_import(Case(activity))
        # usage_history_import(Case(activity))
        # document_import(Case(activity))
        # customer_user_crud(Case(activity))
        # different_multiple_po_number(Case(activity))
        # general_multiple_po_number(Case(activity))
        # allocation_code_crud(Case(activity))
        # checkout_user_crud(Case(activity))
        # checkout_user_import_without_group(Case(activity))
        # change_locker_doortype(Case(activity))
        # create_noweight_locker_location_via_planogram(Case(activity))
        # universal_catalog_crud(Case(activity))
        # universal_catalog_import(Case(activity))
        # checkout_group_crud(Case(activity))
        # checkout_group_assign_shipto(Case(activity))
        # checkout_group_assign_user(Case(activity))
        # distributor_crud(Case(activity))
        # shipto_fee_levels(Case(activity))
        # rfid_label_crud(Case(activity))
        # smart_shelves_crud(Case(activity))
        # smart_shelves_merge_cells(Case(activity))
        # smart_shelves_without_weights(Case(activity))
        # smart_shelves_unavailable_door(Case(activity))
        # smart_shelves_remove_locker_distributor(Case(activity))
        # smart_shelves_assign_to_several_lockers(Case(activity))
        # smart_shelves_edit_dist_portal(Case(activity))
        # smart_shelves_merge_cells_distributor(Case(activity))
        # locker_planogram(Case(activity))
        # planogram_assign_smart_shelf(Case(activity))
        # smart_shelves_assign_via_hardware_check_planogram(Case(activity))
        # planogram_merge_split_cells(Case(activity))
        # planogram_without_weights_assign_smart_shelf(Case(activity))
        # smart_shelf_move_locker_to_another_distributor(Case(activity))

    except:
        print(str(traceback.format_exc()))