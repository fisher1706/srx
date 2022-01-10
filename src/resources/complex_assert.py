from src.resources.messages import Message
class ComplexAssert():

    @staticmethod
    def v2_quantity_shipped(current, status, condition):
        if status in ("SHIPPED", "DELIVERED"):
            assert current == condition, Message.assert_default_message.format("Shipped Quantity", condition, current)
        else:
            assert current in (0, None), Message.assert_default_message.format("Shipped Quantity", "0 or None", current)

    @staticmethod
    def transaction(transaction, status, quantity_ordered, quantity_shipped=None, order_id=None, release=None):
        assert transaction["erpOrderId"] == str(order_id), Message.assert_default_message.format("ERP Order ID", order_id, transaction["erpOrderId"])
        assert transaction["release"] == None if release is None else str(release), Message.assert_default_message.format("Release", release, transaction["release"])
        assert transaction["status"] == status, Message.assert_default_message.format("Status", status, transaction["status"])
        assert transaction["reorderQuantity"] == quantity_ordered, Message.assert_default_message.format("Reorder Quantity", quantity_ordered, transaction["reorderQuantity"])
        ComplexAssert.v2_quantity_shipped(transaction["shippedQuantity"], status, quantity_shipped)
