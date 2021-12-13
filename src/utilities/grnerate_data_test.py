from random import random
from datetime import datetime


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
