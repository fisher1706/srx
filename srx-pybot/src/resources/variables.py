class Variables():
    def __init__(self, environment):
        if (environment == 'dev'):
            self.dev_environment()
        elif (environment == 'staging'):
            self.staging_environment()
        elif (environment == 'qa' or environment is None):
            self.qa_environment()
        self.general()

    def dev_environment(self):
        self.admin_email = "srx-group+dev@agilevision.io"
        self.admin_password = "srx-group"
        self.distributor_email = "dprovorov+testadmin@agilevision.io"
        self.distributor_password = "test29"
        self.distributor_name = "QA-distributor"
        self.customer_email = "dprovorov+customer3@agilevision.io"
        self.customer_password = "test29"
        self.sub_distributor_name = "Dev Distributor"
        self.run_number = [1, 2]
        self.customer_name = "Static Customer"
        self.shipto_number = "2048"

    def staging_environment(self):
        self.admin_email = "srx-group+staging@agilevision.io"
        self.admin_password = "srx-group"
        self.distributor_email = "dprovorov+distributor@agilevision.io"
        self.distributor_password = "test29"
        self.distributor_name = "QA-distributor"
        self.customer_email = "dprovorov+customer3@agilevision.io"
        self.customer_password = "test29"
        self.sub_distributor_name = "Static Test"
        self.run_number = [8]
        self.customer_name = "Static Customer"
        self.customer_id = "54"
        self.shipto_number = "2048"
        self.shipto_id = "31"
        self.inbox_email = "auto-test-stg@storeroomlogix.com"

    def qa_environment(self):
        self.admin_email = "dprovorov@agilevision.io"
        self.admin_password = "test29"
        self.distributor_email = "dprovorov+dist@agilevision.io"
        self.distributor_password = "test29"
        self.distributor_name = "MAIN-QA-DISTRIBUTOR"
        self.customer_email = "dprovorov+cust@agilevision.io"
        self.customer_password = "test29"
        self.sub_distributor_name = "SECOND-QA-DISTRIBUTOR"
        self.run_number = [31, 2]
        self.customer_name = "Static Customer"
        self.customer_id = "4"
        self.shipto_number = "FIRST-QA-SHIPTO"
        self.shipto_id = "4"
        self.inbox_email = "auto-test-qa@storeroomlogix.com"

    def general(self):
        self.expected_error_series = 2
        self.default_wait = 18