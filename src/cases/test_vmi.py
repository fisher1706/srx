import pytest
import copy
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.resources.permissions import Permissions
from src.pages.general.login_page import LoginPage
from src.pages.distributor.vmi_page import VmiPage
from src.api.distributor.location_api import LocationApi
from src.api.distributor.settings_api import SettingsApi
from src.api.customer.customer_vmi_list_api import CustomerVmiListApi
from src.api.setups.setup_product import SetupProduct
from src.api.setups.setup_shipto import SetupShipto
from src.api.setups.setup_location import SetupLocation

class TestVmi():
    @pytest.mark.regression
    def test_vmi_list_partial_sku_match(self, ui):
        ui.testrail_case_id = 1838

        lp = LoginPage(ui)
        vp = VmiPage(ui)

        lp.log_in_distributor_portal()

        product_sku = f"{Tools.random_string_u(7)} {Tools.random_string_u(7)}"

        setup_product = SetupProduct(ui)
        setup_product.add_option("sku", product_sku)
        setup_product.setup()

        vp.follow_location_url()
        vp.wait_until_page_loaded()
        vp.click_id(Locator.id_add_button)
        vp.input_data_xpath(product_sku, Locator.xpath_dialog+Locator.xpath_select_box+"//input")
        vp.wait_until_dropdown_list_loaded(1)
        vp.check_found_dropdown_list_item(Locator.xpath_dropdown_list_item, product_sku)

    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": 2288
        },
        { 
            "user": Permissions.locations("EDIT"),
            "testrail_case_id": 2292
        }
        ])
    @pytest.mark.acl
    @pytest.mark.regression
    def test_location_crud(self, ui, permission_ui, permissions, delete_distributor_security_group, delete_shipto):
        ui.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

        lp = LoginPage(context)
        vp = VmiPage(context)
        location_body = vp.location_body.copy()
        edit_location_body = vp.location_body.copy()

        response_product = SetupProduct(ui).setup()
        response_shipto = SetupShipto(ui).setup()

        #-------------------
        location_body["sku"] = response_product["partSku"]
        location_body["orderingConfig.currentInventoryControls.min"] = response_product["roundBuy"]
        location_body["orderingConfig.currentInventoryControls.max"] = response_product["roundBuy"]*3
        location_body["attributeName1"] = "loc1"
        location_body["attributeValue1"] = "loc1"
        location_body["customerSku"] = Tools.random_string_l()
        #-------------------
        edit_location_body["customerSku"] = Tools.random_string_l()
        #-------------------

        lp.log_in_distributor_portal()
        vp.follow_location_url(shipto_id=response_shipto["shipto_id"])
        vp.wait_until_page_loaded()
        vp.create_location(location_body.copy())
        vp.check_last_location(location_body.copy())

    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": 2294
        },
        { 
            "user": Permissions.locations("EDIT"),
            "testrail_case_id": 2295
        }
        ])
    @pytest.mark.acl
    @pytest.mark.regression
    def test_location_crud_api(self, api, permission_api, permissions, delete_distributor_security_group, delete_shipto):
        api.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(api, permissions["user"], permission_context=permission_api)

        la = LocationApi(context)

        response_product = SetupProduct(api).setup()
        response_shipto = SetupShipto(api).setup()

        location_dto = Tools.get_dto("location_dto.json")
        location_dto["attributeName1"] = "loc1"
        location_dto["attributeValue1"] = "loc1"
        location_dto["orderingConfig"] = {
            "product": {
                "partSku": response_product["partSku"]
            },
            "type": "LABEL",
            "currentInventoryControls": {
                "min": response_product["roundBuy"],
                "max": response_product["roundBuy"]*3
            }
        }
        location_list = [copy.deepcopy(location_dto)]
        la.create_location(location_list, response_shipto["shipto_id"])

        location_1 = la.get_location_by_sku(response_shipto["shipto_id"], response_product["partSku"])[0]
        location_id = location_1["id"]
        assert location_1["attributeName1"] == location_dto["attributeName1"]
        assert location_1["attributeValue1"] == location_dto["attributeValue1"]
        location_1["attributeName1"] = "edit1"
        location_1["attributeValue1"] = "edit1"

        location_list = [copy.deepcopy(location_1)]
        la.update_location(location_list, response_shipto["shipto_id"])

        location_2 = la.get_location_by_sku(response_shipto["shipto_id"], response_product["partSku"])[0]
        assert location_1["attributeName1"] == location_2["attributeName1"]
        assert location_1["attributeValue1"] == location_2["attributeValue1"]

        la.delete_location(location_id, response_shipto["shipto_id"])

    @pytest.mark.acl
    @pytest.mark.regression
    def test_location_crud_view_permission(self, api, permission_api, delete_distributor_security_group, delete_shipto):
        api.testrail_case_id = 2293
        Permissions.set_configured_user(api, Permissions.locations("VIEW"))

        la = LocationApi(permission_api)

        response_product = SetupProduct(api).setup()
        response_shipto = SetupShipto(api).setup()

        location_dto = Tools.get_dto("location_dto.json")
        location_dto["attributeName1"] = "loc1"
        location_dto["attributeValue1"] = "loc1"
        location_dto["orderingConfig"] = {
            "product": {
                "partSku": response_product["partSku"]
            },
            "type": "LABEL",
            "currentInventoryControls": {
                "min": response_product["roundBuy"],
                "max": response_product["roundBuy"]*3
            }
        }
        location_list = [copy.deepcopy(location_dto)]
        la.create_location(location_list, response_shipto["shipto_id"], expected_status_code=400)

        setup_location = SetupLocation(api)
        setup_location.add_option("product", response_product)
        setup_location.add_option("shipto_id", response_shipto["shipto_id"])
        response_location = setup_location.setup()

        location_id = la.get_location_by_sku(response_shipto["shipto_id"], response_product["partSku"])[0]["id"]
        assert location_id == response_location["location_id"]

        la.update_location(location_list, response_shipto["shipto_id"], expected_status_code=400)
        la.delete_location(location_id, response_shipto["shipto_id"], expected_status_code=400)

    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": 2296
        },
        { 
            "user": Permissions.locations("EDIT"),
            "testrail_case_id": 2297
        }
        ])
    @pytest.mark.acl
    @pytest.mark.regression
    def test_location_import(self, ui, permission_ui, permissions, delete_distributor_security_group, delete_shipto):
        ui.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

        lp = LoginPage(context)
        vp = VmiPage(context)
        location_body = vp.location_body.copy()

        response_product = SetupProduct(ui).setup()
        response_shipto = SetupShipto(ui).setup()

        #-------------------
        location_body["sku"] = response_product["partSku"]
        location_body["orderingConfig.currentInventoryControls.min"] = response_product["roundBuy"]
        location_body["orderingConfig.currentInventoryControls.max"] = response_product["roundBuy"]*3
        location_body["attributeName1"] = "loc1"
        location_body["attributeValue1"] = "loc1"
        location_body["type"] = "LABEL"
        #-------------------
        locations = [
            [location_body["attributeName1"], location_body["attributeValue1"], None, None, None, None, None, None, location_body["sku"], location_body["orderingConfig.currentInventoryControls.min"], location_body["orderingConfig.currentInventoryControls.max"], location_body["type"], None, None, None, None, None]
        ]
        #-------------------

        lp.log_in_distributor_portal()
        vp.follow_location_url(shipto_id=response_shipto["shipto_id"])
        vp.wait_until_page_loaded()
        vp.import_location(locations)
        vp.check_last_location(location_body.copy())

    @pytest.mark.regression
    def test_vmi_list_settings_customer_portal(self, api, delete_shipto):
        api.testrail_case_id = 2467

        sa = SettingsApi(api)
        cvla = CustomerVmiListApi(api)

        response_location = SetupLocation(api).setup()

        dto = Tools.get_dto("vmi_settings_dto.json")
        fields = copy.deepcopy(dto["settings"])
        fields.pop("useDefault")
        fields.pop("enableVmiList")
        
        for field in fields.keys():
            dto_copy = copy.deepcopy(dto)
            dto_copy["settings"][field] = "VIEW"
            sa.update_vmi_settings(dto_copy, response_location["shipto_id"])
            location = cvla.get_locations(shipto_id=response_location["shipto_id"])[0]
            mapping = {
                "autoSubmit": "autoSubmit" in location,
                "createdOn": "createdAt" in location,
                "surplus": "surplus" in location,
                "manufacturerSku": "manufacturerPartNumber" in location["orderingConfig"]["product"],
                "inventoryStatus": "inventoryStatus" in location,
                "ohi": "onHandInventory" in location,
                "asset": "assetFlag" in location["orderingConfig"]["product"],
                "serialization": "serialized" in location and "serialized" in location["orderingConfig"]["product"],
                "lot": "lot" in location,
                "triggerType": "type" in location["orderingConfig"],
                "suggestedMinMax": "suggestedInventoryControls" in location["orderingConfig"],
                "location": "attributeName1" in location and "attributeValue1" in location and 
                            "attributeName2" in location and "attributeValue2" in location and
                            "attributeName3" in location and "attributeValue3" in location and
                            "attributeName4" in location and "attributeValue4" in location,
                "distributorSku": "partSku" in location["orderingConfig"]["product"],
                "limits": "currentInventoryControls" in location["orderingConfig"],
                "weights": "lockerWithNoWeights" in location["orderingConfig"],
                "ownedBy": "inventoryOwned" in location,
                "packageConversion": "packageConversion" in location["orderingConfig"]["product"],
                "lifecycleStatus": "lifecycleStatus" in location["orderingConfig"]["product"],
                "customerSku": "customerSku" in location
            }

            for condition in mapping.keys():
                if condition == field:
                    assert mapping[condition], f"{condition} should be TRUE, but it FALSE"
                else:
                    assert not mapping[condition], f"{condition} should be FALSE, but it TRUE"