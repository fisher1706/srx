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


class GetPricingEclipse:
    currency = ['EUR', 'USD', 'UAH']

    def create_rep_price_eclipse(self, product, qnt):
        response = {
            "productId": product,
            "branch": Utils.random_str(size=3),
            "pricingPerQuantity": qnt,
            "pricingUOM": "c",
            "productUnitPrice": {
                "value": '{:.8f}'.format(random.randint(1000, 2000) * 0.01),
                "currency": random.choice(self.currency)
            },
            "quantityBreaks": []
        }

        return response


class GetResponseGerrie:

    @staticmethod
    def generate_resp_gerrie(data_test):
        response = {
            'response': [
                {
                    "id": Utils.random_str(8),
                    "items": [
                        {
                            "dsku": str(random.randint(100, 500)),
                            "msku": str(random.randint(10, 50)),
                            "quantityOrdered": data_test.get("quantityOrdered"),
                            "quantityShipped": data_test.get("quantityShipped"),
                        }
                    ],
                    "release": Utils.random_str(10),
                    "poNumber": Utils.random_str(6),
                    "transactionType": data_test.get("tran_type")
                }
            ]
        }

        return response


class GenerateQuoteInfor:
    @staticmethod
    def create_response_quote_infor(data_test):
        response = {
            "response": {
                "sxt_func_ack": {"sxt_func_ack": []},
                "sxapi_oehdr": {
                    "sxapi_oehdr": [
                        {
                            "invoiceDt": "",
                            "invNr": data_test.get('invNr'),
                            "invSuf": "00",
                            "custPo": str(random.randint(1000, 2000)),
                            "invType": "",
                            "refer": "",
                            "partnerId": "",
                            "buyParty": "",
                            "dept": "",
                            "orderDisp": "",
                            "event": "",
                            "vendNo2": "",
                            "cancelDt": datetime.now().strftime("%m/%d/%y"),
                            "shipDt": "",
                            "promiseDt": datetime.now().strftime("%m/%d/%y"),
                            "reqShipDt": datetime.now().strftime("%m/%d/%y"),
                            "shipVia": "",
                            "poIssDt": "",
                            "enterDt": datetime.now().strftime("%m/%d/%y"),
                            "pkgId": "",
                            "ackType": "AD",
                            "currentDt": datetime.now().strftime("%m/%d/%y"),
                            "user1": "",
                            "user2": "",
                            "user3": "",
                            "userInv": "",
                            "transType": data_test.get('transType'),
                            "shipInstr": "",
                            "placedBy": "",
                            "whse": str(random.randint(10, 20)),
                            "coreChg": "",
                            "datcCost": "",
                            "downPmt": "",
                            "specDiscAmt": "",
                            "restockAmt": "",
                            "taxAmt": '{:.2f}'.format(random.randint(10, 20) * 0.01).zfill(10),
                            "gstTaxAmt": "",
                            "pstTaxAmt": "",
                            "woDiscAmt": "",
                            "termsDiscAmt": '{:.2f}'.format(random.randint(10, 20) * 0.1).zfill(13),
                            "coNo": str(random.randint(1, 10))
                        }
                    ]
                },
                "sxapi_oeitm": {"sxapi_oeitm": []},
                "cErrorMessage": ""
            }
        }

        return response


class GenerateQuoteEclipse:
    @staticmethod
    def create_response_quote_eclipse(data_test):
        response = {
            "results": [
                {
                    "generations": [{
                        "status": data_test.get('orderStatus'),
                    }],
                    "id": data_test.get('productId')
                }
            ]
        }

        return response


class GetPricingD1:

    @staticmethod
    def create_resp_price_d1(prod_id):
        response = {
            "unitName": prod_id,
            "price": '{:.2f}'.format(random.randint(1000, 2000) * 0.01),
        }

        return response


