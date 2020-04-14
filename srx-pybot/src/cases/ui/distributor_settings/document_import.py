from src.pages.sub.login_page import LoginPage
from src.pages.distributor.settings_page import SettingsPage
from src.resources.case import Case
from src.resources.activity import Activity

def document_import(case):
    case.log_name("Document import")
    case.testrail_config(36)

    try:
        lp = LoginPage(case.activity)
        sp = SettingsPage(case.activity)

        lp.log_in_distributor_portal()
        sp.sidebar_account_status()
        sp.click_tab_by_name("Enterprise pricing")
        sp.import_document()
        sp.delete_last_document()

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    document_import(Case(Activity()))