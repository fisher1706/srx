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
            self.checkout_portal = self.get_url_for_env("storeroomlogix.com", "checkout")
            self.new_checkout_portal = self.get_url_for_env("storeroomlogix.com", "next.checkout")
        else:
            raise IOError("Incorrect environment")

    def get_url_for_env(self, url, portal):
        switcher = {
            'dev': f"https://{portal}.dev.{url}",
            'staging': f"https://{portal}.staging.{url}",
            'prod': f"https://{portal}.{url}",
            'qa': f"https://{portal}.qa.{url}"
        }
        return switcher.get(self.environment)

    def get_api_url_for_env(self, url):
        switcher = {
            'dev': f"https://api-dev.storeroomlogix.com{url}",
            'staging': f"https://api-staging.storeroomlogix.com{url}",
            'prod': f"https://api-prod.storeroomlogix.com{url}",
            'qa': f"https://api-qa.storeroomlogix.com{url}"
        }
        return switcher.get(self.environment)
    
    def get_iothub_api_url_for_env(self, url):
        switcher = {
            'dev': f"https://iothub-api.storeroomlogix.com/dev{url}",
            'staging': f"https://iothub-api.storeroomlogix.com/staging{url}",
            'prod': f"https://iothub-api.storeroomlogix.com/prod{url}",
            'qa': f"https://iothub-api.storeroomlogix.com/qa{url}"
        }
        return switcher.get(self.environment)