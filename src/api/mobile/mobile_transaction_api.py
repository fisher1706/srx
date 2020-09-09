from src.api.api import API
import time

class MobileTransactionApi(API):
    def bulk_create(self, shipto_id, customer_id, dto):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/replenishments/list/items/bulkCreate")
        token = self.get_distributor_token()
        params = {
            "customerId" : customer_id,
            'shipToId' : shipto_id
        }
        response = self.send_post(url, token, dto, params=params)
        time.sleep(5)