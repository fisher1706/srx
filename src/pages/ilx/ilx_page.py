#pylint: disable=C0301
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

        return self.get_elements(group)

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
        self.is_visible('xpath', LocatorIlx.connect_type).click()
        self.are_visible ('tag_name', LocatorIlx.tag_name)[-1].click()
        self.is_present('xpath', LocatorIlx.save_edit_group).click()
        time.sleep(3)

        return self.get_elements(new_name)

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

        return self.get_elements(group_name)

    def create_integration(self, integration):
        self.are_visible('class_name', LocatorIlx.button)[1].click()
        self.is_visible('xpath', LocatorIlx.int_template).click()
        self.are_visible ('tag_name', LocatorIlx.tag_name)[-1].click()
        self.is_visible('name', LocatorIlx.group_name).send_keys(integration)
        self.is_visible('name', LocatorIlx.int_base_path).send_keys(integration)
        self.is_visible('name', LocatorIlx.int_group_path).send_keys(integration)
        self.is_visible('xpath', LocatorIlx.button_create_int).click()
        time.sleep(2)
        data = self.are_present('tag_name', LocatorIlx.tag_name)

        return self.get_element_text_by_text(data, integration)

    def edit_integration(self):
        self.is_visible('xpath', LocatorIlx.button_int).click()

        """edit name"""
        self.is_visible('xpath', LocatorIlx.button_edit_int).click()
        self.is_visible('xpath', LocatorIlx.int_name).send_keys('-edit')
        self.is_visible('xpath', LocatorIlx.button_int_save).click()

        """add api key"""
        self.is_visible('xpath', LocatorIlx.int_description).click()
        self.is_visible('xpath', LocatorIlx.int_auth).click()
        self.is_visible ('xpath', LocatorIlx.open_chose_key).click()
        self.are_visible ('tag_name', LocatorIlx.tag_name)[-1].click()

        try:
            self.is_visible ('xpath', LocatorIlx.save_api_key).click()
        except:
            self.is_visible ('xpath', LocatorIlx.open_chose_key).click ()
            self.are_visible ('tag_name', LocatorIlx.tag_name)[-2].click ()
            self.is_visible ('xpath', LocatorIlx.save_api_key).click ()
            time.sleep(2)

        self.is_visible('xpath', LocatorIlx.return_to_int).click()
        time.sleep(3)
        name = self.is_visible('xpath', LocatorIlx.name_int)

        return name.text

    def add_to_group(self):
        self.is_visible('xpath', LocatorIlx.edit_int).click()
        self.is_visible('xpath', LocatorIlx.add_to_group).click()
        self.are_visible('class_name', LocatorIlx.chose_group)[-1].click()
        self.is_visible('xpath', LocatorIlx.button_add_int).click()
        time.sleep(3)

    def add_to_connection(self):
        self.is_visible('xpath', LocatorIlx.chose_endpoint).click()
        self.is_visible('xpath', LocatorIlx.button_int).click()
        self.is_visible('xpath', LocatorIlx.select_connect).click()
        self.is_visible('xpath', LocatorIlx.int_auth).click()
        self.is_visible('xpath', LocatorIlx.open_chose_key).click()
        time.sleep(2)
        self.are_visible('tag_name', LocatorIlx.tag_name)[6].click()
        time.sleep(2)

        try:
            self.is_visible('xpath', LocatorIlx.save_api_key).click()
        except:
            self.is_visible('xpath', LocatorIlx.open_chose_key).click()
            self.are_visible('tag_name', LocatorIlx.tag_name)[5].click()
            time.sleep (2)
            self.is_visible('xpath', LocatorIlx.save_api_key).click()

        el = self.is_visible('xpath', LocatorIlx.get_connect)

        return el.text

    def move_to_group(self):
        try:
            self.is_visible('xpath', LocatorIlx.edit_group_first).click()
        except:
            self.is_visible('xpath', LocatorIlx.edit_group_second).click()
        self.is_visible('xpath', LocatorIlx.move_to_group).click()
        self.are_visible('class_name', LocatorIlx.chose_move_group)[0].click()
        self.is_visible('xpath', LocatorIlx.move_int).click()
        time.sleep(3)

    def remove_from_group(self):
        try:
            self.is_visible('xpath', LocatorIlx.edit_group_first).click()
        except:
            self.is_visible('xpath', LocatorIlx.edit_group_second).click()
        self.is_visible('xpath', LocatorIlx.remove_int_from_group).click()
        self.is_visible('xpath', LocatorIlx.confirm_remove_int).send_keys('Remove')
        self.is_visible('xpath', LocatorIlx.button_remove_int).click()
        time.sleep (3)

    def delete_from_group(self):
        try:
            self.is_visible('xpath', LocatorIlx.edit_group_first).click()
        except:
            self.is_visible('xpath', LocatorIlx.edit_group_second).click()
        self.is_visible('xpath', LocatorIlx.del_int_from_group).click()
        self.is_visible('xpath', LocatorIlx.confirm_delete_from_group).send_keys('Delete')
        self.is_visible('xpath', LocatorIlx.delete_int_from_group).click()
        time.sleep(3)

    def delete_integration(self):
        self.is_visible('xpath', LocatorIlx.edit_int).click()
        self.is_visible('xpath', LocatorIlx.delete_int_first).click()
        self.is_visible('xpath', LocatorIlx.confirm_delete_int).send_keys('Delete')
        self.is_visible('xpath', LocatorIlx.delete_int_second).click()
        time.sleep(3)

    def create_connection(self, connect):
        self.is_visible('xpath', LocatorIlx.access).click()
        self.is_visible('xpath', LocatorIlx.connection).click()
        self.is_visible('xpath', LocatorIlx.new_connection).click()
        self.is_visible('xpath', LocatorIlx.connection_name).send_keys(connect)
        self.is_visible('xpath', LocatorIlx.connection_url).send_keys('http://3.94.89.202:81/')
        self.is_visible('xpath', LocatorIlx.connect_type).click()
        self.is_visible('xpath', LocatorIlx.chose_connect_type).click()
        self.is_visible('xpath', LocatorIlx.client_id).send_keys(connect)
        self.is_visible('xpath', LocatorIlx.user_name).send_keys(connect)
        self.is_visible('xpath', LocatorIlx.client_secret).send_keys(connect)
        self.is_visible('xpath', LocatorIlx.connect_passwd).send_keys(connect)
        self.is_visible('xpath', LocatorIlx.token_url).send_keys('http://3.94.89.202:81/')
        self.is_visible('xpath', LocatorIlx.connection_save).click()
        time.sleep(3)

        el = self.is_visible('xpath', LocatorIlx.connect_name)

        return el

    def delete_connection(self):
        self.is_visible ('xpath', LocatorIlx.access).click ()
        self.is_visible ('xpath', LocatorIlx.connection).click()
        self.is_visible ('xpath', LocatorIlx.connect_chose).click()

        try:
            self.is_visible ('xpath', LocatorIlx.connect_delete).click()
        except:
            self.refresh_browser()

            self.is_visible('xpath', LocatorIlx.chose_connect).click()
            self.is_visible('xpath', LocatorIlx.chose_int).click()
            self.is_visible('xpath', LocatorIlx.chose_dest_endpoint).click()
            self.is_visible('xpath', LocatorIlx.int_auth).click()
            self.is_visible('xpath', LocatorIlx.open_chose_key).click()
            time.sleep(2)

            self.are_present('tag_name', LocatorIlx.tag_name)[5].click()
            self.is_visible('xpath', LocatorIlx.save_api_key).click()
            time.sleep(5)

            self.is_visible('xpath', LocatorIlx.connection).click()
            self.is_visible('xpath', LocatorIlx.connect_chose).click()
            self.is_visible('xpath', LocatorIlx.connect_delete).click()

        self.is_visible('xpath', LocatorIlx.confirm_delete_connect).send_keys('Delete')
        self.is_visible('xpath', LocatorIlx.connect_save).click()
        time.sleep(3)
        self.is_visible ('xpath', LocatorIlx.data_connects).click()

    def edit_connection(self):
        self.is_visible('xpath', LocatorIlx.access).click()
        self.is_visible('xpath', LocatorIlx.connection).click()
        self.is_visible ('xpath', LocatorIlx.connect_chose).click()
        self.is_visible('xpath', LocatorIlx.edit_connect).click()
        self.is_visible ('xpath', LocatorIlx.connection_name).send_keys('-edit')
        self.is_visible ('xpath', LocatorIlx.connection_save).click()
        time.sleep (5)

        name = self.is_visible('xpath', LocatorIlx.connect_name_text)

        return name.text

    def get_connections(self):
        el = self.is_visible('xpath', LocatorIlx.data_connects)
        if el.get_attribute('class').find('jss49') < 0:
            self.is_visible('xpath', LocatorIlx.data_connects).click()
        time.sleep(5)
        self.is_visible('xpath', LocatorIlx.connection).click()

        try:
            con = self.are_visible('id', 'Connections')
            resp = len(con)
        except:
            resp = 0

        self.is_visible('xpath', LocatorIlx.access).click()

        return resp

    def get_data_group(self):
        elements = self.are_visible('class_name', LocatorIlx.data)
        data = self.get_elements_data(elements)

        return data

    def get_elements(self, group):
        elements = self.are_visible('class_name', LocatorIlx.data)
        resp = self.get_element_text_by_text(elements, group)

        return resp

    def create_access_key(self, access_key):
        self.is_visible('xpath', LocatorIlx.access).click()
        self.is_visible('xpath', LocatorIlx.access_before).click()
        self.is_visible('xpath', LocatorIlx.button_access_key).click()
        self.is_visible('xpath', LocatorIlx.input_access_key).send_keys(access_key)
        self.is_visible('xpath', LocatorIlx.create_access_key).click()
        time.sleep(2)
        el = self.is_visible('xpath', LocatorIlx.access_key_name)

        return el.get_attribute('value')
