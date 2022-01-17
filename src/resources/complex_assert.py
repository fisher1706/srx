import logging
from typing import List
from src.resources.messages import Message
from src.entities.transaction import Transaction

class ComplexAssert():

    @staticmethod
    def v2_quantity_shipped(current, status, condition):
        if status in ("SHIPPED", "DELIVERED"):
            assert current == condition, Message.assert_default_message.format("Shipped Quantity", condition, current)
        else:
            assert current in (0, None), Message.assert_default_message.format("Shipped Quantity", "0 or None", current)

    @staticmethod
    def transaction(transaction, status, quantity_ordered, quantity_shipped=None, order_id=None, release=None, backordered_id=None):
        order_id = None if order_id is None else str(order_id)
        release = None if release is None else str(release)
        assert transaction["erpOrderId"] == order_id, Message.assert_default_message.format("ERP Order ID", order_id, transaction["erpOrderId"])
        assert transaction["release"] == release, Message.assert_default_message.format("Release", release, transaction["release"])
        assert transaction["status"] == status, Message.assert_default_message.format("Status", status, transaction["status"])
        assert transaction["reorderQuantity"] == quantity_ordered, Message.assert_default_message.format("Reorder Quantity", quantity_ordered, transaction["reorderQuantity"])
        assert transaction["backorderedItemId"] == backordered_id, Message.assert_default_message.format("Backordered ID", backordered_id, transaction["backorderedItemId"])
        ComplexAssert.v2_quantity_shipped(transaction["shippedQuantity"], status, quantity_shipped)

    @staticmethod
    def v2_backorder_or_active(current, init: List[Transaction], received: List[Transaction], ohi_packages=None, location_max=None) -> int:
        'This method works correctly only for cases where present either BACKORDER ot ACTIVE, not for both'

        count_init = len(init)
        count_received = len(received)
        quantity_on_reorder = 0
        active_quantity = None
        additional_transactions = 0
        if count_init == 1: # split 1 transaction with N>1
            backorder_quantity = None
            shipped_or_delivered = False #if there are neither SHIPPED nor DELIVERED then no BACKORDERED
            backordered_quantity_sum = 0

            #calculate and check BACKORDERED transaction
            for transaction in received:
                if transaction.status in ("SHIPPED", "DELIVERED"):
                    shipped_or_delivered = True
                    backordered_quantity_sum += transaction.quantity_shipped
                elif transaction.status in ("QUOTED", "ORDERED"):
                    backordered_quantity_sum += transaction.quantity_ordered
            if (shipped_or_delivered and init[0].quantity_ordered > backordered_quantity_sum):
                assert current["totalElements"] == count_received+1, \
                    Message.assert_default_message.format("Number of transactions", count_received+1, current["totalElements"])
                backorder_quantity = init[0].quantity_ordered - backordered_quantity_sum #expected backordered quantity
                backordered_transaction = current["entities"][count_received]
                assert backordered_transaction["status"] == "BACKORDERED", \
                    Message.assert_default_message.format("Status", "BACKORDERED", backordered_transaction["status"])
                logging.info("BACKORDERED transaction is present")
                assert backordered_transaction["reorderQuantity"] == backorder_quantity
                logging.info(f"BACKORDERED quantity equal to {backorder_quantity}")
                additional_transactions += 1
            else:
                logging.info("No SHIPPED/DELIVERED or no backorder quantity")

        #calculate and check ACTIVE transaction
        #implemented only for reorder controls option 'As Issued'
        if (location_max is not None and ohi_packages is not None and additional_transactions == 0):
            for transaction in received:
                if transaction.status in ("QUOTED", "ORDERED"):
                    quantity_on_reorder += transaction.quantity_ordered
                elif transaction.status == "SHIPPED":
                    quantity_on_reorder += transaction.quantity_shipped
            active_quantity = location_max - (quantity_on_reorder + ohi_packages) #expected active quantity
            if active_quantity > 0:
                assert current["totalElements"] == count_received+1, \
                    Message.assert_default_message.format("Number of transactions", count_received+1, current["totalElements"])
                active_transaction = current["entities"][count_received]
                assert active_transaction["status"] == "ACTIVE", \
                    Message.assert_default_message.format("Status", "ACTIVE", active_transaction["status"])
                logging.info("ACTIVE transaction is present")
                assert active_transaction["reorderQuantity"] == active_quantity
                logging.info(f"ACTIVE quantity equal to {active_quantity}")
                additional_transactions += 1
            else:
                logging.info("No new ACTIVE transaction by reorder controls")
        else:
            logging.info("Reorder controls is disabled or there are BACKOERDERED transactions")

        return additional_transactions
