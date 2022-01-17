class Response:
    def __init__(self, response):
        self.response = response
        self.response_json = response.json()
        self.response_status = response.status_code
        self.data = self.response_json.get('response')

    def assert_response_status(self, status_code):
        assert self.response_status == status_code, f'incorrect response status {self.response_status}'

    def validate_response_schema(self, schema):
        schema.parse_obj(self.response_json)

    def validate_response_data(self, order_data):
        print(f"\nOrder data:{order_data}")

        assert len(self.data) == len(order_data), f'different data between order and shipment for: {self.response_json}'

        next_ordered = list()

        number = len(order_data)
        for num in range(number):
            ordered = self.data[num].get('items')[0].get('quantityOrdered')
            shipped = self.data[num].get('items')[0].get('quantityShipped')
            status = self.data[num].get('transactionType')

            stock_qtn = order_data[num].get('qnt')
            stock_status = order_data[num].get('status')

            assert shipped == stock_qtn, f'difference between data_order and data_ilx {self.data[num].get("id")}'

            if stock_status in ['Invoice']:
                assert status == 'DELIVERED', f'incorrect status for: {self.data[num].get("id")}'
            else:
                assert status == 'ORDERED', f'incorrect status for: {self.data[num].get("id")}'

            delta = ordered - shipped

            if delta > 0:
                next_ordered.append(delta)
            else:
                next_ordered.append(0)

            if num > 0:
                assert ordered == next_ordered[num - 1], f'incorrect quantity for: {self.data[num].get("id")}'

    def validate_response_edi(self, edi_data):
        assert self.data[0].get('id') == edi_data[0].split('*')[2], f'incorrect id for: {self}'
        assert self.data[0].get('poNumber') == edi_data[2].split('*')[1], f'incorrect poNumber for: {self}'
        assert self.data[0].get('items')[0].get('quantity') == edi_data[3].split('*')[2], \
            f'incorrect quantity for: {self}'

    def validate_response_infor(self, infor_data):
        assert self.data[0].get('id') == infor_data.get('orderno'), f'incorrect orderno for: {self.response_json}'
        assert self.data[0].get('release') == infor_data.get('ordersuf'), f'incorrect release for: {self.response_json}'
        assert self.data[0].get('items')[0].get('quantityShipped') == infor_data.get('qty_stk'), \
            f'incorrect quantityShipped for: {self.response_json}'
        assert self.data[0].get('items')[0].get('quantityOrdered') == infor_data.get('qty_stk'), \
            f'incorrect quantityOrdered for: {self.response_json}'

        if infor_data.get('stage') in ['Shp', 'Inv', 'Pd']:
            assert str(self.data[0].get('transactionType')) == 'SHIPPED', \
                f'incorrect transactionType for: {self.response_json}'
        elif infor_data.get('stage') in ['Ord', 'Pck']:
            assert self.data[0].get('transactionType') == 'ORDERED', \
                f'incorrect transactionType for: {self.response_json}'
        else:
            assert self.data[0].get('transactionType') == 'QUOTED', \
                f'incorrect transactionType for: {self.response_json}'

    def __str__(self):
        return f"\nStatus code: {self.response_status}" \
               f"\nRequested url: {self.response.url}" \
               f"\nResponse body: {self.response_json}" \

