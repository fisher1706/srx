class SessionContext(object):
    #base credentials
    base_admin_email = None
    base_admin_password = None
    base_distributor_email = None
    base_distributor_password = None
    base_customer_email = None
    base_customer_password = None
    base_checkout_group_email =  None
    base_checkout_group_password = None

    #smoke credentials
    smoke_distributor_email = None
    smoke_distributor_password = None
    smoke_customer_email = None
    smoke_customer_password = None

    smoke_distributor_token = None

    #permission credentials
    permission_distributor_email = None
    permission_distributor_password = None
    permission_customer_email = None
    permission_customer_password = None

    #main
    browser_name = None
    cognito_user_pool_id = None
    cognito_client_id = None
    cognito_checkout_client_id = None
    testrail_email = None
    testrail_password = None
    credentials = None
    environment = None
    url = None
    base_data = None
    smoke_data = None

    def __setattr__(self, key, value):
        if (not hasattr(self, key)):
            raise TypeError("Cannot create new attribute for class SessionContext")
        else:
            object.__setattr__(self, key, value)

class Context(object):
    #credentials
    admin_email = None
    admin_password = None
    distributor_email = None
    distributor_password = None
    customer_email = None
    customer_password = None
    checkout_group_email = None
    checkout_group_password = None

    #tokens
    customer_token = None
    distributor_token = None
    stored_distributor_token = None
    admin_token = None
    checkout_token = None
    checkout_group_token = None

    #main
    session_context = None
    dynamic_context = None
    is_teardown = False
    driver = None
    testrail_case_id = None
    testrail_status_id = None
    testrail_comment = None
    data = None
    logger = None
    warnings_counter = 0

    def __setattr__(self, key, value):
        if (not hasattr(self, key)):
            raise TypeError("Cannot create new attribute for class Context")
        else:
            object.__setattr__(self, key, value)