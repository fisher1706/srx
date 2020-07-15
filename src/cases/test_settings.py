import pytest
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.distributor.settings_page import SettingsPage
from src.api.distributor.settings_api import SettingsApi

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

    @pytest.mark.smoke
    def test_smoke_get_settings(self, smoke_api):
        smoke_api.testrail_case_id = 2001

        sa = SettingsApi(smoke_api)

        sa.get_checkout_software_settings_for_shipto(smoke_api.data.shipto_id)