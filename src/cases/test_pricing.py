import pytest
import random
import time
from src.resources.tools import Tools
from src.pages.general.login_page import LoginPage
from src.pages.distributor.pricing_page import PricingPage
from src.resources.permissions import Permissions
from src.api.distributor.product_api import ProductApi
from src.api.setups.setup_location import SetupLocation
from src.pages.distributor.vmi_page import VmiPage
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.location_api import LocationApi

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 35
    },
    {
        "user": Permissions.pricing("EDIT"),
        "testrail_case_id": 2277
    }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_pricing_import(ui, permission_ui, permissions, delete_distributor_security_group):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    pp = PricingPage(context)
    pricing_body = pp.pricing_body.copy()
    temporary_price = str(random.choice(range(100)))

    #-------------------
    pricing_body["Distributor SKU"] = "PRICING_SKU"
    pricing_body["Price"] = "$"+temporary_price+".00"
    pricing_body["UOM"] = "M"
    pricing_body["Expiration Date"] = "Fri, Dec 12, 2025"
    #-------------------
    pricing = [
        [pricing_body["Distributor SKU"], temporary_price, pricing_body["UOM"], "12/12/2025 10:15:30"]
    ]
    #-------------------

    lp.log_in_distributor_portal()
    pp.sidebar_pricing()
    pp.select_customer_shipto(customer_name=ui.data.customer_name)
    pp.import_pricing(pricing)
    pp.select_customer_shipto(customer_name=ui.data.customer_name)
    pp.check_price_by_name(pricing_body.copy())

@pytest.mark.regression
def test_cache_pricing(ui):
        # ui.testrail_case_id = permissions["testrail_case_id"]
    pa = ProductApi(ui)
    vp = VmiPage(ui)
    st = SettingsApi(ui)
    lp = LoginPage(ui)
    pp = PricingPage(ui)
    la = LocationApi(ui)



    product_dto = Tools.get_dto("product_dto.json")
    product_dto["partSku"] = "BANANA"
    product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
    product_dto["roundBuy"] = "1"
    product_dto["upc"] = Tools.random_string_u(18)
    product_dto["gtin"] = Tools.random_string_u(18)
    product_dto["manufacturer"] = Tools.random_string_u(18)
    product_dto["manufacturerPartNumber"] = Tools.random_string_u(18)


    setup_location = SetupLocation(ui)
    setup_location.add_option("product",product_dto)
    response_location = setup_location.setup()

    location_responce = la.get_location_by_sku(sku ="Banana",shipto_id=response_location["shipto_id"])
    price = location_responce[0]["orderingConfig"]["price"]
       
    pricing_body = pp.pricing_body.copy()
    temporary_price = str(random.choice(range(100)))

    #-------------------
    pricing_body["Distributor SKU"] = "BANANA"
    pricing_body["Price"] = "$"+temporary_price+".00"
    pricing_body["UOM"] = "M"
    pricing_body["Expiration Date"] = "Fri, Dec 12, 2025"
    #-------------------
    pricing = [
        [pricing_body["Distributor SKU"], temporary_price, pricing_body["UOM"], "12/12/2025 10:15:30"]
    ]
    #-------------------

    lp.log_in_distributor_portal()
    pp.sidebar_pricing()
    pp.select_customer_shipto(customer_name=ui.data.customer_name)
    pp.import_pricing(pricing)

    location_responce_updated = la.get_location_by_sku(sku ="Banana",shipto_id=response_location["shipto_id"])
    price_updated = location_responce[0]["orderingConfig"]["price"]
        
    assert price == price_updated

    response_cache = st.get_cash_settings( shipto_id=response_location["shipto_id"])

    response_cache["pricingSource"]["settings"]["useCache"] = False
    response_cache["pricingSource"]["defaultSettings"]["useCache"] = False
    response_cache["pricingSource"]["useDefault"] = False
    response_cache.pop("orderCloseSettings",None)
    response_cache.pop("replenishmentListRules",None)

    
    st.update_cash_settings(dto= response_cache, shipto_id=response_location["shipto_id"])
    time.sleep(30)

    location_responce_updated2 = la.get_location_by_sku(sku ="Banana",shipto_id=response_location["shipto_id"])
    price_updated2 = location_responce_updated2[0]["orderingConfig"]["price"]
    new_price = float(temporary_price)
    assert price_updated2 == new_price