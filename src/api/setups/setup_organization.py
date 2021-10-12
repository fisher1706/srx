import copy
from src.api.setups.base_setup import BaseSetup
from src.api.setups.setup_shipto_customer import SetupShiptoCustomer
from src.api.customer.organization_api import OrganizationApi
from src.resources.tools import Tools

class SetupOrganization(BaseSetup):
    def __init__(self, context):
        super().__init__(context)
        self.setup_name = "Organization"
        self.options = {
            "supplier": None,
            "site": None,
            "subsite": None,
            "subsite.site_id": None,
            "shipto": None
        }
        self.supplier = Tools.get_dto("supplier_dto.json")
        self.supplier_id = None
        self.site = Tools.get_dto("site_dto.json")
        self.site_id = None
        self.subsite = Tools.get_dto("subsite_dto.json")
        self.subsite_id = None
        self.shipto = Tools.get_dto("customer_shipto_dto.json")
        self.shipto_id = None
        self.setup_shipto_customer = SetupShiptoCustomer(self.context)
        self.oa = OrganizationApi(self.context)

    def setup(self):
        self.set_site()
        self.set_subsite()
        self.set_supplier()
        self.set_shipto()

        response = {
            "user": self.supplier,
            "user_id": self.supplier_id,
            "site": self.site,
            "site_id": self.site_id,
            "subsite": self.subsite,
            "subsite_id": self.subsite_id,
            "shipto": self.shipto,
            "shipto_id": self.shipto_id
        }

        return copy.deepcopy(response)

    def set_site(self):
        if isinstance(self.options["site"], bool) and self.options["site"]:
            self.site["name"] = Tools.random_string_l(10)
            self.site["number"] = Tools.random_string_l(13)
            self.site_id = self.oa.create_site(copy.deepcopy(self.site))
            if self.site_id is not None:
                self.context.dynamic_context["delete_site_id"].append(self.site_id)

    def set_subsite(self):
        if isinstance(self.options["subsite"], bool) and self.options["subsite"]:
            self.subsite["name"] = Tools.random_string_l(10)
            self.subsite["number"] = Tools.random_string_l(13)
            self.subsite["facilityId"] = self.site_id if self.options["subsite.site_id"] is None else self.options["subsite.site_id"]
            self.subsite_id = self.oa.create_subsite(copy.deepcopy(self.subsite))
            if self.subsite_id is not None:
                self.context.dynamic_context["delete_subsite_id"].append(self.subsite_id)

    def set_supplier(self):
        if isinstance(self.options["supplier"], bool) and self.options["supplier"]:
            self.supplier["name"] = Tools.random_string_l(10)
            self.supplier_id = self.oa.create_supplier(copy.deepcopy(self.supplier))
            if self.supplier_id is not None:
                self.context.dynamic_context["delete_supplier_id"].append(self.supplier_id)

    def set_shipto(self):
        pass
