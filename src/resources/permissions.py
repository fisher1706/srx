from src.api.distributor.user_api import UserApi
from src.resources.tools import Tools

class Permissions():
    @staticmethod
    def set_configured_user(base_context, permissions, permission_context=None):
        if (permissions is not None):
            ua = UserApi(base_context)

            ACL = ua.get_acl_sctructure()
            ua.clear_acl_cache()

            for permission in permissions:
                for item in ACL:
                    if (item["feature"] == permission["feature"]):
                        actions = item["actions"]
                        for action in actions:
                            if (action["action"]["value"] == "VIEW" and (permission["action"] == "VIEW" or permission["action"] == "EDIT" or permission["action"] == "CONFIGURE")):
                                action["permission"] = True
                            if (action["action"]["value"] == "EDIT" and (permission["action"] == "EDIT" or permission["action"] == "CONFIGURE")):
                                action["permission"] = True
                            if (action["action"]["value"] == "CONFIGURE" and permission["action"] == "CONFIGURE"):
                                action["permission"] = True
                        break
                else:
                    base_context.logger.error(f"No permission '{permission['feature']}' found")

            security_group = Tools.get_dto("security_group_dto.json")
            security_group["entries"] = ACL
            security_group["name"] = Tools.random_string_l(10)

            security_group_id = ua.create_security_group(security_group)
            permissions_distributor_users_list = ua.get_distributor_user(email=base_context.session_context.permission_distributor_email)
            permissions_distributor_user = permissions_distributor_users_list[0]
            permissions_distributor_user["userGroup"]["id"] = security_group_id
            base_context.dynamic_context["delete_distributor_security_group_id"].append(security_group_id)

            ua.update_distributor_user(permissions_distributor_user)

            return permission_context
        else:
            return base_context

    @staticmethod
    def distributor_users(action):
        response = [{
            "feature": "distributor.general.users.and.groups",
            "action": action
        }]
        return response

    @staticmethod
    def customers(action):
        response = [{
            "feature": "distributor.general.customers",
            "action": action
        }]
        return response

    @staticmethod
    def rfids(action):
        response = [{
            "feature": "distributor.general.rfid.tagging",
            "action": action
        }]
        return response

    @staticmethod
    def serialization(action):
        response = [{
            "feature": "distributor.general.lot.and.serialization",
            "action": action
        }]
        return response