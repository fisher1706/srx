import time
from src.api.api import API
from src.api.distributor.transaction_api import TransactionApi

class MobileTransactionApi(API):
    def bulk_create(self, shipto_id, dto, customer_id=None, repeat=10, failed=False, admin_context=None, status=None, first_delay=5): #pylint: disable=R0913
        if customer_id is None:
            customer_id = self.data.customer_id
        if admin_context is not None:
            ta = TransactionApi(admin_context)
        else:
            ta = TransactionApi(self.context)
        if status is None:
            status = "ACTIVE"
        len_of_dto = len(dto)
        transactions_count = ta.get_transactions_count(shipto_id=shipto_id, status=status)
        for _ in range(1, repeat):
            url = self.url.get_api_url_for_env("/distributor-portal/distributor/replenishments/list/items/bulkCreate")
            token = self.get_mobile_distributor_token()
            params = {
                "customerId": customer_id,
                'shipToId': shipto_id
            }
            response = self.send_post(url, token, dto, params=params)
            time.sleep(first_delay)
            new_transactions_count = ta.get_transactions_count(shipto_id=shipto_id, status=status)
            if new_transactions_count >= transactions_count+len_of_dto:
                if response.status_code == 200:
                    self.logger.info("New transactions have been successfully created")
                else:
                    self.logger.error(str(response.content))
                if new_transactions_count > transactions_count+len_of_dto:
                    self.logger.warning("Unexpected count of transactions")
                break
            self.logger.info("Transactions cannot be created now due to the deduplication mechanism. Next attempt after 5 second")
            time.sleep(5)
        else:
            if failed:
                self.logger.info("New transactions have not been created as expected")
            else:
                self.logger.error("New transactions have not been created")
                self.logger.error(str(response.content))
