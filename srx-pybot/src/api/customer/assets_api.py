from src.api.api import API

class AssetsApi(API):
    def __init__(self, case):
        super().__init__(case)

    def get_all_assets(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/assets")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Assests have been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]
    
    def check_asset_in_all_assets_list(self, asset, should_be=True):
        response_assets = self.get_all_assets()
        assets_list = []
        for item in response_assets:
            assets_list.append(item["orderingConfig"]["product"]["partSku"])
        if (should_be == True):
            if asset in assets_list:
                self.logger.info(f"Assest {asset} is present in all assets list")
                position = assets_list.index(asset)
                return response_assets[position]
            else: 
                self.logger.error(f"Assest {asset} is NOT present in all assets list")
        elif (should_be == False):
            if asset not in assets_list:
                self.logger.info(f"Assest {asset} is NOT present in all assets list")
            else: 
                self.logger.error(f"Assest {asset} IS present in all assets list, but should not")

    def get_cheked_out_assets_list(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/assets-checked-out")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Checked Out assests have been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def check_asset_in_checked_out_list(self, asset, should_be=True):
        response_assets = self.get_cheked_out_assets_list()
        assets_list = []
        for item in response_assets:
            assets_list.append(item["partSku"])
        if (should_be == True):
            if asset in assets_list:
                self.logger.info(f"Assest {asset} is present in checked out assets list")
                position = assets_list.index(asset)
                return response_assets[position]
            else: 
                self.logger.error(f"Assest {asset} is NOT present in checked out assets list")
        elif (should_be == False):
            if asset not in assets_list:
                self.logger.info(f"Assest {asset} is NOT present in checked out assets list")
            else: 
                self.logger.error(f"Assest {asset} IS present in checked out assets list, but should not")

    def get_list_of_assets_by_user(self, user_id):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/assets-user-checked-out/{user_id}")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("List of user`s assets was successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]
