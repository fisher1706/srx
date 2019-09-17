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

    #TITLEs
    title_edit_user = "//span[@title='Edit User']/button"
    title_delete_user = "//span[@title='Delete User']/button"
    title_edit_super_user = "//span[@title='Edit Super User']/button"
    title_delete_super_user = "//span[@title='Delete Super User']/button"
    title_edit_warehouse = "//span[@title='Edit Warehouse']/button"
    title_delete_warehouse = "//span[@title='Delete Warehouse']/button"

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

