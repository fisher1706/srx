from random import random
import random
from datetime import datetime
from pprint import pprint
from ilx_utils import Utils


class GenerateIDE856:

    @staticmethod
    def generate_data_edi_856_rtf(test_type):
        date = datetime.now().strftime('%y%m%d')
        isa13 = format(int(random() * 100)).zfill(9)
        tran_id = int(random() * 1000000)
        _order_id = int(random() * 1000000)
        amt = int(random() * 100)
        ref_number = int(random() * 100000)

        data = {
            0: f'ISA*00*          *00*          *01*047583551ANX   *01*116961628      *'
               f'{date}*0457*U*00401*{isa13}*0*P*|',
            1: 'GS*SH*047583551ANX*116961628*20211102*0457*13*X*004010',
            2: 'ST*856*0024',
            3: f'BSN*00*{tran_id}2021-11-02-04.36.19.72*20211102*0452*0001',
            4: 'HL*1**S',
            5: 'TD1*CNT*1',
            6: 'TD5*B*2*SEE MEMO*D*LUT VAN 3',
            7: f'REF*CN*{tran_id}{format(amt).zfill(3)}/129609',
            8: f'REF*GV*SIQTE-000-{_order_id}-001',
            9: 'REF*OQ*67951849',
            10: 'DTM*011*20211102',
            11: 'N1*BY*LAVAZZA PROFESSIONAL UK LTD*91*072903',
            12: 'N1*ST*LAVAZZA PROFESSIONAL UK LTD*91*000',
            13: 'N1*SF*EUO - LUTON OEM OPS*91*26A',
            14: 'HL*2*1*O',
            15: 'PRF*4900001419',
            16: 'HL*3*2*I',
            17: 'LIN*2*VN*ASADAN1M500944',
            18: f'SN1*2*{amt}*EA',
            19: 'REF*GX*SRX185416',
            20: 'CTT*3',
            21: 'SE*20*0024',
            22: 'GE*1*13',
            23: f'IEA*1*{isa13}',
            24: ''}

        if test_type == 'fail':
            data.update({15: f'PR*{ref_number}'})

        filename = f'ANXEU_STOREROOM_LOGIX_EU_856_OB_19229744_{isa13}.edi'

        return filename, data


class GenerateInforOrderStatusV2:
    response = {
            "response": {
                "cErrorMessage": "",
                "tFieldlist": {
                    "t-fieldlist": None
                },
                "tOelineitemV3": {
                    "t-oelineitemV3": None
                },
                "tOetaxsa": {
                    "t-oetaxsa": [
                        {
                            "seqno": 1,
                            "locallabels": "State",
                            "taxcode": "IN",
                            "localdescrip": "IN - State",
                            "taxgroupnm": "STANDARD",
                            "taxamt": "14.72",
                            "taxsaleamt": "210.23"
                        }
                    ]
                },
                "tOetaxar": {
                    "t-oetaxar": []
                }
            }
        }

    online_field = {
        "lineNo": 1,
        "specNsType": "",
        "prod": "ARINNMLT10",
        "desc1": "ARL NMLT10 1\" NMLT PUSH",
        "desc2": "IN CONN",
        "unit": "EA",
        "price": 312,
        "discAmt": 0,
        "discType": "%",
        "netOrd": 402.48,
        "netAmt": 0,
        "sortFld": "2",
        "rushfl": False,
        "botype": "y",
        "promisedt": "2021-12-14",
        "reqshipdt": "2021-12-14",
        "ordertype": "",
        "orderaltno": 0,
        "tiedorder": "",
        "bono": 2,
    }


    @staticmethod
    def generate_resp_infor(data_infor, field_online, response):
        qty = data_infor.get('qty')
        qty_stk = data_infor.get('qty_stk')

        fields = [{'fieldName': k, 'fieldValue': v, 'seqNo': '1'} for k, v in data_infor.items()
                  if k in ['orderno', 'ordersuf', 'stage', 'custpo']]
        field_online.update({'qtyOrd': qty, 'qtyShip': qty, 'stkqtyord': qty_stk, 'stkqtyship': qty_stk})

        response['response']['tFieldlist']['t-fieldlist'] = fields
        response['response']['tOelineitemV3']['t-oelineitemV3'] = [field_online]

        return response


class GenerateVmiList:
    partNumbers = ["1 GAL CPLG", "1 HUB", "1 PAR CLMP", "1 PLUG", "1 RI AN CLMP"]
    locations = ["CABINET", "WIRE RACK", "SHELF", "CONDUIT RACK", "CRIB DRAWER"]

    def create_string_id(self, data_vmi):
        return f'"{data_vmi["customerId"]}~{random.choice(self.partNumbers)}~{data_vmi["productId"]}"'

    def create_items(self, data_vmi):
        items = [{
            "customerId": data_vmi["customerId"],
            "partNumber": random.choice(self.partNumbers),
            "location": random.choice(self.locations),
            "productId": data_vmi["productId"],
            "minQty": random.randint(100, 200),
            "maxQty": random.randint(100, 200),
            "id": self.create_string_id(data_vmi)
        } for _ in range(data_vmi["pageSize"])]

        return items

    def create_response_vmi(self, data_vmi):
        resp = {
            "metadata": {
                "startIndex": data_vmi["startIndex"],
                "pageSize": data_vmi["pageSize"],
                "totalItems": 100
            },

            "results": self.create_items(data_vmi)
        }

        return resp


class GenerateBilling:
    @staticmethod
    def generate_results(num):
        results = [{
            "referenceId": "test_" + str(i),
            "id": Utils.random_str(),
        } for i in range(num)]

        return results

    def generate_resp_billing(self, num):
        resp = {
            "hasErrors": random.choice([True, False]),
            "results": self.generate_results(num)
        }

        return resp


if __name__ == '__main__':
    g = GenerateVmiList()

    data = {
        "customerId": 60428,
        "productId": 700,
        "pageSize": 5,
        "startIndex": 3,
    }


    x = g.create_string_id(data)
    print(x)

    y = g.create_items(data)
    pprint(y)

    z = g.create_response_vmi(data)
    pprint(z)