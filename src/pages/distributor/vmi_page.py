from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class VmiPage(DistributorPortalPage):
    def follow_location_url(self, customer_id=None, shipto_id=None):
        if (customer_id is None):
            customer_id = self.data.customer_id
        if (shipto_id is None):
            shipto_id = self.data.shipto_id
        self.follow_url(self.url.get_url_for_env(f"storeroomlogix.com/customers/{customer_id}/shiptos/{shipto_id}#vmi-list", "distributor"), hide_intercom=True)