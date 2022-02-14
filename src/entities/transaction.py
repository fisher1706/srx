class Transaction():
    def __init__(self, status=None, quantity_ordered=None, quantity_shipped=None):
        self.status = status
        self.quantity_ordered = quantity_ordered
        self.quantity_shipped = quantity_shipped

    @staticmethod
    def several(*args):
        transactions = list()
        for transaction in args:
            transactions.append(Transaction(transaction[0], transaction[1], transaction[2]))
        return transactions
        