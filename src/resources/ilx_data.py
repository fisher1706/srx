class IlxData():
    'The class contains the predefined data using in regression tests'

    def __init__(self, environment):
        if environment == 'dev':
            self.dev_environment()
        elif environment == 'qa':
            self.qa_environment()
        elif environment == 'prod':
            self.prod_environment()

    def dev_environment(self):
        self.ilx_url = 'https://api.dev.integrationlogix.com/external-api/' \
               '50ff3a5c-677b-433f-a22d-826659633c61/ilx-test/salesOrdersStatus2'

    def prod_environment(self):
        pass

    def qa_environment(self):
        pass
