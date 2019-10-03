class Variables():
    def __init__(self, environment):
        if (environment == 'dev' or environment is None):
            self.dev_environment()
        elif (environment == 'staging'):
            self.staging_environment()
        self.general()

    def dev_environment(self):
        self.admin_email = "srx-group+dev@agilevision.io"
        self.admin_password = "srx-group"
        self.distributor_email = "dprovorov+testadmin@agilevision.io"
        self.distributor_password = "test29"
        self.distributor_name = "QA-distributor"
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
        self.sub_distributor_name = "Static Test"
        self.run_number = [8]

    def general(self):
        self.expected_error_series = 2
        self.default_wait = 18