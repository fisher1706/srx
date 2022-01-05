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
        if self.environment == "prod":
            if portal == "admin":
                return f"https://{portal}.{url}"
            return f"https://app.{url}/{portal}"
        if portal == "admin":
            return f"https://{portal}.{self.environment}.{url}"
        return f"https://app-{self.environment}.{url}/{portal}"

    def get_api_url_for_env(self, url):
        if self.environment == "prod":
            return f"https://api.storeroomlogix.com{url}"
        return f"https://api.{self.environment}.storeroomlogix.com{url}"

    def get_ip_url(self, url):
        return f"{self.ilx_mocks}{url}"

    def get_iothub_api_url_for_env(self, url):
        return f"https://iothub-api.storeroomlogix.com/{self.environment}{url}"
