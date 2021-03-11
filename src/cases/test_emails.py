import pytest
import time
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.aws.s3 import S3
from src.api.setups.setup_distributor_user import SetupDistributorUser
from src.pages.general.login_page import LoginPage
from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class TestEmails():
    @pytest.mark.regression
    def test_accept_distributor_user_invitation(self, ui, delete_distributor_user):
        ui.testrail_case_id = 4095

        s3 = S3(ui)
        lp = LoginPage(ui)
        dpp = DistributorPortalPage(ui)

        s3.clear_bucket(ui.data.email_data_bucket)
        objects = s3.get_objects_in_bucket(ui.data.email_data_bucket)
        objects_count = len(objects)
        print(f"\nCOUNT: {objects_count}\n")

        setup_user = SetupDistributorUser(ui)
        user_email = ui.data.ses_email.format(suffix=Tools.random_string_l())
        setup_user.add_option("email", user_email)
        setup_user.setup()

        s3.wait_for_new_object(ui.data.email_data_bucket, objects_count)

        last_email_key = s3.get_last_modified_object_in_bucket(ui.data.email_data_bucket).key
        email_filename = "distributor_user_invitation"
        s3.download_by_key(ui.data.email_data_bucket, last_email_key, email_filename)
        temporary_password = Tools.get_password_from_email(email_filename)
        new_password = Tools.random_string_l()

        print(f"\nPASSWORD: {temporary_password}")

        lp.follow_auth_portal()
        lp.input_email(user_email)
        lp.input_password(temporary_password)
        lp.click_on_submit_button()
        lp.input_data_id(new_password, Locator.id_new_password)
        lp.input_data_id(new_password, Locator.id_confirm_password)
        lp.click_on_submit_button()
        lp.title_should_be("SRX Distributor Portal")
        lp.follow_url(lp.url.distributor_portal)
        dpp.distributor_sidebar_should_contain_email(user_email)
        dpp.sign_out()
        lp.log_in_distributor_portal()

