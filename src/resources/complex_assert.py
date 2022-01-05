class ComplexAssert():

    @staticmethod
    def v2_shipped_quantity(current, status, condition):
        if status in ("SHIPPED", "DELIVERED"):
            assert current == condition, f"Shipped Quantity should be equal to {condition}, now {current}"
        else:
            assert current in (0, None), f"Shipped Quantity should be equal to 0, now {current}"
