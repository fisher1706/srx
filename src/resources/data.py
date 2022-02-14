class Data():
    'The class contains the predefined data using in regression tests'

    def __init__(self, environment):
        if environment == 'dev':
            self.dev_environment()
        elif environment == 'staging':
            self.staging_environment()
        elif environment == 'qa':
            self.qa_environment()
        elif environment == 'tenant':
            self.tenant_environment()

    def dev_environment(self):
        self.distributor_name = "QA-distributor"
        self.distributor_id = "73"
        self.sub_distributor_name = "Dev Distributor"
        self.testrail_run_id = 47
        self.mobile_testrail_run_id = 55
        self.customer_name = "Static Customer"
        self.customer_id = "92"
        self.shipto_number = "2048"
        self.shipto_id = "59"
        self.warehouse_id = 47
        self.sub_distributor_id = 422
        self.checkout_group_id = "30"
        self.checkout_user_id = "199"
        self.customer_user_id = "2801"
        self.passcode = "AUTOTEST"
        self.customer_user_passcode = "PSCD"

    def staging_environment(self):
        self.distributor_name = "QA-distributor"
        self.distributor_id = "98"
        self.ilx_distributor_id = "832"
        self.warehouse_id = "38"
        self.sub_distributor_name = "Static Test"
        self.sub_distributor_id = 8
        self.testrail_run_id = 48
        self.mobile_testrail_run_id = 53
        self.ilx_testrail_run_id = 278
        self.customer_name = "Static Customer"
        self.shipto_number = "2048"
        self.customer_id = "54"
        self.shipto_id = "31"
        self.checkout_group_id = "24"
        self.checkout_user_id = "138"
        self.customer_user_id = "26"
        self.passcode = "AUTOTEST"
        self.customer_user_passcode = "PSCD"
        self.customer_user_first_name = "123"
        self.customer_user_last_name = "32123"
        self.default_security_group_id = 1266
        self.email_data_bucket = "srx-email-testing-vjrm1-staging"
        self.ses_email = "automation_testing_email+{suffix}@mail.staging.storeroomlogix.com"

    def qa_environment(self):
        self.distributor_name = "MAIN-QA-DISTRIBUTOR"
        self.distributor_id = "4"
        self.ilx_distributor_id = "937"
        self.warehouse_id = "4"
        self.sub_distributor_name = "SECOND-QA-DISTRIBUTOR"
        self.sub_distributor_id = "5"
        self.customer_name = "Static Customer"
        self.shipto_number = "FIRST-QA-SHIPTO"
        self.testrail_run_id = 44
        self.mobile_testrail_run_id = 54
        self.ilx_testrail_run_id = 279
        self.customer_id = "4"
        self.shipto_id = "4"
        self.checkout_group_id = "816"
        self.checkout_user_id = "630"
        self.customer_user_id = "11"
        self.passcode = "AUTOTEST"
        self.customer_user_passcode = "PSCD"
        self.customer_user_first_name = "dprovorov+cust@agilevision.io"
        self.customer_user_last_name = "dprovorov+cust@agilevision.io"
        self.default_security_group_id = 2160
        self.email_data_bucket = "srx-email-testing-0641q-qa"
        self.ses_email = "automation_testing_email+{suffix}@mail.qa.storeroomlogix.com"

    def tenant_environment(self):
        self.distributor_name = "MAIN-QA-DISTRIBUTOR"
        self.distributor_id = "14"
        self.warehouse_id = "4"
        self.sub_distributor_name = "SECOND-QA-DISTRIBUTOR"
        self.sub_distributor_id = "15"
        self.customer_name = "MAIN CUSTOMER"
        self.shipto_number = "MAIN SHIPTO"
        self.testrail_run_id = 280
        self.mobile_testrail_run_id = 281
        self.customer_id = "4"
        self.shipto_id = "3"
        self.checkout_group_id = "1"
        self.checkout_user_id = "3"
        self.customer_user_id = "2"
        self.passcode = "AUTOTEST"
        self.customer_user_passcode = "PSCD"
        self.customer_user_first_name = "dprovorov"
        self.customer_user_last_name = "dprovorov"
        self.default_security_group_id = 80

class SmokeData():
    'The class contains the predefined data using in smoke tests'

    def __init__(self, environment):
        if environment == 'dev':
            self.dev_environment()
        elif environment == 'staging':
            self.staging_environment()
        elif environment == 'qa':
            self.qa_environment()
        elif environment == 'prod':
            self.prod_environment()

    def dev_environment(self):
        self.smoke_testrail_run_id = 56
        self.customer_id = "1288"
        self.shipto_id = "1653"
        self.ordering_config_id = "17334"
        self.report_id = 8

    def staging_environment(self):
        self.smoke_testrail_run_id = 43
        self.customer_id = "187"
        self.shipto_id = "189"
        self.ordering_config_id = "1516"
        self.report_id = 6
        self.group_id = 431

    def qa_environment(self):
        self.smoke_testrail_run_id = 40
        self.customer_id = "1115"
        self.shipto_id = "35529"
        self.ordering_config_id = "53740"
        self.report_id = 5
        self.group_id = 623

    def prod_environment(self):
        self.smoke_testrail_run_id = 45
        self.customer_id = "120"
        self.shipto_id = "159"
        self.ordering_config_id = "24425"
        self.report_id = 7
        self.group_id = 145
