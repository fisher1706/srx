class Locators():
    #IDs
    id_email = "email"
    id_password = "password"
    id_enter_here = "redirectButton"
    id_create_button = "item-action-create"

    #XPATHs
    xpath_forgot_password = "//a[@href='/forgot-password']"
    xpath_submit_button = "//button[@type='submit']"
    xpath_dialog = "//div[@role='dialog']"
    xpath_select_box = "//div[@test-id='select-box']/div"
    xpath_button_tab = "//button[@role='tab']"
    xpath_table_row = "//div[@role='rowgroup']"
    xpath_table_column = "//div[@role='gridcell']"
    xpath_table_header_column = "//div[@role='columnheader']"
    xpath_checkbox = "//input[@type='checkbox']"
    xpath_confirm_button = "//button[@data-testid='confirm-button']"
    xpath_pagination_bottom = "//div[@class='pagination-bottom']"

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

    def xpath_by_count(self, xpath, count):
        return "("+xpath+")["+str(count)+"]"

    def xpath_checkbox_in_dialog(self, index):
        return self.xpath_by_count(self.xpath_dialog+self.xpath_checkbox, index)

    def xpath_dropdown_in_dialog(self, index):
        return self.xpath_by_count(self.xpath_select_box, index)

    def xpath_checkbox_in_dialog_by_name(self, name):
        return self.xpath_dialog+"//span[text()='"+name+"']/..//input[@type='checkbox']"

    def xpath_button_tab_by_name(self, name):
        return self.xpath_button_tab+"//span[text()='"+name+"']"

    def xpath_table_item(self, row, column):
        return "(("+self.xpath_table_row+")["+str(row)+"]"+self.xpath_table_column+")["+str(column)+"]"

    #bootstrap
    class_button_info = "//button[@class='btn btn-info']"
    class_button_ok = "//button[@class='modal-dialog-ok-button btn btn-lg btn-primary']"
    class_button_close = "//button[@class='close']"
    class_button_success = "//button[@class='control-button btn btn-success']"
    class_button_danger = "//button[@class='control-button btn btn-danger']"
    class_button_danger_dialog = "//button[@class='btn btn-danger']"
    class_modal_dialog = "//div[@class='modal-dialog']"
    class_srx_select = "//div[@class='srx-select has-error']"
    class_jumbotron = "//div[@class='jumbotron']"
    class_page_item = "//li[@class='page-item']"
    class_pagination_bar = "//ul[@class='react-bootstrap-table-page-btns-ul pagination']"
    bootstrap_select_box = class_srx_select+"/div"
    bootstrap_table_row = "//tbody/tr"
    bootstrap_table_column = "//td"
    bootstrap_table_header_column = "//th"

    def xpath_table_item_bootstrap(self, row, column):
        return self.bootstrap_table_row+"["+str(row)+"]"+self.bootstrap_table_column+"["+str(column)+"]"

