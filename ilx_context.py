class IlxSessionContext():
    ilx_auth_token = None
    ilx_testrail_email = None
    ilx_testrail_password = None
    ilx_environment = None
    ilx_base_data = None
    ilx_credentials = None

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise TypeError("Cannot create new attribute for class Context")

class IlxContext():
    ilx_testrail_run_id = None
    ilx_testrail_case_id = None
    ilx_testrail_status_id = None
    ilx_testrail_comment = None
    ilx_session_context = None
    ilx_auth_token = None
    ilx_data = None
    ilx_username_edi856 = None
    ils_password_edi856 = None

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise TypeError("Cannot create new attribute for class Context")
