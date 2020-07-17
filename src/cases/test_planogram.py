import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.distributor.locker_planogram_page import LockerPlanogramPage
from src.api.distributor.location_api import LocationApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.setups.setup_shipto import setup_shipto
from src.api.setups.setup_locker import setup_locker
from src.api.setups.setup_product import setup_product

class TestPlanogram():
    @pytest.mark.regression
    def test_create_noweight_locker_location_via_planogram(self, ui, delete_shipto, delete_hardware):
        ui.testrail_case_id = 1856

        lp = LoginPage(ui)
        lpp = LockerPlanogramPage(ui)
        la = LocationApi(ui)

        lp.log_in_distributor_portal()

        response_shipto = setup_shipto(ui)
        shipto_id = response_shipto["shipto_id"]
        
        response_product = setup_product(ui)
        product_sku = response_product["partSku"]
        round_buy = response_product["roundBuy"]

        response_locker = setup_locker(ui, shipto=shipto_id, no_weight=True)

        lpp.follow_locker_planogram_url(shipto_id=shipto_id)
        lpp.create_location_via_planogram(1, 1, product_sku, round_buy, round_buy*3)
        locations = la.get_location_by_sku(shipto_id, product_sku)
        assert len(locations) == 1, "There should be 1 location with SKU = '{product_sku}'"
        assert locations[0]["orderingConfig"]["lockerWithNoWeights"] == True, "Locations should be with NoWeight flag"

    @pytest.mark.regression
    def test_locker_planogram(self, ui, delete_shipto, delete_hardware):
        ui.testrail_case_id = 1961

        lp = LoginPage(ui)
        lpp = LockerPlanogramPage(ui)
        sta = ShiptoApi(ui)

        #create shipto
        response_shipto = setup_shipto(ui)

        # create locker with shipto
        response_locker = setup_locker(ui, shipto=response_shipto["shipto_id"])
        locker_body = response_locker["locker"]
        locker = locker_body["value"]
        iothub_body = response_locker["iothub"]

        lp.log_in_distributor_portal()
        lpp.sidebar_hardware()
        lpp.open_locker_planogram(locker, response_shipto["shipto_id"])

