import pytest
from src.resources.tools import Tools
from src.resources.permissions import Permissions
from src.pages.general.login_page import LoginPage
from src.pages.distributor.cribcrawl_page import CribcrawlPage
from src.api.setups.setup_shipto import SetupShipto

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 2301
    },
    {
        "user": Permissions.cribcrawls("EDIT"),
        "testrail_case_id": 2302
    }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_cribcrawl_import(ui, permission_ui, permissions, delete_distributor_security_group, delete_shipto):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    cp = CribcrawlPage(context)

    response_shipto = SetupShipto(ui).setup()
    cribcrawl_body = {}

    #-------------------
    cribcrawl_body["sku"] = Tools.random_string_u()
    #-------------------
    cribcrawls = [
        [cribcrawl_body["sku"], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    ]
    #-------------------

    lp.log_in_distributor_portal()
    cp.follow_cribcrawl_url(shipto_id=response_shipto["shipto_id"])
    cp.wait_until_page_loaded()
    cp.import_cribcrawl(cribcrawls)
    cp.check_last_cribcrawl(cribcrawl_body.copy())
