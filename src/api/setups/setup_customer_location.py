import copy
from src.api.customer.customer_location_api import CustomerLocationApi
from src.api.setups.setup_organization import SetupOrganization
from src.api.setups.setup_customer_product import SetupCustomerProduct
from src.api.setups.base_setup import BaseSetup
from src.api.setups.general_functions import GeneralFunctions
from src.resources.tools import Tools

class SetupCustomerLocation(BaseSetup):
    def __init__(self, context):
        super().__init__(context)
        self.setup_name = "Location"
        self.options = {
            "product": None,
            "subsite_id": None,
            "supplier_id": None,
            "location_pairs": None,
            "type": "LABEL",
            "autosubmit": None,
            "ohi": None,
            "transaction": None,
            "dsn": None,
            "min": None,
            "max": None,
            "critical_min": None
        }
        self.location = Tools.get_dto("customer_location_dto.json")
        self.location_id = None
        self.product = None
        self.organization = None
        self.transaction = dict()
        self.setup_customer_product = SetupCustomerProduct(self.context)
        self.setup_organization = SetupOrganization(self.context)

    def setup(self):
        self.set_organization()
        self.set_product()
        self.set_location()
        self.set_transaction()

        response = {
            "product": self.product,
            "organization": self.organization,
            "location": self.location,
            "location_id": self.location_id,
            "transaction": self.transaction
        }

        return copy.deepcopy(response)

    def set_organization(self):
        if self.options["subsite_id"] is None or self.options["supplier_id"] is None:
            self.organization = self.setup_organization.setup()

            self.location["orderingConfig"]["product"]["distributor"]["id"] = self.organization["supplier_id"]
            self.location["sharedSpaceId"] = self.organization["subsite_id"]
            self.location["distributorId"] = self.organization["supplier_id"]
        else:
            self.location["orderingConfig"]["product"]["distributor"]["id"] = self.options["supplier_id"]
            self.location["sharedSpaceId"] = self.options["subsite_id"]
            self.location["distributorId"] = self.options["supplier_id"]

    def set_product(self):
        if self.options["product"] is None:
            product_supplier_id = self.organization["supplier_id"] if self.options["supplier_id"] is None else self.options["supplier_id"]
            self.setup_customer_product.add_option("supplier_id", product_supplier_id)
            self.product = self.setup_customer_product.setup()
        else:
            self.product = self.options["product"]

    def set_location(self):
        cla = CustomerLocationApi(self.context)

        GeneralFunctions.fill_location_body(self.location, self.product, self.options)
        print(self.location)
        self.location["orderingConfig"]["product"]["customerSku"] = self.product["customerSku"]
        if self.options["ohi"] == "MAX":
            package_conversion = self.product["packageConversion"] if self.product["packageConversion"] is not None else 1
            self.location["onHandInventory"] = self.location["orderingConfig"]["currentInventoryControls"]["max"] * package_conversion
        else:
            self.location["onHandInventory"] = self.options["ohi"]
        cla.create_location(copy.deepcopy(self.location))

    def set_transaction(self):
        pass
