import pytest
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.distributor.settings_page import SettingsPage

class TestSettings():
    @pytest.mark.regression
    def test_document_import(self, ui):
        ui.testrail_case_id = 36

        lp = LoginPage(ui)
        sp = SettingsPage(ui)

        lp.log_in_distributor_portal()
        sp.sidebar_account_status()
        sp.click_tab_by_name("Enterprise pricing")
        sp.import_document()
        sp.delete_last_document()