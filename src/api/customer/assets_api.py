from src.api.api import API
from src.resources.messages import Message
from glbl import LOG, ERROR

class AssetsApi(API):
    def get_all_assets(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/assets")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            LOG.info(Message.entity_operation_done.format(entity="Asset", operation="got"))
        else:
            ERROR(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def check_asset_in_all_assets_list(self, asset, should_be=True):
        response_assets = self.get_all_assets()
        assets_list = []
        for item in response_assets:
            assets_list.append(item["orderingConfig"]["product"]["partSku"])
        if should_be:
            if asset in assets_list:
                LOG.info(f"Assest {asset} is present in all assets list")
                position = assets_list.index(asset)
                return response_assets[position]
            ERROR(f"Assest {asset} is NOT present in all assets list")
        else:
            if asset not in assets_list:
                LOG.info(f"Assest {asset} is NOT present in all assets list")
            else:
                ERROR(f"Assest {asset} IS present in all assets list, but should not")

    def get_list_of_assets_by_user(self, user_id):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/assets-user-checked-out/{user_id}")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            LOG.info(Message.entity_operation_done.format(entity="List of User", operation="got"))
        else:
            ERROR(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def get_cheked_out_assets_list(self):
        url = self.url.get_api_url_for_env("/customer-portal/customer/assets-checked-out")
        token = self.get_customer_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            LOG.info(Message.entity_operation_done.format(entity="Checked Out asset", operation="got"))
        else:
            ERROR(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def check_asset_in_checked_out_list(self, asset, should_be=True):
        response_assets = self.get_cheked_out_assets_list()
        assets_list = []
        for item in response_assets:
            assets_list.append(item["partSku"])
        if should_be:
            if asset in assets_list:
                LOG.info(f"Assest {asset} is present in checked out assets list")
                position = assets_list.index(asset)
                return response_assets[position]
            ERROR(f"Assest {asset} is NOT present in checked out assets list")
        else:
            if asset not in assets_list:
                LOG.info(f"Assest {asset} is NOT present in checked out assets list")
            else:
                ERROR(f"Assest {asset} IS present in checked out assets list, but should not")
