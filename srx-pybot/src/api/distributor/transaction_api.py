from src.api.api import API

class TransactionApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_active_item(self, shipto_id, ordering_config_id):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/replenishments/list/items/createActiveItem?customerId="+self.variables.customer_id+"&shipToId="+str(shipto_id)+"&orderingConfigId="+str(ordering_config_id))
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("New transaction has been successfully created")
        else:
            self.logger.error(str(response.content))