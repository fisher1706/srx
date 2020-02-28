from src.api.api import API

class ProductApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_product(self, dto):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/products/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 201):
            self.logger.info(f"New product '{dto['partSku']}' has been successfully created")
        else:
            self.logger.error(str(response.content))