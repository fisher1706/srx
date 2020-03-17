class Locators():
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

    #TITLEs
    title_edit_user = "//span[@title='Edit User']/button"
    title_delete_user = "//span[@title='Delete User']/button"
    title_edit_super_user = "//span[@title='Edit Super User']/button"
    title_delete_super_user = "//span[@title='Delete Super User']/button"
    title_edit_warehouse = "//span[@title='Edit Warehouse']/button"
    title_delete_warehouse = "//span[@title='Delete Warehouse']/button"
    title_customer_info = "//button[@title='Customer info']"
    title_delete_customer = "//span[@title='Delete Customer']/button"
    title_edit_product = "//span[@title='Edit Product']/button"
    title_delete_document = "//span[@title='Delete document']/button"
    title_delete_allocation_code = "//span[@title='Delete Allocation Code']/button"
    title_manage_customer_users = "//button[@title='Manage Customer users']"
    title_shipto_info = "//button[@title='Shipto info']"
    title_delete_shipto = "//span[@title='Delete Shipto']/button"
    title_delete_checkout_user = "//span[@title='Delete Checkout User']/button"
    title_delete_checkout_group = "//span[@title='Delete Checkout Group']/button"
    title_update_utc_and_gtin = "//span[@title='Edit UPC & GTIN']/button"
    title_delete_utc_and_gtin = "//span[@title='Delete UPC & GTIN']/button"
    title_associated_shiptos = "//button[@id='shiptos-button']"
    title_associated_users = "//button[@title='Associated Users']"
    title_delete_associated_shipto = "//span[@title='Delete Associated Shipto']/button"
    title_delete_associated_user = "//span[@title='Delete Associated User']/button"
    title_edit_iothub = "//span[@title='Edit IoTHub']/button"
    title_delete_iothub = "//span[@title='Delete IoTHub']/button"
    title_delete_locker = "//span[@title='Delete Locker']/button"
    title_delete_vending = "//span[@title='Delete Vending']/button"
    title_configure = "//button[@title='Configure']"
    title_edit_door = "//span[@title='Edit Door']/button"

    def xpath_by_count(self, xpath, count):
        return f"({xpath})[{count}]"

    def xpath_checkbox_in_dialog(self, index):
        return self.xpath_by_count(self.xpath_dialog+self.xpath_checkbox, index)

    def xpath_dropdown_in_dialog(self, index):
        return self.xpath_by_count(self.xpath_select_box, index)

    def xpath_checkbox_in_dialog_by_name(self, name):
        return f"{self.xpath_dialog}//span[text()='{name}']/..//input[@type='checkbox']"

    def xpath_button_tab_by_name(self, name):
        return f"{self.xpath_button_tab}//span[text()='{name}']"

    def xpath_table_item(self, row, column, sub_xpath=""):
        return f"(({sub_xpath}{self.xpath_table_row})[{row}]{self.xpath_table_column})[{column}]"

    def xpath_table_item_in_dialog(self, row, column):
        return f"(({self.xpath_dialog}{self.xpath_table_row})[{row}]{self.xpath_table_column})[{column}]"

    def xpath_button_by_name(self, name):
        return f"//button[@type='button']//span[text()='{name}']"

    def xpath_planogram(self, door, cell):
        return f"//div[@data-door='{door}']//div[@data-cell='{cell}']"