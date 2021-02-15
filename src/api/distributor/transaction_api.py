from src.api.api import API
from src.resources.messages import Message
from src.fixtures.decorators import Decorator
import time

class TransactionApi(API):
    def create_active_item(self, shipto_id, ordering_config_id, repeat=21):
        transactions_count = self.get_transactions_count(shipto_id=shipto_id)
        for count in range (1, repeat):
            url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/replenishments/list/items/createActiveItem?customerId={self.data.customer_id}&shipToId={shipto_id}&orderingConfigId={ordering_config_id}")
            token = self.get_mobile_distributor_token()
            response = self.send_post(url, token)
            time.sleep(5)
            new_transactions_count = self.get_transactions_count(shipto_id=shipto_id)
            if (new_transactions_count >= transactions_count+1):
                if (response.status_code == 200):
                    self.logger.info("New transaction has been successfully created")
                else:
                    self.logger.error(str(response.content))
                if (new_transactions_count > transactions_count+1):
                    self.logger.warning("Unexpected count of transactions")
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

    def get_transaction(self, sku=None, status=None, customer_id=None, shipto_id=None, ids=None):
        url_string = f"/distributor-portal/distributor/replenishments/list/items?"
        if (sku is not None):
            url_string += f"productPartSku={sku}&"
        if (status is not None):
            url_string += f"status={status}&"
        if (shipto_id is not None):
            url_string += f"shipToIds={shipto_id}"
        if (ids is not None):
            ids_string = ""
            if isinstance(ids, list):
                for id in ids:
                    ids_string += f"{id},"
            elif isinstance(ids, str) or isinstance(ids, int):
                ids_string = ids
            else:
                self.logger.error(f"Incorrect type 'ids' parameter. Expected 'str', 'int' or 'list'. Now '{type(ids)}'")
            url_string += f"replenishmentIds={ids}"
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

    def update_transactions_with_specific_status(self, status_before, quantity, status_after):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/replenishments/list/item/update")
        token = self.get_distributor_token()
        transactions_response = self.get_transaction(status=status_before)
        tranactions_list = transactions_response["entities"]
        for item in range(transactions_response["totalElements"]):
            transaction_id = tranactions_list[item]["id"]
            self.update_replenishment_item(transaction_id, quantity, status_after)

    @Decorator.default_expected_code(200)
    def submit_transaction(self, dto, expected_status_code):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/replenishment/list")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"Transaction has been successfully submitted")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Transaction", operation="submit", status_code=response.status_code, content=response.content))

