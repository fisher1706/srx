class IlxSessionContext:
    ilx_testrail_email = None
    ilx_testrail_password = None
    ilx_environment = None
    ilx_base_data = None
    ilx_credentials = None

    ilx_auth_token = None

    edi_856_auth_token = None
    user_name_edi_856 = None
    password_edi_856 = None

    ilx_infor_token = None

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise TypeError("Cannot create new attribute for class Context")


class IlxContext:
    ilx_testrail_run_id = None
    ilx_testrail_case_id = None
    ilx_testrail_status_id = None
    ilx_testrail_comment = None
    ilx_session_context = None
    ilx_data = None

    ilx_auth_token = None

    edi_856_auth_token = None
    user_name_edi_856 = None
    password_edi_856 = None

    ilx_infor_token = None


    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise TypeError("Cannot create new attribute for class Context")
