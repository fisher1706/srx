class Variables():
    def __init__(self, environment, portal_credentials, smoke=None):
        self.smoke = smoke
        self.portal_credentials = portal_credentials
        if (environment == 'dev'):
            self.dev_environment()
        elif (environment == 'staging'):
            self.staging_environment()
        elif (environment == 'qa' or environment is None):
            self.qa_environment()
        elif (environment == 'prod' and smoke == True):
            self.smoke_prod_environment()
        self.general()

    def dev_environment(self):
        self.api_environment = "dev"
        self.admin_email = self.portal_credentials["admin_email"]
        self.admin_password = self.portal_credentials["admin_password"]
        self.distributor_email = self.portal_credentials["distributor_email"]
        self.distributor_password = self.portal_credentials["distributor_password"]
        self.customer_email = self.portal_credentials["customer_email"]
        self.customer_password = self.portal_credentials["customer_password"]
        self.distributor_name = "QA-distributor"
        self.distributor_id = "73"
        self.sub_distributor_name = "Dev Distributor"
        self.run_number = None
        self.customer_name = "Static Customer"
        self.customer_id = "92"
        self.shipto_number = "2048"
        self.shipto_id = "59"

    def staging_environment(self):
        self.api_environment = "staging"
        self.admin_email = self.portal_credentials["admin_email"]
        self.admin_password = self.portal_credentials["admin_password"]
        self.distributor_email = self.portal_credentials["distributor_email"]
        self.distributor_password = self.portal_credentials["distributor_password"]
        self.customer_email = self.portal_credentials["customer_email"]
        self.customer_password = self.portal_credentials["customer_password"]
        self.distributor_name = "QA-distributor"
        self.distributor_id = "98"
        self.warehouse_id = "38"
        self.sub_distributor_name = "Static Test"
        self.run_number = None
        self.customer_name = "Static Customer"
        self.shipto_number = "2048"
        if (self.smoke is True):
            self.run_number = [43]
            self.customer_id = "187"
            self.shipto_id = "189"
            self.ordering_config_id = "1516"
            self.report_id = 6
        else:
            self.run_number = None
            self.customer_id = "54"
            self.shipto_id = "31"

    def qa_environment(self):
        self.api_environment = "qa"
        self.admin_email = self.portal_credentials["admin_email"]
        self.admin_password = self.portal_credentials["admin_password"]
        self.distributor_email = self.portal_credentials["distributor_email"]
        self.distributor_password = self.portal_credentials["distributor_password"]
        self.customer_email = self.portal_credentials["customer_email"]
        self.customer_password = self.portal_credentials["customer_password"]
        self.distributor_name = "MAIN-QA-DISTRIBUTOR"
        self.distributor_id = "4"
        self.warehouse_id = "4"
        self.sub_distributor_name = "SECOND-QA-DISTRIBUTOR"
        self.sub_distributor_id = "5"
        self.customer_name = "Static Customer"
        self.shipto_number = "FIRST-QA-SHIPTO"
        if (self.smoke is True):
            self.run_number = [40]
            self.customer_id = "191"
            self.shipto_id = "2192"
            self.locker_id = "3869"
            self.ordering_config_id = "2577"
            self.report_id = 5
        else:
            self.run_number = [31, 2]
            self.customer_id = "4"
            self.shipto_id = "4"
        
    def smoke_prod_environment(self):
        pass

    def general(self):
        self.expected_error_series = 1
        self.default_wait = 18