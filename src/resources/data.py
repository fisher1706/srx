class Data():
    def __init__(self, environment):
        if (environment == 'dev'):
            self.dev_environment()
        elif (environment == 'staging'):
            self.staging_environment()
        elif (environment == 'qa'):
            self.qa_environment()

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
        self.warehouse_id = "38"
        self.sub_distributor_name = "Static Test"
        self.sub_distributor_id = 8
        self.testrail_run_id = 48
        self.mobile_testrail_run_id = 53
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

    def qa_environment(self):
        self.distributor_name = "MAIN-QA-DISTRIBUTOR"
        self.distributor_id = "4"
        self.warehouse_id = "4"
        self.sub_distributor_name = "SECOND-QA-DISTRIBUTOR"
        self.sub_distributor_id = "5"
        self.customer_name = "Static Customer"
        self.shipto_number = "FIRST-QA-SHIPTO"
        self.testrail_run_id = 44
        self.mobile_testrail_run_id = 54
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

class SmokeData():
    def __init__(self, environment):
        if (environment == 'dev'):
            self.dev_environment()
        elif (environment == 'staging'):
            self.staging_environment()
        elif (environment == 'qa'):
            self.qa_environment()
        elif (environment == 'prod'):
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

    def qa_environment(self):
        self.smoke_testrail_run_id = 40
        self.customer_id = "191"
        self.shipto_id = "2192"
        self.ordering_config_id = "2577"
        self.report_id = 5

    def prod_environment(self):
        self.smoke_testrail_run_id = 45
        self.customer_id = "120"
        self.shipto_id = "159"
        self.ordering_config_id = "24425"
        self.report_id = 7
