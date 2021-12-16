class URL():
    def __init__(self, environment):
        self.environment = environment
        if self.environment is None:
            self.environment = 'qa'
        if self.environment in ('dev', 'staging', 'prod', 'qa'):
            self.admin_portal = self.get_url_for_env("storeroomlogix.com", "admin")
            self.auth_portal = self.get_url_for_env("storeroomlogix.com", "auth")
            self.distributor_portal = self.get_url_for_env("storeroomlogix.com", "distributor")
            self.customer_portal = self.get_url_for_env("storeroomlogix.com", "customer")
            self.checkout_portal = self.get_url_for_env("storeroomlogix.com", "checkout")
            self.new_checkout_portal = self.get_url_for_env("storeroomlogix.com", "next.checkout")
            self.ilx_mocks = "http://54.175.164.185:8080"
        else:
            raise IOError("Incorrect environment")

    def get_url_for_env(self, url, portal):
        if self.environment != "tenant":
            switcher = {
                'dev': f"https://{portal}.dev.{url}",
                'staging': f"https://{portal}.staging.{url}",
                'prod': f"https://{portal}.{url}",
                'qa': f"https://{portal}.qa.{url}",
            }
            return switcher.get(self.environment)
        if portal in ("admin", "checkout"):
            return f"https://{portal}.tenant.{url}"
        if portal == "next.checkout":
            return f"https://app-tenant.{url}/checkout"
        return f"https://app-tenant.{url}/{portal}"

    def get_api_url_for_env(self, url):
        return f"https://api-{self.environment}.storeroomlogix.com{url}"

    def get_ip_url(self, url):
        return f"{self.ilx_mocks}{url}"

    def get_iothub_api_url_for_env(self, url):
        return f"https://iothub-api.storeroomlogix.com/{self.environment}{url}"
