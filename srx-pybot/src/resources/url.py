class URL():
    def __init__(self, environment):
        self.environment = environment
        if (self.environment is None):
            self.environment = 'dev'
        if (self.environment == 'dev' or self.environment == 'staging' or self.environment == 'prod'):
            self.admin_portal = self.get_url_for_env("storeroomlogix.com", "admin")
            self.auth_portal = self.get_url_for_env("storeroomlogix.com", "auth")
            self.distributor_portal = self.get_url_for_env("storeroomlogix.com", "distributor")
            self.customer_portal = self.get_url_for_env("storeroomlogix.com", "customer")
        else:
            raise IOError("Incorrect environment")
        _ENV = self.environment

    @staticmethod
    def get_api_url_for_env(self, url, portal):
        switcher = {
            'dev': "https://"+portal+"-dev."+url,
            'staging': "https://"+portal+"-staging."+url,
            'prod': "https://"+portal+"."+url
        }
        return switcher.get(_ENV)

    def get_url_for_env(self, url, portal):
        switcher = {
            'dev': "https://"+portal+".dev."+url,
            'staging': "https://"+portal+".staging."+url,
            'prod': "https://"+portal+"."+url
        }
        return switcher.get(self.environment)