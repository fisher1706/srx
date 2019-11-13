class URL():
    def __init__(self, environment):
        self.environment = environment
        if (self.environment is None):
            self.environment = 'qa'
        if (self.environment == 'dev' or self.environment == 'staging' or self.environment == 'prod' or self.environment == 'qa'):
            self.admin_portal = self.get_url_for_env("storeroomlogix.com", "admin")
            self.auth_portal = self.get_url_for_env("storeroomlogix.com", "auth")
            self.distributor_portal = self.get_url_for_env("storeroomlogix.com", "distributor")
            self.customer_portal = self.get_url_for_env("storeroomlogix.com", "customer")
        else:
            raise IOError("Incorrect environment")

    def get_url_for_env(self, url, portal):
        switcher = {
            'dev': "https://"+portal+".dev."+url,
            'staging': "https://"+portal+".staging."+url,
            'prod': "https://"+portal+"."+url,
            'qa': "https://"+portal+".qa."+url
        }
        return switcher.get(self.environment)

    def get_api_url_for_env(self, url):
        switcher = {
            'dev': "https://api-dev.storeroomlogix.com"+url,
            'staging': "https://api-staging.storeroomlogix.com"+url,
            'prod': "https://api-prod.storeroomlogix.com"+url,
            'qa': "https://api-qa.storeroomlogix.com"+url
        }
        return switcher.get(self.environment)