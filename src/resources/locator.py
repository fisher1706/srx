class Locator():
    'The class contains all base locators'

    #IDs
    id_email = "email"
    id_password = "password"
    id_enter_here = "redirectButton"
    id_add_button = "item-action-add"
    id_item_action_customer_add = "item-action-customer-add"
    id_file_upload = "file-upload"
    id_upload_rfid_csv = "upload-rfid-csv"
    id_upload_rfid_available = "upload-rfid-available"
    id_intercom_container = "intercom-container"
    id_drop_down_button = "dropDownButton"
    id_new_password = "newPassword"
    id_confirm_password = "confirmPassword"
    id_item_action_import = "item-action-import"

    #XPATHs
    xpath_forgot_password = "//a[text()='Reset my password']"
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
    xpath_pagination_navigation = "//nav[@aria-label='pagination navigation']"
    xpath_continue_import = "//button/span[text()='Continue import']"
    xpath_successfully_imported_msg = "//span[@id='client-snackbar']//strong[text()='Successfully imported']"
    xpath_successfully_uploaded_document_msg = "//span[text()='Document uploaded successfully!']"
    xpath_successfully_submitted_reorder_list = "//span[text()='Reorder list was successfully submitted']"
    xpath_button = "//div[@role='button']"
    xpath_button_type = "//button[@type='button']"
    xpath_button_save = "//button[@label='Save']"
    xpath_role_row = "//div[@role='row']"
    xpath_last_role_row = f"({xpath_role_row})[last()]"
    xpath_role_cell = "//div[@role='cell']"
    xpath_replenishment_item = "//div[@data-testid='replenishment-item']"
    xpath_replenishment_item_sku = "//div[@data-testid='part-sku']"
    xpath_submit_reorder_list_button = "//button/span[text()='Submit']"
    xpath_save_button = "//button/span[text()='Save']"
    xpath_cancel_button = "//button[@label='Cancel']"
    xpath_type_text = "//input[@type='text']"
    xpath_assign_product_planogram = "//button[@type='button']/span[text()='ASSIGN PRODUCT']"
    xpath_no_data_found = "//div[text()='No data found']"
    xpath_close_button = "//button[@data-testid='close-button']"
    xpath_role_presentation = "//div[@role='presentation']"
    xpath_label_confirm = "//button[@label='Confirm']"
    xpath_label_cancel = "//button[@label='Cancel']"
    xpath_progress_bar = "//div[@role='progressbar']"
    xpath_issue_button = "//span[text()='Issue']/../button"
    xpath_ping_to_return = "//span[text()='Request to return']/../../button"
    xpath_edit_button = "//button[@data-testid='edit-button']"
    xpath_remove_button = "//button[@data-testid='remove-button']"
    xpath_planogram_button = "//button[@data-testid='planogram-button']"
    xpath_unassign_button = "//button[@data-testid='unassign-button']"
    xpath_customer_info_button = "//button[@data-testid='customer-info-button']"
    xpath_shipto_info_button = "//button[@data-testid='shipto-info-button']"
    xpath_associated_shiptos = "//button[@data-testid='associated-shiptos-button']"
    xpath_associated_users = "//button[@data-testid='associated-users-button']"
    xpath_configure_button = "//button[@data-testid='configure-button']"
    xpath_view_button = "//button[@data-testid='view-button']"
    xpath_select_button = "//button[@data-testid='select-button']"
    xpath_edit_status_button = "//button[@data-testid='edit-status-button']"
    xpath_split_button = "//button[@data-testid='split-button']"
    xpath_role_menu = "//ul[@role='menu']"
    xpath_role_menuitem = "//li[@role='menuitem']"
    xpath_check_mark = "//span[text()='✓']"
    xpath_next = "//button/span[text()='Next']"
    xpath_complete_button = "//button/span[text()='Complete']"
    xpath_sign_out = "//div[text()='Sign Out']"
    xpath_reset_password = "//div[text()='Reset password']"
    xpath_actions_button = "//button[@data-testid='sticky-last-more-button']"
    xpath_listbox = "//div[@aria-haspopup='listbox']/.."
    xpath_role_listbox = "//ul[@role='listbox']"
    xapth_button_last_page = "//button[@aria-label='Go to last page']"
    xpath_reload_button = "//button[@data-testid='reload-button']"

    @staticmethod
    def xpath_by_count(xpath, count):
        return f"({xpath})[{count}]"

    @staticmethod
    def xpath_checkbox_in_dialog(index):
        return Locator.xpath_by_count(Locator.xpath_dialog+Locator.xpath_checkbox, index)

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
    def xpath_get_table_item(row, column):
        return f"(({Locator.xpath_role_row})[{row}]{Locator.xpath_role_cell})[{column}]"

    @staticmethod
    def xpath_get_last_table_item(column):
        return f"(({Locator.xpath_role_row})[last()]{Locator.xpath_role_cell})[{column}]"

    @staticmethod
    def xpath_get_row_by_index(index):
        return f"//div[@role='row' and @data-row-index='{index}']"

    @staticmethod
    def xpath_get_table_item_by_index(index, column):
        return f"//div[@role='row' and @data-row-index='{index}']{Locator.xpath_role_cell}[{column}]"

    @staticmethod
    def xpath_table_item_in_dialog(row, column):
        return f"(({Locator.xpath_dialog}{Locator.xpath_table_row})[{row}]{Locator.xpath_table_column})[{column}]"

    @staticmethod
    def xpath_button_by_name(name):
        return f"//button[@type='button']//span[text()='{name}']"

    @staticmethod
    def xpath_planogram(door, cell):
        return f"//div[@data-door='{door}']//div[@data-cell='{cell}']"

    @staticmethod
    def xpath_dropdown_sku(sku):
        return f"{Locator.xpath_dropdown_list_item}//span[text()='{sku}']/../.."

    @staticmethod
    def xpath_select_pagination(value):
        return f"{Locator.xpath_role_listbox}/li[@data-value='{value}']"

    def __setattr__(self, key, value):
        if hasattr(key):
            object.__setattr__(key, value)
        else:
            raise TypeError("Cannot create new attribute for class Locator")
