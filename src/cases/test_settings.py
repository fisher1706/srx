import pytest
from src.pages.general.login_page import LoginPage
from src.pages.distributor.settings_page import SettingsPage
from src.api.distributor.settings_api import SettingsApi

@pytest.mark.regression
def test_document_import(ui):
    ui.testrail_case_id = 36

    lp = LoginPage(ui)
    sp = SettingsPage(ui)

    lp.log_in_distributor_portal()
    sp.follow_url(ui.session_context.url.get_url_for_env("storeroomlogix.com/profile#pricing", "distributor"))
    sp.import_document()
    sp.delete_last_document()

@pytest.mark.smoke
def test_smoke_get_settings(smoke_api):
    smoke_api.testrail_case_id = 2001

    sa = SettingsApi(smoke_api)

    sa.get_reorder_controls_settings_for_shipto(smoke_api.data.shipto_id)