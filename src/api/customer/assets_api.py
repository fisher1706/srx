from src.api.api import API

class AssetsApi(API):
    def get_all_assets(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/assets")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Assests have been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json
    
    def check_asset_in_all_assets_list(self, asset):
        response = self.get_all_assets()
        response_assets = response["data"]["entities"]
        assets_list = []
        for item in response_assets:
            assets_list.append(item["orderingConfig"]["product"]["partSku"])
        if asset in assets_list:
            self.logger.info(f"Assest {asset} is pesetnt in all assets list")
        else: 
            self.logger.error(f"Assest {asset} is NOT pesetnt in all assets list")