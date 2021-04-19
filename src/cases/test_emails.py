import pytest
import time
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.aws.s3 import S3
from src.api.setups.setup_distributor_user import SetupDistributorUser
from src.api.setups.setup_customer import SetupCustomer
from src.api.setups.setup_customer_user_as_customer import SetupCustomerUserAsCustomer
from src.api.setups.setup_checkout_group import SetupCheckoutGroup
from src.pages.general.login_page import LoginPage
from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.pages.customer.customer_portal_page import CustomerPortalPage
from src.pages.checkout.checkout_portal_page import CheckoutPortalPage

class TestEmails():
    @pytest.mark.parametrize("conditions", [
        {
            "user": "SUPER",
            "testrail_case_id": 4095
        },
        {
            "user": None,
            "testrail_case_id": 4400
        }
        ])
    @pytest.mark.regression
    def test_accept_distributor_user_invitation_and_reset_password(self, ui, conditions, delete_distributor_user):
        ui.testrail_case_id = conditions["testrail_case_id"]

        s3 = S3(ui)
        lp = LoginPage(ui)
        dpp = DistributorPortalPage(ui)

        s3.clear_bucket(ui.data.email_data_bucket)
        objects = s3.get_objects_in_bucket(ui.data.email_data_bucket)
        objects_count = len(objects)

        #create new user
        setup_user = SetupDistributorUser(ui)
        user_email = ui.data.ses_email.format(suffix=Tools.random_string_l())
        setup_user.add_option("email", user_email)
        setup_user.add_option("group", conditions["user"])
        setup_user.setup()

        #waiting for new email with the temporary password
        s3.wait_for_new_object(ui.data.email_data_bucket, objects_count)

        #parse email and get temporary password
        last_email_key = s3.get_last_modified_object_in_bucket(ui.data.email_data_bucket).key
        email_filename = "distributor_user_invitation"
        s3.download_by_key(ui.data.email_data_bucket, last_email_key, email_filename)
        temporary_password = Tools.get_password_from_email(email_filename)
        new_password = Tools.random_string_l()

        #create users's password
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
        lp.log_in_distributor_portal(user_email, new_password)

        #sigh out and reset password
        dpp.sign_out()
        lp.open_forgot_password_page()
        lp.input_email(user_email)
        lp.click_on_submit_button()
        lp.get_element_by_xpath("//h2[text()='Please check your inbox']")

        #waiting for email with reset password confirmation
        s3.wait_for_new_object(ui.data.email_data_bucket, objects_count+1)

        #confirm reset password from email
        last_email_key = s3.get_last_modified_object_in_bucket(ui.data.email_data_bucket).key
        email_filename = "distributor_user_reset"
        s3.download_by_key(ui.data.email_data_bucket, last_email_key, email_filename)
        acception_link = Tools.get_reset_password_link_from_email(email_filename)[0]
        lp.follow_url(acception_link)

        #set a new password
        new_reset_password = Tools.random_string_l()
        
        lp.input_data_id(new_reset_password, Locator.id_new_password)
        lp.input_data_id(new_reset_password, Locator.id_confirm_password)
        lp.click_on_submit_button()
        lp.log_in_distributor_portal(user_email, new_reset_password)


    @pytest.mark.regression
    def test_accept_new_customer_user_invitation(self, ui, delete_customer):
        ui.testrail_case_id = 4549

        s3 = S3(ui)
        lp = LoginPage(ui)
        cpp = CustomerPortalPage(ui)

        s3.clear_bucket(ui.data.email_data_bucket)
        objects = s3.get_objects_in_bucket(ui.data.email_data_bucket)
        objects_count = len(objects)

        setup_customer = SetupCustomer(ui)
        user_email = ui.data.ses_email.format(suffix=Tools.random_string_l(20))
        setup_customer.add_option("user", user_email)
        setup_customer.setup()

        s3.wait_for_new_object(ui.data.email_data_bucket, objects_count)

        last_email_key = s3.get_last_modified_object_in_bucket(ui.data.email_data_bucket).key
        email_filename = "customer_user_invitation_accept"
        s3.download_by_key(ui.data.email_data_bucket, last_email_key, email_filename)
        acception_link = Tools.get_acception_link_from_email(email_filename)[0]
        lp.follow_url(acception_link)
        lp.get_element_by_xpath("//h3[text()='Your invite was successfully accepted']")

        s3.wait_for_new_object(ui.data.email_data_bucket, objects_count+1)

        last_email_key = s3.get_last_modified_object_in_bucket(ui.data.email_data_bucket).key
        email_filename = "customer_user_invitation_password"
        s3.download_by_key(ui.data.email_data_bucket, last_email_key, email_filename)
        temporary_password = Tools.get_password_from_email(email_filename)
        new_password = Tools.random_string_l()

        lp.follow_auth_portal()
        lp.input_email(user_email)
        lp.input_password(temporary_password)
        lp.click_on_submit_button()
        lp.input_data_id(new_password, Locator.id_new_password)
        lp.input_data_id(new_password, Locator.id_confirm_password)
        lp.click_on_submit_button()
        lp.title_should_be("SRX User Dashboard")
        lp.follow_url(lp.url.customer_portal)
        cpp.customer_sidebar_should_contain_email(user_email)
        cpp.sign_out()
        lp.log_in_customer_portal(user_email, new_password)

    @pytest.mark.regression
    def test_accept_customer_user_invitation_and_reset_password(self, ui, delete_customer_user):
        ui.testrail_case_id = 4581

        s3 = S3(ui)
        lp = LoginPage(ui)
        cpp = CustomerPortalPage(ui)

        s3.clear_bucket(ui.data.email_data_bucket)
        objects = s3.get_objects_in_bucket(ui.data.email_data_bucket)
        objects_count = len(objects)

        setup_user = SetupCustomerUserAsCustomer(ui)
        user_email = ui.data.ses_email.format(suffix=Tools.random_string_l(15))
        setup_user.add_option("email", user_email)
        setup_user.setup()

        s3.wait_for_new_object(ui.data.email_data_bucket, objects_count)

        last_email_key = s3.get_last_modified_object_in_bucket(ui.data.email_data_bucket).key
        email_filename = "customer_user_invitation"
        s3.download_by_key(ui.data.email_data_bucket, last_email_key, email_filename)
        temporary_password = Tools.get_password_from_email(email_filename)
        new_password = Tools.random_string_l()

        lp.follow_auth_portal()
        lp.input_email(user_email)
        lp.input_password(temporary_password)
        lp.click_on_submit_button()
        lp.input_data_id(new_password, Locator.id_new_password)
        lp.input_data_id(new_password, Locator.id_confirm_password)
        lp.click_on_submit_button()
        lp.title_should_be("SRX User Dashboard")
        lp.follow_url(lp.url.customer_portal)
        cpp.customer_sidebar_should_contain_email(user_email)
        cpp.sign_out()
        lp.log_in_customer_portal(user_email, new_password)

        #sigh out and reset password
        cpp.sign_out()
        lp.open_forgot_password_page()
        lp.input_email(user_email)
        lp.click_on_submit_button()
        lp.get_element_by_xpath("//h2[text()='Please check your inbox']")

        #waiting for email with reset password confirmation
        s3.wait_for_new_object(ui.data.email_data_bucket, objects_count+1)

        #confirm reset password from email
        last_email_key = s3.get_last_modified_object_in_bucket(ui.data.email_data_bucket).key
        email_filename = "customer_user_reset"
        s3.download_by_key(ui.data.email_data_bucket, last_email_key, email_filename)
        acception_link = Tools.get_reset_password_link_from_email(email_filename)[0]
        lp.follow_url(acception_link)

        #set a new password
        new_reset_password = Tools.random_string_l()
        
        lp.input_data_id(new_reset_password, Locator.id_new_password)
        lp.input_data_id(new_reset_password, Locator.id_confirm_password)
        lp.click_on_submit_button()
        lp.log_in_customer_portal(user_email, new_reset_password)

    @pytest.mark.regression
    def test_accept_checkout_group_invitation_and_reset_password(self, ui, delete_checkout_group):
        ui.testrail_case_id = 4588

        s3 = S3(ui)
        lp = LoginPage(ui)
        cpp = CheckoutPortalPage(ui)

        s3.clear_bucket(ui.data.email_data_bucket)
        objects = s3.get_objects_in_bucket(ui.data.email_data_bucket)
        objects_count = len(objects)

        setup_user = SetupCheckoutGroup(ui)
        user_email = ui.data.ses_email.format(suffix=Tools.random_string_l(16))
        setup_user.add_option("email", user_email)
        setup_user.setup()

        s3.wait_for_new_object(ui.data.email_data_bucket, objects_count)

        last_email_key = s3.get_last_modified_object_in_bucket(ui.data.email_data_bucket).key
        email_filename = "checkout_group_invitation"
        s3.download_by_key(ui.data.email_data_bucket, last_email_key, email_filename)
        temporary_password = Tools.get_password_from_email(email_filename)
        new_password = Tools.random_string_l()

        lp.follow_checkout_portal()
        cpp.input_email_checkout_portal(user_email)
        cpp.input_password_checkout_portal(temporary_password)
        cpp.sign_in_checkout_portal()
        cpp.input_data_id(new_password, "mat-input-2")
        cpp.input_data_id(new_password, "mat-input-3")
        cpp.click_xpath(Locator.xpath_button_type)
        cpp.input_email_checkout_portal(user_email)
        cpp.input_password_checkout_portal(new_password)
        cpp.sign_in_checkout_portal()
        cpp.get_element_by_xpath(f"//div[text()='{user_email}']")
        assert "Passcode" in ui.driver.page_source

        #sigh out and reset password
        lp.click_xpath("//img")
        lp.click_xpath(Locator.xpath_sign_out)
        lp.click_xpath(Locator.xpath_reset_password)
        lp.input_by_name("login", user_email)
        lp.click_xpath(Locator.xpath_button_type)

        #waiting for email with reset password confirmation
        s3.wait_for_new_object(ui.data.email_data_bucket, objects_count+1)

        #confirm reset password from email
        last_email_key = s3.get_last_modified_object_in_bucket(ui.data.email_data_bucket).key
        email_filename = "checkout_group_reset"
        s3.download_by_key(ui.data.email_data_bucket, last_email_key, email_filename)
        acception_link = Tools.get_reset_password_link_from_email(email_filename)[0]
        lp.follow_url(acception_link)

        #set a new password
        new_reset_password = Tools.random_string_l()
        
        cpp.input_data_id(new_password, "mat-input-0")
        cpp.input_data_id(new_password, "mat-input-1")
        cpp.click_xpath(Locator.xpath_button_type)
        cpp.input_email_checkout_portal(user_email)
        cpp.input_password_checkout_portal(new_password)
        cpp.sign_in_checkout_portal()
        cpp.get_element_by_xpath(f"//div[text()='{user_email}']")
        assert "Passcode" in ui.driver.page_source
