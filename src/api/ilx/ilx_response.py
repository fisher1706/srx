from src.api.api import API
from context import Context
from src.resources.local_credentials import LocalCredentials


class Response:
    def __init__(self, response):
        self.response = response
        self.response_json = response.json()
        self.response_status = response.status_code
        self.data = self.response_json.get('response')

    def assert_response_status(self, status_code):
        assert self.response_status == status_code

    def validate_response_schema(self, schema):
        schema.parse_obj(self.response_json)

    def validate_response_data(self, order_data):
        print(f"\nOrder data:{order_data}")

        assert len(self.data) == len(order_data)

        next_ordered = list()
        for number in range(len(order_data)):
            ordered = self.data[number].get('items')[0].get('quantityOrdered')
            shipped = self.data[number].get('items')[0].get('quantityShipped')
            status = self.data[number].get('transactionType')

            stock_qtn = order_data[number].get('qnt')
            stock_status = order_data[number].get('status')

            assert shipped == stock_qtn, f'difference between data_order and data_ilx {self.data[number].get("id")}'

            if stock_status in ['Invoice']:
                assert status == 'DELIVERED', f'incorrect status for {self.data[number].get("id")}'
            else:
                assert status == 'ORDERED', f'incorrect status for {self.data[number].get("id")}'

            delta = ordered - shipped

            if delta > 0:
                next_ordered.append(delta)
            else:
                next_ordered.append(0)

            if number > 0:
                assert ordered == next_ordered[number - 1], f'incorrect status for {self.data[number].get("id")}'

    def __str__(self):
        return f"\nStatus code: {self.response_status}" \
               f"\nRequested url: {self.response.url}" \
               f"\nResponse body: {self.response_json}" \





if __name__ == '__main__':
    cont = Context()

    print(cont.__dict__)
