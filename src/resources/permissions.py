class Permissions():

    @staticmethod
    def catalog_only():
        pass

    @staticmethod
    def set_configured_user(context, permissions):
        if (permissions["user"] is not None):
            context.distributor_email = context.session_context.permission_distributor_email
            context.distributor_password = context.session_context.permission_distributor_password