class GetBillingInfor:
    @staticmethod
    def create_resp_billing_infor(num):
        date_now = datetime.now().strftime('%d/%m/%y')

        response = {
            "response": {
                "sxt_func_ack": {
                    "sxt_func_ack": [
                        {
                            "coNo": 1,
                            "correlation_data": "",
                            "data1": f"{num}-00",
                            "errorNo": 0,
                            "msg": f"Order: {num}-00, has been created.",
                            "seqNo": 0,
                            "trxType": ""
                        }
                    ]
                },
                "sxapi_oehdr": {
                    "sxapi_oehdr": [
                        {
                            "invoiceDt": "",
                            "invNr": f"0{num}",
                            "invSuf": "00",
                            "custPo": "SX27714_32",
                            "invType": "",
                            "refer": "",
                            "partnerId": "IDCX_COMAU-01",
                            "buyParty": "",
                            "dept": "",
                            "orderDisp": "",
                            "event": "",
                            "vendNo2": "",
                            "cancelDt": "",
                            "shipDt": "",
                            "promiseDt": f"{date_now}",
                            "reqShipDt": f"{date_now}",
                            "shipVia": "CAP WEST",
                            "poIssDt": "        ",
                            "enterDt": f"{date_now}",
                            "pkgId": "",
                            "ackType": "AD",
                            "currentDt": f"{date_now}",
                            "user1": "",
                            "user2": "",
                            "user3": "",
                            "userInv": "",
                            "transType": "SO",
                            "shipInstr": "",
                            "placedBy": "",
                            "whse": "X610",
                            "coreChg": "",
                            "datcCost": "",
                            "downPmt": "",
                            "specDiscAmt": "",
                            "restockAmt": "",
                            "taxAmt": "",
                            "gstTaxAmt": "",
                            "pstTaxAmt": "",
                            "woDiscAmt": "",
                            "termsDiscAmt": "",
                            "coNo": "1"
                        }
                    ]
                },
                "sxapi_oeitm": {
                    "sxapi_oeitm": [
                        {
                            "lineIden": "0001",
                            "qtyUom": "EA",
                            "prodSvcCd": "",
                            "sellerProd": "WOOD114030K12M005",
                            "buyerProd": "",
                            "descrip": "WOOD 114030K12M005 MC 4P",
                            "user1": "",
                            "user2": "",
                            "user3": "",
                            "user4": "",
                            "user5": "",
                            "ordStatCd": "",
                            "chgCd": "",
                            "boType": "y",
                            "user6": "",
                            "user7": "",
                            "user8": "",
                            "user9": "",
                            "user10": "",
                            "specCostTy": "Y",
                            "sCostUnit": "000001.000000",
                            "xrefProdTy": "",
                            "taxableFl": "n",
                            "taxableTy": "",
                            "taxGroup": "1",
                            "promiseDt": f"{date_now}",
                            "reqShipDt": f"{date_now}",
                            "specNsType": "s",
                            "upc": "",
                            "sxLineNo": "0001",
                            "qtyShip": "000001.00",
                            "price": "0000045.68000",
                            "discPct": "",
                            "qtyOrd": "000001.00",
                            "discAmt": "",
                            "taxAmt1": "0000000.00000",
                            "taxAmt2": "0000000.00000",
                            "taxAmt3": "0000000.00000",
                            "taxAmt4": "0000000.00000",
                            "upcSection1": "000000000000",
                            "upcSection2": "000000000000",
                            "upcSection3": "000000786788",
                            "upcSection4": "000000002291",
                            "upcSection5": "000000000000",
                            "upcSection6": "000000000000",
                            "restockChg": "000000000.00",
                            "spCostUnit": "EA"
                        }
                    ]
                },
                "cErrorMessage": ""
            }
        }

        return response


class InforTransfers:
    @staticmethod
    def get_resp_infor_transfers(data):
        response = {
            "cErrorMessage": data,
            "tFieldlist": {
                "t-fieldlist": [
                    {
                        "wtno": random.randint(1, 10),
                        "stage": "Ord",
                        "wtsuf": random.randint(1, 10),
                        "transtype": Utils.random_str(),
                        "shipfmwhse": Utils.random_str(),
                        "shiptowhse": Utils.random_str()
                    }
                ]
            },
            "tWtlineitemv2": {
                "t-wtlineitemv2": [
                    {
                        "bono": random.randint(1, 10),
                        "unit": Utils.random_str(),
                        "duedt": Utils.random_str(),
                        "lineno": random.randint(1, 10),
                        "netamt": random.randint(1, 10),
                        "netord": random.randint(1, 10),
                        "netrcv": random.randint(1, 10),
                        "qtyord": random.randint(1, 10),
                        "qtyrcv": random.randint(1, 10),
                        "qtyship": random.randint(1, 10),
                        "sortFld": Utils.random_str(),
                        "prodcost": random.randint(1, 10),
                        "shipprod": Utils.random_str(),
                        "unitconv": random.randint(1, 10),
                        "approvety": Utils.random_str(),
                        "ordertype": Utils.random_str(),
                        "proddesc": Utils.random_str(),
                        "proddesc2": Utils.random_str(),
                        "stkqtyord": random.randint(1, 10),
                        "stkqtyrcv": random.randint(1, 10),
                        "tiedorder": Utils.random_str(),
                        "nonstockty": Utils.random_str(),
                        "orderaltno": random.randint(1, 10),
                        "stkqtyship": random.randint(1, 10),
                        "prodinrcvfl": random.choice([True, False]),
                        "rcvunavailfl": random.choice([True, False])
                    }
                ]
            }
        }

        return response


if __name__ == '__main__':
    g = GetPricingD1()
    item = 'zapel'

    resp = g.create_resp_price_d1(item)

    print(resp)
