class URL():
    def __init__(self, environment):
        self.environment = environment
        if (self.environment is None):
            self.environment = 'dev'
        if (self.environment == 'dev' or self.environment == 'staging' or self.environment == 'prod'):
            self.admin_portal = self.get_admin_portal()
            self.auth_portal = self.get_auth_portal()
            self.distributor_portal = self.get_distributor_portal()
        else:
            raise IOError("Incorrect environment")

    def get_admin_portal(self):
        switcher = {
            'dev': "https://admin.dev.storeroomlogix.com/",
            'staging': "https://admin.staging.storeroomlogix.com/",
            'prod': "https://admin.storeroomlogix.com/"
        }
        return switcher.get(self.environment)

    def get_auth_portal(self):
        switcher = {
            'dev': "https://auth.dev.storeroomlogix.com/",
            'staging': "https://auth.staging.storeroomlogix.com/",
            'prod': "https://auth.storeroomlogix.com/"
        }
        return switcher.get(self.environment)

    def get_distributor_portal(self):
        switcher = {
            'dev': "https://distributor.dev.storeroomlogix.com/",
            'staging': "https://distributor.staging.storeroomlogix.com/",
            'prod': "https://distributor.storeroomlogix.com/"
        }
        return switcher.get(self.environment)