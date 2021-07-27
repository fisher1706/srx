from src.api.distributor.user_api import UserApi
from src.resources.tools import Tools

class Permissions():
    'The class contains the methods for working with permissions and predefined permission sets'

    @staticmethod
    def set_configured_user(base_context, permissions, permission_context=None):
        if permissions is not None:
            ua = UserApi(base_context)

            acl = ua.get_acl_sctructure()
            ua.clear_acl_cache()

            for permission in permissions:
                for item in acl:
                    if item["feature"] == permission["feature"]:
                        actions = item["actions"]
                        for action in actions:
                            if (action["action"]["value"] == "VIEW" and (permission["action"] == "VIEW" or permission["action"] == "EDIT" or permission["action"] == "CONFIGURE")):
                                action["permission"] = True
                            if (action["action"]["value"] == "EDIT" and (permission["action"] == "EDIT" or permission["action"] == "CONFIGURE")):
                                action["permission"] = True
                            if (action["action"]["value"] == "CONFIGURE" and permission["action"] == "CONFIGURE"):
                                action["permission"] = True
                            if (action["action"]["value"] == "ENABLE" and permission["action"] == "ENABLE"):
                                action["permission"] = permission["value"]
                        break
                else:
                    base_context.logger.error(f"No permission '{permission['feature']}' found")

            security_group = Tools.get_dto("security_group_dto.json")
            security_group["entries"] = acl
            security_group["name"] = Tools.random_string_l(10)

            security_group_id = ua.create_security_group(security_group)
            permissions_distributor_users_list = ua.get_distributor_user(email=base_context.session_context.permission_distributor_email)
            permissions_distributor_user = permissions_distributor_users_list[0]
            permissions_distributor_user["userGroup"]["id"] = security_group_id
            base_context.dynamic_context["delete_distributor_security_group_id"].append(security_group_id)

            ua.update_distributor_user(permissions_distributor_user)

            return permission_context
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
    def mobile_buttons(action, value):
        response = [{
            "feature": "distributor.mobile.buttons",
            "action": action,
            "value": value
        }]
        return response

    @staticmethod
    def mobile_cycle_count(action, value):
        response = [{
            "feature": "distributor.mobile.cycle.count",
            "action": action,
            "value": value
        }]
        return response

    @staticmethod
    def mobile_labels(action, value):
        response = [{
            "feature": "distributor.mobile.labels",
            "action": action,
            "value": value
        }]
        return response

    @staticmethod
    def mobile_rfid(action, value):
        response = [{
            "feature": "distributor.mobile.rfid",
            "action": action,
            "value": value
        }]
        return response

    @staticmethod
    def mobile_rfid_manage(action, value):
        response = [{
            "feature": "distributor.mobile.rfid.manage.rfid.tags",
            "action": action,
            "value": value
        }]
        return response

    @staticmethod
    def mobile_rfid_manifest(action, value):
        response = [{
            "feature": "distributor.mobile.rfid.manifest",
            "action": action,
            "value": value
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

    @staticmethod
    def catalog(action):
        response = [{
            "feature": "distributor.general.catalog",
            "action": action
        }]
        return response

    @staticmethod
    def usage_history(action):
        response = [
            {
                "feature": "distributor.general.customers.usage.history",
                "action": action
            },
            {
                "feature": "distributor.general.customers",
                "action": "VIEW"
            }
        ]
        return response

    @staticmethod
    def warehouses(action):
        response = [{
            "feature": "distributor.general.warehouses",
            "action": action
        }]
        return response

    @staticmethod
    def pricing(action):
        response = [{
            "feature": "distributor.general.pricing",
            "action": action
        }]
        return response

    @staticmethod
    def orders(action):
        response = [{
            "feature": "distributor.general.orders",
            "action": action
        }]
        return response

    @staticmethod
    def shiptos(action):
        response = [
            {
                "feature": "distributor.general.shiptos",
                "action": action
            },
            {
                "feature": "distributor.general.customers",
                "action": "VIEW"
            }
        ]
        return response

    @staticmethod
    def locations(action):
        response = [
            {
                "feature": "distributor.general.shiptos",
                "action": "VIEW"
            },
            {
                "feature": "distributor.general.customers",
                "action": "VIEW"
            },
            {
                "feature": "distributor.general.shiptos.vmi.list.locations",
                "action": action
            }
        ]
        return response

    @staticmethod
    def cribcrawls(action):
        response = [
            {
                "feature": "distributor.general.shiptos",
                "action": "VIEW"
            },
            {
                "feature": "distributor.general.customers",
                "action": "VIEW"
            },
            {
                "feature": "distributor.general.shiptos.crib.crawl",
                "action": action
            }
        ]
        return response
