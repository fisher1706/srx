class Locator():
    #IDs
    id_email = "email"
    id_password = "password"
    id_enter_here = "redirectButton"
    id_add_button = "item-action-add"
    id_file_upload = "file-upload"
    id_intercom_container = "intercom-container"

    #XPATHs
    xpath_forgot_password = "//a[@href='/forgot-password']"
    xpath_submit_button = "//button[@type='submit']"
    xpath_dialog = "//div[@role='dialog']"
    xpath_select_box = "//div[@test-id='select-box']/div"
    xpath_dropdown_list_item = xpath_select_box+"/div[2]/div/div"
    xpath_button_tab = "//button[@role='tab']"
    xpath_table_row = "//div[@role='rowgroup']"
    xpath_table_column = "//div[@role='gridcell']"
    xpath_table_header_column = "//div[@role='columnheader']"
    xpath_table = "//div[@class='rt-table']"
    xpath_checkbox = "//input[@type='checkbox']"
    xpath_confirm_button = "//button[@data-testid='confirm-button']"
    xpath_dialog_cancel_button = "//button[@data-testid='cancel-button']"
    xpath_pagination_bottom = "//div[@class='pagination-bottom']"
    xpath_continue_import = "//button/span[text()='Continue import']"
    xpath_successfully_imported_msg = "//span[@id='client-snackbar']//strong[text()='Successfully imported']"
    xpath_successfully_uploaded_document_msg = "//span[text()='Document uploaded successfully!']"
    xpath_successfully_submitted_reorder_list = "//span[text()='Reorder list was successfully submitted']"
    xpath_button = "//div[@role='button']"
    xpath_button_type = "//button[@type='button']"
    xpath_button_save = "//button[@label='Save']"
    xpath_role_row = "//div[@role='row']"
    xpath_replenishment_item = "//div[@data-testid='replenishment-item']"
    xpath_replenishment_item_sku = "//div[@data-testid='part-sku']"
    xpath_submit_reorder_list_button = "//button/span[text()='Submit']"
    xpath_cancel_button = "//button[@label='Cancel']"
    xpath_type_text = "//input[@type='text']"
    xpath_assign_product_planogram = "//button[@type='button']/span[text()='ASSIGN PRODUCT']"
    xpath_no_data_found = "//div[text()='No data found']"
    xpath_close_button = "//button[@data-testid='close-btn']"
    xpath_role_presentation = "//div[@role='presentation']"
    xpath_label_confirm = "//button[@label='Confirm']"
    xpath_label_cancel = "//button[@label='Cancel']"
    xpath_progress_bar = "//div[@role='progressbar']"
    xpath_issue_button = "//span[text()='Issue']/../button"
    xpath_ping_to_return = "//span[text()='Request to return']/../../button"

    #TITLEs
    title_edit_user = "//span[@title='Edit User']/button"
    title_delete_user = "//span[@title='Delete User']/button"
    title_edit_super_user = "//span[@title='Edit Super User']/button"
    title_delete_super_user = "//span[@title='Delete Super User']/button"
    title_edit_warehouse = "//span[@title='Edit Warehouse']/button"
    title_delete_warehouse = "//span[@title='Delete Warehouse']/button"
    title_customer_info = "//div[@title='Customer info']/button"
    title_delete_customer = "//span[@title='Delete Customer']/button"
    title_edit_product = "//span[@title='Edit Product']/button"
    title_delete_document = "//span[@title='Delete document']/button"
    title_delete_allocation_code = "//span[@title='Delete Allocation Code']/button"
    title_manage_customer_users = "//button[@title='Manage Customer users']"
    title_shipto_info = "//div[@title='Shipto info']/button"
    title_delete_shipto = "//span[@title='Delete Shipto']/button"
    title_delete_checkout_user = "//span[@title='Delete Checkout User']/button"
    title_delete_checkout_group = "//span[@title='Delete Checkout Group']/button"
    title_update_utc_and_gtin = "//span[@title='Edit UPC & GTIN']/button"
    title_delete_utc_and_gtin = "//span[@title='Delete UPC & GTIN']/button"
    title_associated_shiptos = "//button[@id='shiptos-button']"
    title_associated_users = "//div[@title='Associated Users']/button"
    title_delete_associated_shipto = "//span[@title='Delete Associated Shipto']/button"
    title_delete_associated_user = "//span[@title='Delete Associated User']/button"
    title_edit_iothub = "//span[@title='Edit IoTHub']/button"
    title_delete_iothub = "//span[@title='Delete IoTHub']/button"
    title_delete_locker = "//span[@title='Delete Locker']/button"
    title_delete_vending = "//span[@title='Delete Vending']/button"
    title_configure = "//button[@title='Configure']"
    title_delete_distributor = "//span[@title='Delete distributor']/button"
    title_edit_distributor = "//span[@title='Edit distributor']/button"
    title_edit_door = "//span[@title='Edit Door']/button"
    title_undo = "//span[@title='Undo cell edit (Ctrl+Z)']/button"
    title_edit_status = "//span[@title='Edit status']/button"
    title_unassign = "//span[@title='Unassign']/button"
    title_delete_smart_shelves = "//span[@title='Delete Smart Shelf']/button"
    title_edit_smart_shelves = "//span[@title='Edit Smart Shelf']/button"
    title_edit_smart_shelves_dist = "//span[@title='Edit smart shelf']/button"
    title_switch_locker_planogram = "//div[@title='Switch to LOCKER Planogram']/button"
    title_configure_door_number = "//span[@title='Configure Door #1']/button"
    title_go_to_locker_planogram = "//div[@title='Go to LOCKER Planogram']/button"
    title_configure_door = "//span[@title='Configure Door']/button"
    title_delete_security_group = "//span[@title='Delete Security group']/button"
    title_select_item = "//span[@title='Select item']/button"

    @staticmethod
    def xpath_by_count(xpath, count):
        return f"({xpath})[{count}]"

    @staticmethod
    def xpath_checkbox_in_dialog(index):
        return xpath_by_count(Locator.xpath_dialog+Locator.xpath_checkbox, index)

    @staticmethod
    def xpath_dropdown_in_dialog(index):
        return Locator.xpath_by_count(Locator.xpath_select_box, index)

    @staticmethod
    def xpath_checkbox_in_dialog_by_name(name):
        return f"{Locator.xpath_dialog}//span[text()='{name}']/..//input[@type='checkbox']"

    @staticmethod
    def xpath_button_tab_by_name(name):
        return f"{Locator.xpath_button_tab}//span[text()='{name}']"

    @staticmethod
    def xpath_table_item(row, column, sub_xpath=""):
        return f"(({sub_xpath}{Locator.xpath_table_row})[{row}]{Locator.xpath_table_column})[{column}]"

    @staticmethod
    def xpath_table_item_in_dialog(row, column):
        return f"(({Locator.xpath_dialog}{Locator.xpath_table_row})[{row}]{Locator.xpath_table_column})[{column}]"

    @staticmethod
    def xpath_button_by_name(name):
        return f"//button[@type='button']//span[text()='{name}']"

    @staticmethod
    def xpath_planogram(door, cell):
        return f"//div[@data-door='{door}']//div[@data-cell='{cell}']"

    def __setattr__(self, key, value):
        if (not hasattr(key)):
            raise TypeError("Cannot create new attribute for class Locator")
        else:
            object.__setattr__(key, value)
    
    @staticmethod
    def xpath_dropdown_sku(sku):
        return f"{Locator.xpath_dropdown_list_item}//span[text()='{sku}']/../.."