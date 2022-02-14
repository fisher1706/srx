import time


class IlxUtils:

    @staticmethod
    def generate_name(name):
        timestamp = int(time.time())
        return f'{name}-{timestamp}'

    @staticmethod
    def diff(list_1, list_2):
        pairs = zip(list_1, list_2)
        resp = [(x, y) for x, y in pairs if x != y]
        return resp
