from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class VmiPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def follow_location_url(self, customer_id=None, shipto_id=None):
        if (customer_id is None):
            customer_id = self.variables.customer_id
        if (shipto_id is None):
            shipto_id = self.variables.shipto_id
        self.follow_url(self.url.get_url_for_env("storeroomlogix.com/customers/"+str(customer_id)+"/shiptos/"+str(shipto_id)+"#vmi-list", "distributor"), hide_intercom=True)