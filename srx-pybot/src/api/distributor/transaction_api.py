from src.api.api import API
import time

class TransactionApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_active_item(self, shipto_id, ordering_config_id, repeat=21):
        transactions_count = self.get_transactions_count(status="ACTIVE", shipto_id=shipto_id)
        for count in range (1, repeat):
            url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/replenishments/list/items/createActiveItem?customerId={self.variables.customer_id}&shipToId={shipto_id}&orderingConfigId={ordering_config_id}")
            token = self.get_distributor_token()
            response = self.send_post(url, token)
            new_transactions_count = self.get_transactions_count(status="ACTIVE", shipto_id=shipto_id)
            if (new_transactions_count == transactions_count+1):
                if (response.status_code == 200):
                    self.logger.info("New transaction has been successfully created")
                else:
                    self.logger.error(str(response.content))
                break
            elif (new_transactions_count > transactions_count+1):
                self.logger.error("Unexpected count of transactions")
                break
            self.logger.info("Transaction cannot be created now due to the deduplication mechanism. Next attempt after 5 second")
            time.sleep(5)
        else:
            self.logger.error("New transaction has not been created")
            self.logger.error(str(response.content))

    def update_replenishment_item(self, transaction_id, quantity, status):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/replenishments/list/item/update")
        token = self.get_distributor_token()
        dto = {
            "reorderQuantity": quantity,
            "status": status,
            "id": transaction_id
        }
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Transaction '{transaction_id}' has been successfully updated")
        else:
            self.logger.error(str(response.content))

    def get_transaction(self, sku=None, status=None, customer_id=None, shipto_id=None):
        if (customer_id is None):
            customer_id = self.variables.customer_id
        if (shipto_id is None):
            shipto_id = self.variables.shipto_id
        url_string = f"/distributor-portal/distributor/replenishments/list/customers/{customer_id}/shiptos/{shipto_id}/items/pageable?"
        if (sku is not None):
            url_string += f"productPartSku={sku}&"
        if (status is not None):
            url_string += f"status={status}&"
        url = self.url.get_api_url_for_env(url_string)
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            pass
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def get_transactions_count(self, sku=None, status=None, customer_id=None, shipto_id=None):
        response = self.get_transaction(sku=sku, status=status, customer_id=customer_id, shipto_id=shipto_id)
        return response["totalElements"]

    def get_transaction_id(self, sku=None, status=None, customer_id=None, shipto_id=None):
        response = self.get_transaction(sku=sku, status=status, customer_id=customer_id, shipto_id=shipto_id)
        return response["entities"][0]["id"]

    def get_transaction_id_and_qty(self, sku=None, status=None, customer_id=None, shipto_id=None):
        response = self.get_transaction(sku=sku, status=status, customer_id=customer_id, shipto_id=shipto_id)
        return response["entities"][0]["id"], response["entities"][0]["reorderQuantity"]