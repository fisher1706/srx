import time
from src.api.api import API
from src.resources.messages import Message
from src.resources.tools import Tools
from src.fixtures.decorators import default_expected_code

class TransactionApi(API):
    def create_active_item(self, shipto_id, ordering_config_id, repeat=21, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        transactions_count = self.get_transactions_count(shipto_id=shipto_id)
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/replenishments/list/items/createActiveItem")
        params = {
            "customerId": customer_id,
            "shipToId": shipto_id,
            "orderingConfigId": ordering_config_id
        }
        token = self.get_mobile_distributor_token()
        for _ in range(1, repeat):
            response = self.send_post(url, token, params=params)
            time.sleep(5)
            new_transactions_count = self.get_transactions_count(shipto_id=shipto_id)
            if new_transactions_count >= transactions_count+1:
                if response.status_code == 200:
                    self.logger.info(Message.entity_operation_done.format(entity="Transaction", operation="created"))
                else:
                    self.logger.error(str(response.content))
                if new_transactions_count > transactions_count+1:
                    self.logger.warning("Unexpected count of transactions")
                break
            self.logger.info("Transaction cannot be created now due to the deduplication mechanism. Next attempt after 5 second")
            time.sleep(5)
        else:
            self.logger.error("New transaction has not been created")
            self.logger.error(str(response.content))

    @default_expected_code(200)
    def update_replenishment_item(self, transaction_id, quantity_ordered, status, quantity_shipped=-1, expected_status_code=None):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/replenishments/list/item/update")
        token = self.get_distributor_token()
        if (quantity_shipped == -1 and status in ("SHIPPED", "DELIVERED")):
            quantity_shipped = quantity_ordered
        elif (quantity_shipped == -1 and status == "DO_NOT_REORDER"):
            quantity_shipped = 0
        elif quantity_shipped == -1:
            quantity_shipped = None
        dto = {
            "reorderQuantity": quantity_ordered,
            "shippedQuantity": quantity_shipped,
            "status": status,
            "id": transaction_id,
        }
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Transaction", id=transaction_id, operation="updated"))
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Transaction", operation="updating", status_code=response.status_code, content=response.content))

    def get_transaction(self, sku=None, status=None, shipto_id=None, ids=None):
        params = dict()
        Tools.add_to_dict_if_not_none(params, "productPartSku", sku)
        Tools.add_to_dict_if_not_none(params, "status", status)
        Tools.add_to_dict_if_not_none(params, "shipToIds", shipto_id)
        if ids is not None:
            ids_string = ""
            if isinstance(ids, list):
                for item_id in ids:
                    ids_string += f"{item_id},"
            elif isinstance(ids, (int, str)):
                ids_string = ids
            else:
                self.logger.error(f"Incorrect type 'ids' parameter. Expected 'str', 'int' or 'list'. Now '{type(ids)}'")
            params["replenishmentIds"] = ids
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/replenishments/list/items")
        token = self.get_distributor_token()
        response = self.send_get(url, token, params=params)
        if response.status_code == 200:
            pass
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def get_transactions_count(self, sku=None, status=None, shipto_id=None):
        response = self.get_transaction(sku=sku, status=status, shipto_id=shipto_id)
        return response["totalElements"]

    def get_transaction_id(self, sku=None, status=None, shipto_id=None):
        response = self.get_transaction(sku=sku, status=status, shipto_id=shipto_id)
        return response["entities"][0]["id"]

    def get_transaction_id_and_qty(self, sku=None, status=None, shipto_id=None):
        response = self.get_transaction(sku=sku, status=status, shipto_id=shipto_id)
        return response["entities"][0]["id"], response["entities"][0]["reorderQuantity"]

    def update_transactions_with_specific_status(self, status_before, quantity, status_after):
        transactions_response = self.get_transaction(status=status_before)
        tranactions_list = transactions_response["entities"]
        for item in range(transactions_response["totalElements"]):
            transaction_id = tranactions_list[item]["id"]
            self.update_replenishment_item(transaction_id, quantity, status_after)

    @default_expected_code(200)
    def submit_transaction(self, dto, expected_status_code=None):
        url = self.url.get_api_url_for_env("/customer-portal/customer/replenishment/list")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Transaction", operation="submitted"))
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Transaction", operation="submit", status_code=response.status_code, content=response.content))

    def refresh_order_status(self, order_id, v_2, distributor_id=None):
        url = self.url.get_api_url_for_env("/admin-portal/admin/orders/erp-test/get-order-status")
        params = {
            "distributorId": self.data.ilx_distributor_id if distributor_id is None else distributor_id,
            "orderId": order_id,
            "isV2Api": v_2
        }
        token = self.get_admin_token()
        response = self.send_get(url, token, params=params)
        if response.status_code == 200:
            self.logger.info(f"Order {order_id} has been refreshed")
        else:
            self.logger.error(str(response.content))

    def transactions_bulk_update(self, status, order_ids):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/replenishments/list/statuses/bulk-update")
        token = self.get_distributor_token()
        dto = {
            "all": False,
            "orderIds": order_ids,
            "status": status
        }
        response = self.send_post(url, token, data=dto)
        if response.status_code == 200:
            self.logger.info(f"Orders {order_ids} has been updated")
        else:
            self.logger.error(str(response.content))
