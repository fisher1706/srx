import pytest
from src.pages.ilx.ilx_page import IlxPage
from src.pages.ilx.ilx_utils_ui import IlxUtils


@pytest.fixture(scope='function')
def login_ilx(ui_ilx):
    IlxPage(ui_ilx).login_ilx()


@pytest.mark.usefixtures('login_ilx')
class TestGroups:

    def test_create_group(self, ui_ilx):
        group = IlxUtils.generate_name('group')
        resp = IlxPage(ui_ilx).create_group(group)
        assert group == resp, 'group is not created'
    #
    # def test_delete_group(self, ui_ilx):
    #     data_group = IlxPage(ui_ilx).get_data_group()
    #     if len(data_group) <= 2:
    #         self.test_create_group(ui_ilx)
    #     resp = IlxPage(ui_ilx).delete_group(data_group[3])
    #     assert resp is None, 'group is not deleted'

    def test_edit_group(self, ui_ilx):
        data_group = IlxPage(ui_ilx).get_data_group()
        if len(data_group) <= 2:
            self.test_create_group(ui_ilx)
        group = data_group[3].get('name')
        group_new = f'{group}-edit'
        resp = IlxPage(ui_ilx).edit_group(data_group[3])

        assert resp == group_new, 'group is not edited'

    # def test_create_access_key(self, ui_ilx):
    #     access_key = IlxUtils.generate_name('key')
    #     resp = IlxPage(ui_ilx).create_access_key(access_key)
    #     assert str(resp) == 'API keys', 'api key is not created'


@pytest.mark.usefixtures('login_ilx')
class TestIntegrations:
    pass


@pytest.mark.usefixtures('login_ilx')
class TestConnections:
    pass