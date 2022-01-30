import pytest
from src.pages.ilx.ilx_page import IlxPage
from src.pages.ilx.ilx_utils_ui import IlxUtils


@pytest.fixture(scope='function')
def login_ilx(ui_ilx):
    IlxPage(ui_ilx).login_ilx()


@pytest.mark.usefixtures('login_ilx')
class TestGroups:

    def test_create_access_key(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11393
        access_key = IlxUtils.generate_name('key')
        resp = IlxPage(ui_ilx).create_access_key(access_key)
        assert str(resp) == access_key, 'api key is not created'

    def test_create_group(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11390
        group = IlxUtils.generate_name('group')
        resp = IlxPage(ui_ilx).create_group(group)
        assert group == resp, 'group is not created'

    def test_edit_group(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11391
        data_group = IlxPage(ui_ilx).get_data_group()
        if len(data_group) <= 2:
            self.test_create_group(ui_ilx)
        group = data_group[3].get('name')
        group_new = f'{group}-edit'
        resp = IlxPage(ui_ilx).edit_group(data_group[3])
        assert resp == group_new, 'group is not edited'

    def test_delete_group(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11392
        data_group = IlxPage(ui_ilx).get_data_group()
        if len(data_group) <= 2:
            self.test_create_group(ui_ilx)
        resp = IlxPage(ui_ilx).delete_group(data_group[3])
        assert resp is None, 'group is not deleted'


@pytest.mark.usefixtures('login_ilx')
class TestIntegrations:

    def test_create_integration(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11394
        integration = IlxUtils.generate_name('a-int')
        resp = IlxPage(ui_ilx).create_integration(integration)
        assert resp == integration, 'integration is not created'

    def test_edit_integration(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11395
        resp = IlxPage(ui_ilx).edit_integration()
        assert resp.split('-')[-1] == 'edit', 'integration is not edited'

    def test_add_integration_to_group(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11396
        before = IlxPage(ui_ilx).get_data_group()
        if len(before) <= 2:
            TestGroups().test_create_group(ui_ilx)
            before = IlxPage(ui_ilx).get_data_group()
        IlxPage(ui_ilx).add_to_group()
        after = IlxPage(ui_ilx).get_data_group()
        resp = IlxUtils.diff(before, after)
        assert len(resp) > 0, 'integration not added to group'

    def test_add_integration_to_connection(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11411
        connect = IlxPage(ui_ilx).get_connections()
        if not connect:
            TestConnections().test_create_connection(ui_ilx)
        resp = IlxPage(ui_ilx).add_to_connection()
        assert str(resp) == 'Integrations', 'integration not added to connection'

    @pytest.mark.parametrize('operation, testrail_case_id', [
        ('move', 11397),
        ('remove', 11398),
        ('delete', 11399)
    ])
    def test_move_remove_delete_integration_group(self, ui_ilx, operation, testrail_case_id):
        before = IlxPage(ui_ilx).get_data_group()
        if len(before) <= 3:
            count = 4 - len(before)
            while count > 0:
                TestGroups().test_create_group(ui_ilx)
                count -= 1
            before = IlxPage(ui_ilx).get_data_group ()
        if before[0].get('name').split('\n')[-1] == before[1].get('name').split('\n')[-1]:
            self.test_add_integration_to_group(ui_ilx)
            before = IlxPage(ui_ilx).get_data_group()
        if operation == 'move':
            IlxPage(ui_ilx).move_to_group()
            after = IlxPage (ui_ilx).get_data_group()
            resp = IlxUtils.diff(before, after)
            assert len(resp) > 0, 'integration not moved to group'
        elif operation == 'remove':
            IlxPage(ui_ilx).remove_from_group()
            after = IlxPage(ui_ilx).get_data_group()
            resp = IlxUtils.diff(before, after)
            assert len(resp) > 0, 'integration not removed from group'
        else:
            IlxPage(ui_ilx).delete_from_group()
            after = IlxPage(ui_ilx).get_data_group()
            resp = IlxUtils.diff(before, after)
            assert len(resp) > 0, 'integration not deleted from group'

    def test_delete_integration(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11400
        before = IlxPage(ui_ilx).get_data_group()
        if before[0].get('name').find('\n') < 0:
            self.test_create_integration(ui_ilx)
            before = IlxPage(ui_ilx).get_data_group()
        IlxPage(ui_ilx).delete_integration()
        after = IlxPage(ui_ilx).get_data_group()
        resp = IlxUtils.diff(before, after)
        assert len (resp) > 0, 'integration not deleted'


@pytest.mark.usefixtures('login_ilx')
class TestConnections:

    def test_create_connection(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11412
        connect = IlxUtils.generate_name('a-connect')
        resp = IlxPage(ui_ilx).create_connection(connect)
        assert resp.text == connect, 'connection is not created'

    def test_edit_connection(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11413
        connect = IlxPage(ui_ilx).get_connections()
        if not connect:
            self.test_create_connection(ui_ilx)
        resp = IlxPage(ui_ilx).edit_connection()
        assert resp.split('-')[-1] == 'edit', 'connection is not edited'

    def test_delete_connection(self, ui_ilx):
        ui_ilx.ilx_testrail_case_id = 11414
        before = IlxPage(ui_ilx).get_connections()
        if not before:
            self.test_create_connection(ui_ilx)
            before = IlxPage(ui_ilx).get_connections()
        IlxPage(ui_ilx).delete_connection()
        after = IlxPage(ui_ilx).get_connections()
        assert before - after == 1, 'connection is not deleted'