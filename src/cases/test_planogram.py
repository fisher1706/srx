import pytest
from src.pages.general.login_page import LoginPage
from src.pages.distributor.locker_planogram_page import LockerPlanogramPage
from src.api.distributor.location_api import LocationApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.setups.setup_shipto import SetupShipto
from src.api.setups.setup_locker import SetupLocker
from src.api.setups.setup_product import SetupProduct

@pytest.mark.regression
def test_create_noweight_locker_location_via_planogram(ui, delete_shipto, delete_hardware):
    ui.testrail_case_id = 1856

    lp = LoginPage(ui)
    lpp = LockerPlanogramPage(ui)
    la = LocationApi(ui)

    lp.log_in_distributor_portal()

    response_shipto = SetupShipto(ui).setup()
    shipto_id = response_shipto["shipto_id"]
    
    response_product = SetupProduct(ui).setup()
    product_sku = response_product["partSku"]
    round_buy = response_product["roundBuy"]

    setup_locker = SetupLocker(ui)
    setup_locker.add_option("shipto_id", response_shipto["shipto_id"])
    setup_locker.add_option("no_weight")
    setup_locker.setup()

    lpp.follow_locker_planogram_url(shipto_id=shipto_id)
    lpp.create_location_via_planogram(1, 1, product_sku, round_buy, round_buy*3)
    locations = la.get_location_by_sku(shipto_id, product_sku)
    assert len(locations) == 1, "There should be 1 location with SKU = '{product_sku}'"
    assert locations[0]["orderingConfig"]["lockerWithNoWeights"], "Locations should be with NoWeight flag"

@pytest.mark.regression
def test_locker_planogram(ui, delete_shipto, delete_hardware):
    ui.testrail_case_id = 1961

    lp = LoginPage(ui)
    lpp = LockerPlanogramPage(ui)
    sta = ShiptoApi(ui)

    #create shipto
    response_shipto = SetupShipto(ui).setup()

    # create locker with shipto
    setup_locker = SetupLocker(ui)
    setup_locker.add_option("shipto_id", response_shipto["shipto_id"])
    response_locker = setup_locker.setup()

    locker_body = response_locker["locker"]
    locker = locker_body["value"]

    lp.log_in_distributor_portal()
    lpp.sidebar_hardware()
    lpp.open_locker_planogram(locker, response_shipto["shipto_id"])

