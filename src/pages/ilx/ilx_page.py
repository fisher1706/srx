import time
from src.pages.ilx_base_page import IlxBase
from src.resources.locator_ilx import LocatorIlx


class IlxPage(IlxBase):

    def login_ilx(self):
        self.open_browser()
        self.is_visible('name', LocatorIlx.ilx_email).send_keys(self.ilx_context.ilx_email)
        self.is_visible('name', LocatorIlx.ilx_password).send_keys(self.ilx_context.ilx_password)
        self.is_visible('class_name', LocatorIlx.button).click()
        el = self.is_visible('xpath', LocatorIlx.user_email)
        assert str(el.text) == self.ilx_context.ilx_email, 'Can not login to ILX!'

    def create_group(self, group):
        self.are_visible('class_name', LocatorIlx.button)[0].click()
        self.is_visible('name', LocatorIlx.group_name).send_keys(group)
        self.is_visible('name', LocatorIlx.group_path).send_keys(group)
        self.is_visible('xpath', LocatorIlx.group_create).click()
        time.sleep (2)

        return self.get_data_group_after(group)

    def create_integration(self):
        pass

    def create_connection(self):
        pass

    def delete_group(self, data):
        group_id = data.get('id')
        group_name = data.get('name')

        if group_name.find('\n') > 0:
            self.is_visible('id', group_id).click()
            self.is_visible('xpath', LocatorIlx.before_button_remove_from_group).click()
            self.is_visible('xpath', LocatorIlx.button_remove_from_group).click()
            self.is_visible('xpath', LocatorIlx.remove_from_group).send_keys('Remove')
            self.is_visible('xpath', LocatorIlx.after_button_remove_from_group).click()
            time.sleep(3)

        self.move_to_element('id', group_id)
        xpath = f'//*[@id="{group_id}"]/span/div/div[2]/button/span[1]'
        self.is_visible('xpath', xpath).click()
        self.is_visible('xpath', LocatorIlx.group_delete).click()
        self.is_visible ('name', LocatorIlx.confirm).send_keys('Delete')
        self.is_visible ('xpath', LocatorIlx.button_group_del).click()
        time.sleep(3)

        return self.get_data_group_after(group_name)

    def edit_group(self, data):
        group_id = data.get('id')
        group_name = data.get("name")
        new_name = f'{group_name}-edit'

        self.move_to_element('id', group_id)
        xpath = f'//*[@id="{group_id}"]/span/div/div[2]/button/span[1]'
        self.is_visible('xpath', xpath).click()
        self.is_visible('xpath', LocatorIlx.group_edit).click()
        self.is_visible('xpath', LocatorIlx.input_group_edit).send_keys('-edit')
        self.is_visible('xpath', LocatorIlx.input_path_edit).send_keys('-edit')
        self.is_present('xpath', LocatorIlx.save_edit_group).click()
        time.sleep(3)

        return self.get_data_group_after(new_name)

    def delete_integration(self):
        pass

    def delete_connection(self):
        pass

    def get_data_group(self):
        elements = self.are_visible('class_name', LocatorIlx.data)
        data = self.get_elements_data(elements)
        return data

    def get_data_group_after(self, group):
        elements = self.are_visible('class_name', LocatorIlx.data)
        resp = self.get_element_text_by_text(elements, group)
        return resp

    def create_access_key(self, access_key):
        self.is_visible ('xpath', LocatorIlx.access).click()
        self.is_visible ('xpath', LocatorIlx.access_before).click()
        self.is_visible ('xpath', LocatorIlx.button_access_key).click()
        self.is_visible ('xpath', LocatorIlx.input_access_key).send_keys(access_key)
        self.is_visible ('xpath', LocatorIlx.create_access_key).click()

        return self.is_visible('xpath', LocatorIlx.created_key).text

