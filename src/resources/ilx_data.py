class IlxData:

    'The class contains the predefined data using in regression tests'

    def __init__(self, environment):
        if environment == 'dev':
            self.dev_environment()
        elif environment == 'qa':
            self.qa_environment()
        elif environment == 'prod':
            self.prod_environment()

    def dev_environment(self):
        # ILX-ERP
        self.ilx_url = 'https://api.dev.integrationlogix.com/external-api/' \
                       '50ff3a5c-677b-433f-a22d-826659633c61/ilx-test/salesOrdersStatus2'

        # EDI_856
        self.edi_856_url = 'https://api.dev.integrationlogix.com/external-api/' \
                           '12bf8a81-6dd6-4611-b407-368aabcc11f0/test_edi/salesOrdersStatus'

        self.path_out = '/home/oleg/PycharmProjects/srx-robot/src/ilx_cases/outbox/'
        self.path_in = '.src/ilx_cases/inbox/'

        self.host_edi_856 = 'ftps.dev.integrationlogix.com'
        self.inbox_edi_856 = '/test_edi_salesOrdersStatus/EDI/X12_856/Inbox/'
        self.reject_edi_856 = '/test_edi_salesOrdersStatus/EDI/X12_856/Rejected/'
        self.outbox_edi_856 = '/test_edi_salesOrdersStatus/EDI/X12_856/Outbox/'

        # INFOR
        self.ilx_infor_url = 'https://api.qa.integrationlogix.com/external-api' \
                             '/a568e5d3-38d4-4cd1-9aa1-3484afa78a0f/infor_final/infor_final'

    def prod_environment(self):
        pass

    def qa_environment(self):
        # INFOR
        self.ilx_infor_url = 'https://api.qa.integrationlogix.com/external-api' \
                             '/a568e5d3-38d4-4cd1-9aa1-3484afa78a0f/infor_final/infor_final'

        # WMI
        self.ilx_wmi_url = 'https://api.qa.integrationlogix.com/external-api' \
                           '/a568e5d3-38d4-4cd1-9aa1-3484afa78a0f/vmi_sync/vmi_sync'

        # BILLING
        self.ilx_billing_url = 'https://api.qa.integrationlogix.com/external-api' \
                               '/a568e5d3-38d4-4cd1-9aa1-3484afa78a0f/billing_test/billing_test'

        # ECLIPSE PRICE
        self.ilx_billing_url = 'https://api.qa.integrationlogix.com/external-api' \
                               '/a568e5d3-38d4-4cd1-9aa1-3484afa78a0f/get_pricing_eclipse/get_pricing_eclipse'

        # JERRIE
        self.ilx_gerrie_url = 'https://api.qa.integrationlogix.com/external-api' \
                              '/a568e5d3-38d4-4cd1-9aa1-3484afa78a0f/sales_orders_jd/sales_orders_jd'


