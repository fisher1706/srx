from src.api.distributor.settings_api import SettingsApi
import pytest
import copy
import time
from src.resources.locator import Locator
from src.resources.tools import Tools
from src.pages.distributor.order_status_page import OrderStatusPage
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.product_api import ProductApi
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.serial_number_api import SerialNumberApi
from src.api.customer.submit_api import SubmitApi

class TestReorderControls():
    @pytest.mark.parametrize("conditions", [
        {
            "coefficient": 0,
            "transaction_qty": 1,
            "reorder_qty_coefficient": 3,
            "testrail_case_id": 2581
        },
        { 
            "coefficient": 1,
            "transaction_qty": 1,
            "reorder_qty_coefficient": 2,
            "testrail_case_id": 2582
        },
        {
            "coefficient": 2,
            "transaction_qty": 0,
            "reorder_qty_coefficient": 0,
            "testrail_case_id": 2583
        }
        ])
    @pytest.mark.regression
    def test_create_transaction_at_min_by_ohi_update(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.add_option("ohi","MAX")
        response_location = setup_location.setup()

        #update OHi
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]*conditions["coefficient"]
        la.update_location([location],response_location["shipto_id"])
    
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert len(transaction) == conditions["transaction_qty"], f"The number of transactions should be equal to {conditions['transaction_qty']}"
        if conditions["transaction_qty"] != 0:
            assert transaction[0]["reorderQuantity"] == (response_location["product"]["roundBuy"]*conditions["reorder_qty_coefficient"]), f"Reorder quantity of transaction should be equal to {response_location['product']['roundBuy']*conditions['reorder_qty_coefficient']}"
            assert transaction[0]["product"]["partSku"] == response_location["product"]["partSku"]

    @pytest.mark.parametrize("conditions_issued", [
        {
            "coefficient": 2,
            "transaction_qty": 0,
            "reorder_qty_coefficient": 0,
            "testrail_case_id": 3198
        },
        {
            "coefficient": 0.5,
            "transaction_qty": 1,
            "reorder_qty_coefficient": 2,
            "testrail_case_id": 3197
        }
        ])
    @pytest.mark.regression
    def test_create_transaction_as_issued_by_ohi_update(self, api, conditions_issued, delete_shipto):
        api.testrail_case_id = conditions_issued["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls": "ISSUED"})
        setup_location.setup_product.add_option("issue_quantity", 1)
        response_location = setup_location.setup()

        #update OHi
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]*conditions_issued["coefficient"]
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert len(transaction) == conditions_issued["transaction_qty"], f"The number of transactions should be equal to {conditions_issued['transaction_qty']}"
        if conditions_issued["transaction_qty"] != 0:
            assert transaction[0]["reorderQuantity"] == (response_location["product"]["roundBuy"]*conditions_issued["reorder_qty_coefficient"]), f"Reorder quantity of transaction should be equal to {response_location['product']['roundBuy']*conditions_issued['reorder_qty_coefficient']}"
            assert transaction[0]["product"]["partSku"] == response_location["product"]["partSku"]
             
    @pytest.mark.parametrize("conditions_close", [
        {
            "close_transaction_cofficient":2, # MAX > OHI > MIN
            "transaction_qty": 1,
            "close_transaction_qty": 0,
            "reorder_controls": "MIN",
            "testrail_case_id": 3199
        },
        {
            "close_transaction_cofficient":4,
            "transaction_qty": 1,
            "close_transaction_qty": 0,
            "reorder_controls": "ISSUED",
            "testrail_case_id": 3200
        }
        ])
    @pytest.mark.regression
    def test_close_transaction_by_ohi_update(self, api, conditions_close, delete_shipto):
        api.testrail_case_id = conditions_close["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_close['reorder_controls']})
        setup_location.add_option("transaction",'ACTIVE')
        response_location = setup_location.setup()

        #close transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]*conditions_close["close_transaction_cofficient"]
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction[0]["status"] == "DO_NOT_REORDER"

    @pytest.mark.regression
    def test_update_reorder_quantity_at_min(self, api, delete_shipto):
        api.testrail_case_id = 3201

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls":'MIN'})
        setup_location.setup_product.add_option("issue_quantity", 1)
        setup_location.add_option("transaction","ACTIVE")
        response_location = setup_location.setup()

        #check quantity
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity_old = transaction[0]["reorderQuantity"]
        #change OHI
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]*0
        la.update_location([location],response_location["shipto_id"])        
        time.sleep(5)
        transaction_updated= ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["reorderQuantity"] == quantity_old + (response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"] - location["onHandInventory"])
       
    @pytest.mark.regression
    def test_update_reorder_quantity_as_issued(self, api, delete_shipto):
        api.testrail_case_id = 3202

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls":'ISSUED'})
        setup_location.add_option("ohi","MAX")
        setup_location.add_option("transaction","ACTIVE")
        setup_location.setup_product.add_option("issue_quantity", 1)
        response_location = setup_location.setup()

        #check quantity
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity_old = transaction[0]["reorderQuantity"]
        #change OHI
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]-1
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction_updated= ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["reorderQuantity"] == quantity_old/2

    @pytest.mark.parametrize("conditions_close_by_pack", [
            {
                "pack_conv": 10,
                "reorder_controls": "MIN",
                "testrail_case_id": 3206
            },
            {
                "pack_conv": 2,
                "reorder_controls": "ISSUED",
                "testrail_case_id": 3207
            }
            ])
    @pytest.mark.regression
    def test_close_transaction_by_pack_conversion_update(self, api, conditions_close_by_pack, delete_customer):
        api.testrail_case_id = conditions_close_by_pack["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)
        pa = ProductApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_close_by_pack['reorder_controls']})
        setup_location.add_option("ohi","MAX")
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_product.add_option("package_conversion", conditions_close_by_pack["pack_conv"])
        setup_location.add_option("transaction",'ACTIVE')
        response_location = setup_location.setup()

        product_dto = copy.deepcopy(response_location["product"])
        product_dto["packageConversion"] = "1"
        pa.update_product(dto = product_dto, product_id  =response_location["product"]["id"])
        time.sleep(5)
        transaction_updated= ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["status"] == "DO_NOT_REORDER"

    @pytest.mark.parametrize("conditions_create_by_pack", [
            {
                "create_pack_conv":10, 
                "reorder_controls": "MIN",
                "testrail_case_id": 3204
            },
            {
                "create_pack_conv":2,
                "reorder_controls": "ISSUED",
                "testrail_case_id": 3205
            }
            ])
    @pytest.mark.regression
    def test_create_transaction_by_pack_conversion_update(self, api, conditions_create_by_pack, delete_customer):
        api.testrail_case_id = conditions_create_by_pack["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)
        pa = ProductApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_create_by_pack['reorder_controls']})
        setup_location.setup_shipto.add_option("customer")
        setup_location.add_option("ohi","MAX")
        setup_location.setup_product.add_option("package_conversion", "1")
        response_location = setup_location.setup()

        product_dto = copy.deepcopy(response_location["product"])
        product_dto["packageConversion"] = conditions_create_by_pack["create_pack_conv"]
        pa.update_product(dto = product_dto, product_id  =response_location["product"]["id"])
        time.sleep(5)
        transaction_updated= ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["status"] == "ACTIVE"

    @pytest.mark.parametrize("conditions_update_by_pack", [
            {
                "update_pack_conv":10, 
                "pack_conv": 2,
                "reorder_controls": "MIN",
                "testrail_case_id": 3208
            },
            {
                "update_pack_conv":4,
                "pack_conv": 1,
                "reorder_controls": "ISSUED",
                "testrail_case_id": 3209
            }
            ])
    @pytest.mark.regression
    def test_update_transaction_quantity_by_pack_conversion_update(self, api, conditions_update_by_pack, delete_customer):
        api.testrail_case_id = conditions_update_by_pack["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)
        pa = ProductApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_update_by_pack['reorder_controls']})
        setup_location.add_option("ohi","MAX")
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_product.add_option("package_conversion", conditions_update_by_pack["pack_conv"])
        setup_location.add_option("transaction",'ACTIVE')
        response_location = setup_location.setup()

        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity_old = transaction[0]["reorderQuantity"]

        product_dto = copy.deepcopy(response_location["product"])
        product_dto["packageConversion"] = conditions_update_by_pack["update_pack_conv"]
        pa.update_product(dto = product_dto, product_id=response_location["product"]["id"])
        time.sleep(5)
        transaction_updated= ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["reorderQuantity"] == quantity_old*1.5
    
    @pytest.mark.parametrize("conditions_create", [
        {
            "reorder_controls": "MIN",
            "testrail_case_id": 3494
        },
        {
            "reorder_controls": "ISSUED",
            "testrail_case_id": 3495
        }
        ])
    @pytest.mark.regression
    def test_create_transaction_by_min_max_update(self, api, conditions_create, delete_shipto):
        api.testrail_case_id = conditions_create["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_create['reorder_controls']})
        setup_location.add_option("ohi","MAX")
        response_location = setup_location.setup()

        #create transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["orderingConfig"]["currentInventoryControls"]["min"] *= 4
        location["orderingConfig"]["currentInventoryControls"]["max"] *= 4
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction[0]["status"] == "ACTIVE"

    @pytest.mark.parametrize("conditions_close", [
        {
            "reorder_controls": "MIN",
            "close_coeff_min": 0,
            "close_coeff_max": 1,
            "testrail_case_id": 3496
        }, 
        {
            "reorder_controls": "ISSUED",
            "close_coeff_min": 1,
            "close_coeff_max": 1.5,
            "testrail_case_id": 3497
        }
        ])
    @pytest.mark.regression
    def test_close_transaction_by_min_max_update(self, api, conditions_close, delete_shipto):
        api.testrail_case_id = conditions_close["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_close['reorder_controls']})
        setup_location.add_option("ohi","MAX")
        setup_location.add_option("transaction","ACTIVE")
        response_location = setup_location.setup()

        #close transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["orderingConfig"]["currentInventoryControls"]["min"] *=conditions_close["close_coeff_min"]
        location["orderingConfig"]["currentInventoryControls"]["max"] /=conditions_close["close_coeff_max"]
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction[0]["status"] == "DO_NOT_REORDER"
 
    @pytest.mark.parametrize("conditions_update", [
        {
            "reorder_controls": "MIN",
            "testrail_case_id": 3499
        }, 
        {
            "reorder_controls": "ISSUED",
            "testrail_case_id": 3498
        }
        ])
    @pytest.mark.regression
    def test_update_transaction_by_min_max_update(self, api, conditions_update, delete_shipto):
        api.testrail_case_id = conditions_update["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_update['reorder_controls']})
        setup_location.add_option("ohi","0")
        setup_location.add_option("transaction","ACTIVE")
        response_location = setup_location.setup()

        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity_old = transaction[0]["reorderQuantity"]

        #update transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["orderingConfig"]["currentInventoryControls"]["min"] +=1
        location["orderingConfig"]["currentInventoryControls"]["max"] +=1
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity = transaction_updated[0]["reorderQuantity"]
        assert transaction_updated[0]["reorderQuantity"] == quantity_old*2

    @pytest.mark.parametrize("conditions_rfid_create", [
        {
            "reorder_controls": "MIN",
            "created_coeff": 300,
            "testrail_case_id": 3642
        }, 
        {
            "reorder_controls": "ISSUED",
            "created_coeff": 50,
            "testrail_case_id": 3643
        }
        ])
    @pytest.mark.regression
    def test_create_transaction_rfid_by_updated_issue_qnt(self, api, conditions_rfid_create, delete_shipto):
        api.testrail_case_id = conditions_rfid_create["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        ra = RfidApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("type", "RFID")
        setup_location.add_option("rfid_labels", 1)
        setup_location.setup_shipto.add_option("customer.clc", False)
        setup_location.setup_product.add_option("issue_quantity", 300)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_rfid_create["reorder_controls"]})
        response_location = setup_location.setup()

        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][0]["rfid_id"], "AVAILABLE")

        product_dto = copy.deepcopy(response_location["product"])
        product_dto["issueQuantity"] /= conditions_rfid_create["created_coeff"]
        pa.update_product(dto=product_dto, product_id=response_location["product"]["id"])
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["status"] == "ACTIVE"

    @pytest.mark.parametrize("conditions_rfid_update", [
        {
            "reorder_controls": "MIN",
            "testrail_case_id": 3644
        }, 
        {
            "reorder_controls": "ISSUED",
            "testrail_case_id": 3645
        }
        ])
    @pytest.mark.regression
    def test_update_transaction_rfid_by_updated_issue_qnt(self, api, conditions_rfid_update, delete_shipto):
        api.testrail_case_id = conditions_rfid_update["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        ra = RfidApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("type", 'RFID')
        setup_location.add_option("rfid_labels", 1)
        setup_location.setup_shipto.add_option("customer.clc", False)
        setup_location.setup_product.add_option("issue_quantity", 1)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_rfid_update["reorder_controls"]})
        response_location = setup_location.setup()

        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][0]["rfid_id"], "AVAILABLE")
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity_old = transaction[0]["reorderQuantity"]

        product_dto = copy.deepcopy(response_location["product"])
        product_dto["issueQuantity"] *=  product_dto["roundBuy"]
        pa.update_product(dto = product_dto, product_id  =response_location["product"]["id"])
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity = transaction_updated[0]["reorderQuantity"]
        assert quantity_old-quantity == response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]

    @pytest.mark.parametrize("conditions_rfid_close", [
        {
            "reorder_controls": "MIN",
            "testrail_case_id": 3646
        }, 
        {
            "reorder_controls": "ISSUED",
            "testrail_case_id": 3647
        }
        ])
    @pytest.mark.regression
    def test_close_transaction_rfid_by_updated_issue_qnt(self, api, conditions_rfid_close, delete_shipto):
        api.testrail_case_id = conditions_rfid_close["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        ra = RfidApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("type", "RFID")
        setup_location.add_option("rfid_labels", 1)
        setup_location.setup_shipto.add_option("customer.clc", False)
        setup_location.setup_product.add_option("issue_quantity",1)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_rfid_close["reorder_controls"]})
        response_location = setup_location.setup()

        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][0]["rfid_id"], "AVAILABLE")

        product_dto = copy.deepcopy(response_location["product"])
        product_dto["issueQuantity"] *= response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]
        pa.update_product(dto = product_dto, product_id  =response_location["product"]["id"])
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity = transaction_updated[0]["reorderQuantity"]
        assert transaction_updated[0]["status"] == "DO_NOT_REORDER"

    @pytest.mark.regression
    def test_create_transaction_by_sn_status_update_at_min(self, api, delete_shipto):
        api.testrail_case_id = 3794

        ta = TransactionApi(api)
        la = LocationApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :"MIN"})
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", 1)
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        la = LocationApi(api)
        sn = Tools.random_string_u()
        sn1 = Tools.random_string_u()
        sn2 = Tools.random_string_u()

        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn1)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn2)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)
        sn_dto1 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[1]
        sn_dto1["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto1)
        sn_dto2 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[2]
        sn_dto2["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto2) 

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto["status"] = "ASSIGNED"
        sna.update_serial_number(sn_dto)
        sn_dto1 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto1["status"] = "ASSIGNED"
        sna.update_serial_number(sn_dto1)
        sn_dto2 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[2]
        sn_dto2["status"] = "ASSIGNED"
        sna.update_serial_number(sn_dto2)
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"][-1]
        assert transaction["status"] == "ACTIVE"

    @pytest.mark.regression
    def test_create_transaction_by_sn_status_update_as_issued(self, api, delete_shipto):
        api.testrail_case_id = 3795

        ta = TransactionApi(api)
        la = LocationApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :"ISSUED"})
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", 1)
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        la = LocationApi(api)
        sn = Tools.random_string_u()
        sn1 = Tools.random_string_u()
        sn2 = Tools.random_string_u()

        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn1)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn2)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)
        sn_dto1 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[1]
        sn_dto1["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto1)
        sn_dto2 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[2]
        sn_dto2["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto2) 

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto["status"] = "ASSIGNED"
        sna.update_serial_number(sn_dto)
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"][-1]
        assert transaction["status"] == "ACTIVE"

    @pytest.mark.regression
    def test_close_transaction_by_sn_status_update_at_min(self, api, delete_shipto):
        api.testrail_case_id = 3796

        ta = TransactionApi(api)
        la = LocationApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :"MIN"})
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", 1)
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        la = LocationApi(api)
        sn = Tools.random_string_u()
        sn1 = Tools.random_string_u()
        sn2 = Tools.random_string_u()

        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn1)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn2)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)
        sn_dto1 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[1]
        sn_dto1["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto1)
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"][-1]
        assert transaction["status"] == "DO_NOT_REORDER"

    @pytest.mark.regression
    def test_close_transaction_by_sn_status_update_as_issued(self, api, delete_shipto):
        api.testrail_case_id = 3797

        ta = TransactionApi(api)
        la = LocationApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :"ISSUED"})
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("round_buy", 1)
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        la = LocationApi(api)
        sn = Tools.random_string_u()
        sn1 = Tools.random_string_u()
        sn2 = Tools.random_string_u()

        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn1)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn2)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)
        sn_dto1 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[1]
        sn_dto1["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto1)
        sn_dto2 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[2]
        sn_dto2["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto2) 
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"][-1]
        assert transaction["status"] == "DO_NOT_REORDER"

    @pytest.mark.parametrize("conditions_sn_updated", [
        {
            "reorder_controls": "MIN",
            "coef":0,
            "testrail_case_id": 3798
        }, 
        {
            "reorder_controls": "ISSUED",
            "coef":0.5,
            "testrail_case_id": 3799
        }
        ])
    @pytest.mark.regression
    def test_update_transaction_by_sn_status_update_as_issued(self, conditions_sn_updated, api, delete_shipto):
        api.testrail_case_id = conditions_sn_updated["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_sn_updated["reorder_controls"]})
        setup_location.add_option("serialized")
        setup_location.setup_product.add_option("round_buy",1)
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        la = LocationApi(api)
        sn = Tools.random_string_u()
        sn1 = Tools.random_string_u()
        sn2 = Tools.random_string_u()

        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn1)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn2)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        sn_dto["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto)
        time.sleep(5)
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"][-1]
        quantity = transaction["reorderQuantity"]
        
        sn_dto1 = sna.get_serial_number(shipto_id=response_location["shipto_id"])[1]
        sn_dto1["status"] = "AVAILABLE"
        sna.update_serial_number(sn_dto1)
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"][-1]
        quantity_updated = transaction_updated["reorderQuantity"]
        assert quantity_updated == quantity*conditions_sn_updated["coef"]

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "ohi": 0,
            "SHIPPED": 1,
            "ORDERED": 0,
            "QUOTED": 0,
            "result": 9,
            "testrail_case_id": 5156
        },
        {
            "reorder_controls": "MIN",
            "ohi": 0,
            "SHIPPED": 0,
            "ORDERED": 1,
            "QUOTED": 0,
            "result": 9,
            "testrail_case_id": 5157
        },
        {
            "reorder_controls": "MIN",
            "ohi": 0,
            "SHIPPED": 0,
            "ORDERED": 0,
            "QUOTED": 1,
            "result": 9,
            "testrail_case_id": 5158
        },
        {
            "reorder_controls": "MIN",
            "ohi": 0,
            "SHIPPED": 1,
            "ORDERED": 1,
            "QUOTED": 1,
            "result": 7,
            "testrail_case_id": 5159
        },
        {
            "reorder_controls": "MIN",
            "ohi": 3,
            "SHIPPED": 1,
            "ORDERED": 1,
            "QUOTED": 1,
            "result": 6,
            "testrail_case_id": 5160
        },
        {
            "reorder_controls": "MIN",
            "ohi": 6,
            "SHIPPED": 1,
            "ORDERED": 1,
            "QUOTED": 1,
            "result": None,
            "testrail_case_id": 5161
        },
        {
            "reorder_controls": "MIN",
            "ohi": 12,
            "SHIPPED": 1,
            "ORDERED": 0,
            "QUOTED": 0,
            "result": None,
            "testrail_case_id": 5162
        },
        {
            "reorder_controls": "MIN",
            "ohi": 9,
            "SHIPPED": 2,
            "ORDERED": 0,
            "QUOTED": 0,
            "result": None,
            "testrail_case_id": 5163
        },
        {
            "reorder_controls": "MIN",
            "ohi": 0,
            "SHIPPED": 0,
            "ORDERED": 3,
            "QUOTED": 2,
            "result": None,
            "testrail_case_id": 5164
        },
        {
            "reorder_controls": "ISSUED",
            "ohi": 0,
            "SHIPPED": 1,
            "ORDERED": 2,
            "QUOTED": 2,
            "result": 5,
            "testrail_case_id": 5165
        },
        {
            "reorder_controls": "ISSUED",
            "ohi": 11,
            "SHIPPED": 6,
            "ORDERED": 0,
            "QUOTED": 0,
            "result": 1,
            "testrail_case_id": 5166
        },
        {
            "reorder_controls": "ISSUED",
            "ohi": 12,
            "SHIPPED": 6,
            "ORDERED": 0,
            "QUOTED": 0,
            "result": None,
            "testrail_case_id": 5167
        },
        {
            "reorder_controls": "ISSUED",
            "ohi": 0,
            "SHIPPED": 9,
            "ORDERED": 0,
            "QUOTED": 0,
            "result": 1,
            "testrail_case_id": 5168
        },
        {
            "reorder_controls": "ISSUED",
            "ohi": 0,
            "SHIPPED": 10,
            "ORDERED": 0,
            "QUOTED": 0,
            "result": None,
            "testrail_case_id": 5169
        },
        ])
    @pytest.mark.regression
    def test_reorder_controls_with_quantity_on_reorder(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create transactions for quantity on reorder
        ordering_config_id = la.get_ordering_config_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])
        statuses = ["SHIPPED", "ORDERED", "QUOTED"]
        for status in statuses:
            if (conditions[status] > 0):
                ta.create_active_item(response_location["shipto_id"], ordering_config_id, repeat=15)
                transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
                transaction_id = transaction["entities"][-1]["id"]
                ta.update_replenishment_item(transaction_id, conditions[status], status)

        #update location ohi
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = conditions["ohi"]
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)

        #check new ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        if conditions["result"] is not None:
            assert transaction["entities"][0]["reorderQuantity"] == conditions["result"]
        else:
            assert transaction["entities"] == []

    @pytest.mark.regression
    def test_reorder_controls_with_quantity_on_reorder_with_several_same_statuses(self, api, delete_shipto):
        api.testrail_case_id = 5172

        ta = TransactionApi(api)
        la = LocationApi(api)
        sa = SettingsApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create transactions for quantity on reorder
        ordering_config_id = la.get_ordering_config_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])
        for i in range (2):
            ta.create_active_item(response_location["shipto_id"], ordering_config_id, repeat=15)
            transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
            transaction_id = transaction["entities"][-1]["id"]
            ta.update_replenishment_item(transaction_id, 1, "QUOTED")

        sa.set_reorder_controls_settings_for_shipto(response_location["shipto_id"], reorder_controls="MIN", track_ohi=True, enable_reorder_control=True)
        #update location ohi
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = 0
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)

        #check new ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"][0]["reorderQuantity"] == 8

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "SHIPPED": 3,
            "result": None,
            "testrail_case_id": 5594
        },
        {
            "reorder_controls": "MIN",
            "SHIPPED": 2,
            "result": 6,
            "testrail_case_id": 5595
        },
        {
            "reorder_controls": "MIN",
            "SHIPPED": 1,
            "result": 7,
            "testrail_case_id": 5603
        },
        {
            "reorder_controls": "ISSUED",
            "SHIPPED": 8,
            "result": None,
            "testrail_case_id": 5596
        },
        {
            "reorder_controls": "ISSUED",
            "SHIPPED": 7,
            "result": 1,
            "testrail_case_id": 5597
        },
        ])
    @pytest.mark.regression
    def test_reorder_controls_update_quantity_on_reorder_qnty_with_existing_active_for_update(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create transaction for quantity on reorder
        ordering_config_id = la.get_ordering_config_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])
        ta.create_active_item(response_location["shipto_id"], ordering_config_id, repeat=15)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        ta.update_replenishment_item(transaction_id, 1, "SHIPPED")

        #update location ohi
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = 6
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)

        #check new ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"][0]["reorderQuantity"] == 7

        #update quantityOnReorder
        ta.update_replenishment_item(transaction_id, conditions["SHIPPED"], "SHIPPED")

        #check new ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        if conditions["result"] is not None:
            assert transaction["entities"][0]["reorderQuantity"] == conditions["result"]
        else:
            assert transaction["entities"] == []

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "testrail_case_id": 5604
        },
        {
            "reorder_controls": "ISSUED",
            "testrail_case_id": 5605
        }
        ])
    @pytest.mark.regression
    def test_reorder_controls_update_quantity_on_reorder_status_with_existing_active_for_create(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        if conditions["reorder_controls"] == "MIN":
            start_ohi = LOCATION_MIN * LOCATION_PACKAGE_CONVERSION + LOCATION_PACKAGE_CONVERSION
        elif conditions["reorder_controls"] == "ISSUED":
            start_ohi = LOCATION_MAX * LOCATION_PACKAGE_CONVERSION
        else:
            api.logger.error("Incorrect 'reorder_controls' value")
        setup_location.add_option("ohi", start_ohi)
        response_location = setup_location.setup()

        #create transaction for quantity on reorder
        ordering_config_id = la.get_ordering_config_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])
        ta.create_active_item(response_location["shipto_id"], ordering_config_id, repeat=15)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        ta.update_replenishment_item(transaction_id, start_ohi / LOCATION_PACKAGE_CONVERSION, "SHIPPED")

        #update location ohi
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = start_ohi - LOCATION_PACKAGE_CONVERSION
        la.update_location([location],response_location["shipto_id"])

        #update status of qntyOnReorder transaction
        ta.update_replenishment_item(transaction_id, transaction["entities"][-1]["reorderQuantity"], "DO_NOT_REORDER")
        time.sleep(5)

        #check new ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"][0]["reorderQuantity"] == LOCATION_MAX - (start_ohi - LOCATION_PACKAGE_CONVERSION)/LOCATION_PACKAGE_CONVERSION

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "case": 1,
            "testrail_case_id": 5606
        },
        {
            "reorder_controls": "MIN",
            "case": 2,
            "testrail_case_id": 5607
        },
        {
            "reorder_controls": "ISSUED",
            "case": 3,
            "testrail_case_id": 5608
        }
        ])
    @pytest.mark.regression
    def test_reorder_controls_update_quantity_on_reorder_qnty_with_existing_active_for_create(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1

        if conditions["case"] == 1:
            new_reorder_quantity = LOCATION_MIN
            result = LOCATION_MAX - new_reorder_quantity
        elif conditions["case"] == 2:
            new_reorder_quantity = LOCATION_MIN + 1
            result = None
        elif conditions["case"] == 3:
            new_reorder_quantity = LOCATION_MAX - 1
            result = 1
        else:
            api.logger.error("Incorrect 'case' value")
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create transaction for quantity on reorder
        ordering_config_id = la.get_ordering_config_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])
        ta.create_active_item(response_location["shipto_id"], ordering_config_id, repeat=15)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        ta.update_replenishment_item(transaction_id, LOCATION_MAX, "SHIPPED")

        #update location ohi
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = 0
        la.update_location([location],response_location["shipto_id"])

        #there is no ACTIVE transactions
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"] == []

        #update qntyOfReorder qnty
        ta.update_replenishment_item(transaction_id, new_reorder_quantity, "SHIPPED")
        time.sleep(5)

        #check new ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        if result is not None:
            assert transaction["entities"][0]["reorderQuantity"] == result
        else:
            assert transaction["entities"] == []

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "updated_quantity": 9,
            "updated_status": "ACTIVE",
            "start_result_quantity": 10,
            "start_result_status": "ACTIVE",
            "new_result_quantity": None,
            "new_result_status": None,
            "testrail_case_id": 5609
        },
        {
            "reorder_controls": "MIN",
            "updated_quantity": 10,
            "updated_status": "DO_NOT_REORDER",
            "start_result_quantity": 10,
            "start_result_status": "DO_NOT_REORDER",
            "new_result_quantity": 10,
            "new_result_status": "ACTIVE",
            "testrail_case_id": 5610
        },
        {
            "reorder_controls": "MIN",
            "updated_quantity": 4,
            "updated_status": "SHIPPED",
            "start_result_quantity": 4,
            "start_result_status": "SHIPPED",
            "new_result_quantity": 6,
            "new_result_status": "ACTIVE",
            "testrail_case_id": 5611
        },        
        {
            "reorder_controls": "MIN",
            "updated_quantity": 4,
            "updated_status": "DELIVERED",
            "start_result_quantity": 4,
            "start_result_status": "DELIVERED",
            "new_result_quantity": 6,
            "new_result_status": "ACTIVE",
            "testrail_case_id": 5612
        },
        {
            "reorder_controls": "MIN",
            "updated_quantity": 5,
            "updated_status": "DELIVERED",
            "start_result_quantity": 5,
            "start_result_status": "DELIVERED",
            "new_result_quantity": None,
            "new_result_status": None,
            "testrail_case_id": 5613
        },
        {
            "reorder_controls": "MIN",
            "updated_quantity": 5,
            "updated_status": "SHIPPED",
            "start_result_quantity": 5,
            "start_result_status": "SHIPPED",
            "new_result_quantity": None,
            "new_result_status": None,
            "testrail_case_id": 5614
        },
        {
            "reorder_controls": "ISSUED",
            "updated_quantity": 9,
            "updated_status": "SHIPPED",
            "start_result_quantity": 9,
            "start_result_status": "SHIPPED",
            "new_result_quantity": 1,
            "new_result_status": "ACTIVE",
            "testrail_case_id": 5615
        },
        {
            "reorder_controls": "ISSUED",
            "updated_quantity": 10,
            "updated_status": "SHIPPED",
            "start_result_quantity": 10,
            "start_result_status": "SHIPPED",
            "new_result_quantity": None,
            "new_result_status": None,
            "testrail_case_id": 5616
        },
        ])
    @pytest.mark.regression
    def test_reorder_controls_update_active_transaction(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create ACTIVE transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = 0
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        assert transaction["entities"][-1]["reorderQuantity"] == LOCATION_MAX

        #update ACTIVE transaction
        ta.update_replenishment_item(transaction_id, conditions["updated_quantity"], conditions["updated_status"])
        time.sleep(5)

        #check start transaction result
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status=conditions["start_result_status"])
        assert transaction["entities"][-1]["reorderQuantity"] == conditions["start_result_quantity"]
        assert transaction["entities"][-1]["id"] == transaction_id

        #check new transaction result
        if conditions["new_result_status"] is not None:
            transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status=conditions["new_result_status"])
            assert transaction["entities"][0]["reorderQuantity"] == conditions["new_result_quantity"]
            assert transaction["entities"][-1]["id"] != transaction_id
            transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
            assert transaction["totalElements"] == 2
        else:
            transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
            assert transaction["totalElements"] == 1

    @pytest.mark.regression
    def test_reorder_controls_is_not_triggered_by_update_transaction_from_customer_portal(self, api, delete_shipto):
        api.testrail_case_id = 5617

        ta = TransactionApi(api)
        la = LocationApi(api)
        sa = SubmitApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :"ISSUED"})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create ACTIVE transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = 0
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        assert transaction["entities"][-1]["reorderQuantity"] == LOCATION_MAX

        #update transaction from customer portal
        sa.update_replenishment_item(response_location["shipto_id"], transaction_id, LOCATION_MAX-1)

        #check new transaction's quantity
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"][-1]["reorderQuantity"] == LOCATION_MAX-1

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "submitted_quantity": 0,
            "start_result_quantity": 0,
            "start_result_status": "DO_NOT_REORDER",
            "new_result_quantity": 10,
            "testrail_case_id": 5618
        },
        {
            "reorder_controls": "MIN",
            "submitted_quantity": 4,
            "start_result_quantity": 4,
            "start_result_status": "QUOTED",
            "new_result_quantity": 6,
            "testrail_case_id": 5619
        },
        {
            "reorder_controls": "MIN",
            "submitted_quantity": 5,
            "start_result_quantity": 5,
            "start_result_status": "QUOTED",
            "new_result_quantity": None,
            "testrail_case_id": 5620
        },        
        {
            "reorder_controls": "ISSUED",
            "submitted_quantity": 9,
            "start_result_quantity": 9,
            "start_result_status": "QUOTED",
            "new_result_quantity": 1,
            "testrail_case_id": 5621
        },
        {
            "reorder_controls": "ISSUED",
            "submitted_quantity": 10,
            "start_result_quantity": 10,
            "start_result_status": "QUOTED",
            "new_result_quantity": None,
            "testrail_case_id": 5622
        }
        ])
    @pytest.mark.regression
    def test_reorder_controls_submit_replenishment_list_for_create(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)
        sa = SubmitApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create ACTIVE transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = 0
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        assert transaction["entities"][-1]["reorderQuantity"] == LOCATION_MAX

        #submit ACTIVE transaction
        items = [{
            "id": transaction_id,
            "reorderQuantity": conditions["submitted_quantity"],
            "status": "QUOTED"
        }]
        sa.submit_replenishment_list(items)
        time.sleep(5)

        #check start transaction result
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status=conditions["start_result_status"])
        assert transaction["entities"][-1]["reorderQuantity"] == conditions["start_result_quantity"]
        assert transaction["entities"][-1]["id"] == transaction_id

        #check new transaction result
        if conditions["new_result_quantity"] is not None:
            transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
            assert transaction["entities"][0]["reorderQuantity"] == conditions["new_result_quantity"]
            assert transaction["entities"][-1]["id"] != transaction_id
            transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
            assert transaction["totalElements"] == 2
        else:
            transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
            assert transaction["totalElements"] == 1

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "new_status": "DELIVERED",
            "new_active_quantity": 9,
            "testrail_case_id": 5623
        },
        {
            "reorder_controls": "MIN",
            "new_status": "DO_NOT_REORDER",
            "new_active_quantity": 10,
            "testrail_case_id": 5624
        },       
        {
            "reorder_controls": "ISSUED",
            "new_status": "DELIVERED",
            "new_active_quantity": 9,
            "testrail_case_id": 5625
        },
        {
            "reorder_controls": "ISSUED",
            "new_status": "DO_NOT_REORDER",
            "new_active_quantity": 10,
            "testrail_case_id": 5626
        }
        ])
    @pytest.mark.regression
    def test_reorder_controls_update_quantity_on_reorder_status_with_existing_active_for_update(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create ACTIVE transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = 0
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        assert transaction["entities"][-1]["reorderQuantity"] == LOCATION_MAX

        #update ACTIVE -> qntyOnReorder
        ta.update_replenishment_item(transaction_id, 1, "ORDERED")
        time.sleep(5)

        #check new ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"][-1]["reorderQuantity"] == LOCATION_MAX-1
        assert transaction["entities"][-1]["id"] != transaction_id

        #update qntyOnReorder transaction
        ta.update_replenishment_item(transaction_id, 1, conditions["new_status"])

        #check ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"][-1]["reorderQuantity"] == conditions["new_active_quantity"]
        assert transaction["entities"][-1]["id"] != transaction_id

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "start_qnty_on_reorder": 5,
            "new_min": 5,
            "new_max": 10,
            "new_active_quantity": 5,
            "testrail_case_id": 5627
        },
        {
            "reorder_controls": "ISSUED",
            "start_qnty_on_reorder": 10,
            "new_min": 4,
            "new_max": 11,
            "new_active_quantity": 1,
            "testrail_case_id": 5628
        }
        ])
    @pytest.mark.regression
    def test_reorder_controls_with_quantity_on_reorder_update_min_and_max_for_create(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create ACTIVE transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = 0
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        assert transaction["entities"][-1]["reorderQuantity"] == LOCATION_MAX

        #update ACTIVE -> qntyOnReorder
        ta.update_replenishment_item(transaction_id, conditions["start_qnty_on_reorder"], "ORDERED")

        #check there is no ACTIVE
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"] == []

        #update MIN/MAX
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["orderingConfig"]["currentInventoryControls"]["min"] = conditions["new_min"]
        location["orderingConfig"]["currentInventoryControls"]["max"] = conditions["new_max"]
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)

        #check new ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"][-1]["reorderQuantity"] == conditions["new_active_quantity"]

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "start_qnty_on_reorder": 3,
            "new_min": 4,
            "new_max": 11,
            "new_active_quantity": 8,
            "testrail_case_id": 5629
        },
        {
            "reorder_controls": "MIN",
            "start_qnty_on_reorder": 4,
            "new_min": 3,
            "new_max": 10,
            "new_active_quantity": None,
            "testrail_case_id": 5630
        },
        {
            "reorder_controls": "MIN",
            "start_qnty_on_reorder": 3,
            "new_min": 3,
            "new_max": 10,
            "new_active_quantity": 7,
            "testrail_case_id": 5633
        },
        {
            "reorder_controls": "ISSUED",
            "start_qnty_on_reorder": 9,
            "new_min": 4,
            "new_max": 11,
            "new_active_quantity": 2,
            "testrail_case_id": 5631
        },
        {
            "reorder_controls": "ISSUED",
            "start_qnty_on_reorder": 9,
            "new_min": 4,
            "new_max": 9,
            "new_active_quantity": None,
            "testrail_case_id": 5632
        }
        ])
    @pytest.mark.regression
    def test_reorder_controls_with_quantity_on_reorder_update_min_and_max_for_update(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        LOCATION_MIN = 4
        LOCATION_MAX = 10
        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 1
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.add_option("min", LOCATION_MIN)
        setup_location.add_option("max", LOCATION_MAX)
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create ACTIVE transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = 0
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        assert transaction["entities"][-1]["reorderQuantity"] == LOCATION_MAX

        #update ACTIVE -> qntyOnReorder
        ta.update_replenishment_item(transaction_id, conditions["start_qnty_on_reorder"], "ORDERED")

        #check ACTIVE
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        assert transaction["entities"][-1]["reorderQuantity"] == LOCATION_MAX - conditions["start_qnty_on_reorder"]

        #update MIN/MAX
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["orderingConfig"]["currentInventoryControls"]["min"] = conditions["new_min"]
        location["orderingConfig"]["currentInventoryControls"]["max"] = conditions["new_max"]
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)

        #check new ACTIVE transaction
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        if conditions["new_active_quantity"] is not None:
            assert transaction["entities"][0]["reorderQuantity"] == conditions["new_active_quantity"]
        else:
            assert transaction["entities"] == []

    @pytest.mark.parametrize("conditions", [
        {
            "reorder_controls": "MIN",
            "min": 3,
            "max": 12,
            "ohi": 1,
            "qnty_on_reorder": 0,
            "active": 12,
            "testrail_case_id": 5634
        },
        {
            "reorder_controls": "MIN",
            "min": 3,
            "max": 12,
            "ohi": 8,
            "qnty_on_reorder": 0,
            "active": 12,
            "testrail_case_id": 5635
        },
        {
            "reorder_controls": "MIN",
            "min": 3,
            "max": 12,
            "ohi": 9,
            "qnty_on_reorder": 0,
            "active": 9,
            "testrail_case_id": 5636
        },
        {
            "reorder_controls": "MIN",
            "min": 4,
            "max": 10,
            "ohi": 9,
            "qnty_on_reorder": 0,
            "active": 9,
            "testrail_case_id": 5637
        },
        {
            "reorder_controls": "MIN",
            "min": 4,
            "max": 10,
            "ohi": 2,
            "qnty_on_reorder": 3,
            "active": 9,
            "testrail_case_id": 5638
        },
        {
            "reorder_controls": "ISSUED",
            "min": 4,
            "max": 10,
            "ohi": 29,
            "qnty_on_reorder": 0,
            "active": 3,
            "testrail_case_id": 5639
        },
        {
            "reorder_controls": "ISSUED",
            "min": 4,
            "max": 10,
            "ohi": 20,
            "qnty_on_reorder": 3,
            "active": 3,
            "testrail_case_id": 5640
        },
        {
            "reorder_controls": "ISSUED",
            "min": 3,
            "max": 12,
            "ohi": 20,
            "qnty_on_reorder": 3,
            "active": 3,
            "testrail_case_id": 5641
        },
        ])
    @pytest.mark.regression
    def test_reorder_controls_rounding(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        ta = TransactionApi(api)
        la = LocationApi(api)

        LOCATION_PACKAGE_CONVERSION = 3
        ROUND_BUY = 3
        
        #setup
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True, "enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions["reorder_controls"]})
        setup_location.setup_product.add_option("round_buy", ROUND_BUY)
        setup_location.setup_product.add_option("package_conversion", LOCATION_PACKAGE_CONVERSION)
        setup_location.setup_product.add_option("issue_quantity", 1)
        setup_location.add_option("min", conditions["min"])
        setup_location.add_option("max", conditions["max"])
        setup_location.add_option("ohi", "MAX")
        response_location = setup_location.setup()

        #create ACTIVE transaction
        location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
        location["onHandInventory"] = conditions["ohi"]
        la.update_location([location],response_location["shipto_id"])
        time.sleep(5)
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
        transaction_id = transaction["entities"][-1]["id"]
        assert transaction["entities"][-1]["reorderQuantity"] == conditions["qnty_on_reorder"] + conditions["active"]

        #update ACTIVE -> qntyOnReorder
        if conditions["qnty_on_reorder"] > 0:
            ta.update_replenishment_item(transaction_id, conditions["qnty_on_reorder"], "SHIPPED")
            transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"], status="ACTIVE")
            assert transaction["entities"][-1]["reorderQuantity"] == conditions["active"]

    @pytest.mark.parametrize("conditions_create_by_pack", [
            {
                "create_pack_conv":10, 
                "reorder_controls": "MIN",
                "testrail_case_id": 7504
            },
            {
                "create_pack_conv":2,
                "reorder_controls": "ISSUED",
                "testrail_case_id": 7505
            }
            ])
    @pytest.mark.regression
    def test_create_transaction_by_pack_conversion_update_with_clc(self, api, conditions_create_by_pack, delete_customer):
        api.testrail_case_id = conditions_create_by_pack["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_create_by_pack['reorder_controls']})
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_shipto.setup_customer.add_option("clc")
        setup_location.add_option("ohi","MAX")
        setup_location.setup_product.add_option("package_conversion", "1")
        response_location = setup_location.setup()

        product_dto = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = product_dto.pop("id")
        product_dto["packageConversion"] = conditions_create_by_pack["create_pack_conv"]
        pa.update_customer_product(dto=product_dto, product_id=product_id, customer_id=response_location["customer_id"])
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["status"] == "ACTIVE"

    @pytest.mark.parametrize("conditions_close_by_pack", [
            {
                "pack_conv": 10,
                "reorder_controls": "MIN",
                "testrail_case_id": 7506
            },
            {
                "pack_conv": 2,
                "reorder_controls": "ISSUED",
                "testrail_case_id": 7507
            }
            ])
    @pytest.mark.regression
    def test_close_transaction_by_pack_conversion_update_with_clc(self, api, conditions_close_by_pack, delete_customer):
        api.testrail_case_id = conditions_close_by_pack["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_close_by_pack['reorder_controls']})
        setup_location.add_option("ohi","MAX")
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_shipto.setup_customer.add_option("clc")
        setup_location.setup_product.add_option("package_conversion", conditions_close_by_pack["pack_conv"])
        setup_location.add_option("transaction",'ACTIVE')
        response_location = setup_location.setup()

        product_dto = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = product_dto.pop("id")
        product_dto["packageConversion"] = "1"
        pa.update_customer_product(dto=product_dto, product_id=product_id, customer_id=response_location["customer_id"])
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["status"] == "DO_NOT_REORDER"

    @pytest.mark.parametrize("conditions_update_by_pack", [
            {
                "update_pack_conv":10, 
                "pack_conv": 2,
                "reorder_controls": "MIN",
                "testrail_case_id": 7508
            },
            {
                "update_pack_conv":4,
                "pack_conv": 1,
                "reorder_controls": "ISSUED",
                "testrail_case_id": 7509
            }
            ])
    @pytest.mark.regression
    def test_update_transaction_quantity_by_pack_conversion_update_with_clc(self, api, conditions_update_by_pack, delete_customer):
        api.testrail_case_id = conditions_update_by_pack["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_update_by_pack['reorder_controls']})
        setup_location.add_option("ohi","MAX")
        setup_location.setup_shipto.add_option("customer")
        setup_location.setup_shipto.setup_customer.add_option("clc")
        setup_location.setup_product.add_option("package_conversion", conditions_update_by_pack["pack_conv"])
        setup_location.add_option("transaction",'ACTIVE')
        response_location = setup_location.setup()

        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity_old = transaction[0]["reorderQuantity"]

        product_dto = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = product_dto.pop("id")
        product_dto["packageConversion"] = conditions_update_by_pack["update_pack_conv"]
        pa.update_customer_product(dto=product_dto, product_id=product_id, customer_id=response_location["customer_id"])
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["reorderQuantity"] == quantity_old*1.5

    @pytest.mark.parametrize("conditions_rfid_create", [
        {
            "reorder_controls": "MIN",
            "created_coeff": 300,
            "testrail_case_id": 7510
        }, 
        {
            "reorder_controls": "ISSUED",
            "created_coeff": 50,
            "testrail_case_id": 7511
        }
        ])
    @pytest.mark.regression
    def test_create_transaction_rfid_by_updated_issue_qnt_with_clc(self, api, conditions_rfid_create, delete_shipto):
        api.testrail_case_id = conditions_rfid_create["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        ra = RfidApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("type", "RFID")
        setup_location.add_option("rfid_labels", 1)
        setup_location.setup_shipto.add_option("customer.clc")
        setup_location.setup_product.add_option("issue_quantity", 300)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_rfid_create["reorder_controls"]})
        response_location = setup_location.setup()

        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][0]["rfid_id"], "AVAILABLE")

        product_dto = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = product_dto.pop("id")
        product_dto["issueQuantity"] /= conditions_rfid_create["created_coeff"]
        pa.update_customer_product(dto=product_dto, product_id=product_id)
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction_updated[0]["status"] == "ACTIVE"

    @pytest.mark.parametrize("conditions_rfid_update", [
        {
            "reorder_controls": "MIN",
            "testrail_case_id": 7512
        }, 
        {
            "reorder_controls": "ISSUED",
            "testrail_case_id": 7513
        }
        ])
    @pytest.mark.regression
    def test_update_transaction_rfid_by_updated_issue_qnt_with_clc(self, api, conditions_rfid_update, delete_shipto):
        api.testrail_case_id = conditions_rfid_update["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        ra = RfidApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("type", 'RFID')
        setup_location.add_option("rfid_labels", 1)
        setup_location.setup_shipto.add_option("customer.clc")
        setup_location.setup_product.add_option("issue_quantity", 1)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_rfid_update["reorder_controls"]})
        response_location = setup_location.setup()

        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][0]["rfid_id"], "AVAILABLE")
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity_old = transaction[0]["reorderQuantity"]

        product_dto = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = product_dto.pop("id")
        product_dto["issueQuantity"] *=  product_dto["roundBuy"]
        pa.update_customer_product(dto=product_dto, product_id=product_id)
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity = transaction_updated[0]["reorderQuantity"]
        assert quantity_old - quantity == response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]

    @pytest.mark.parametrize("conditions_rfid_close", [
        {
            "reorder_controls": "MIN",
            "testrail_case_id": 7514
        }, 
        {
            "reorder_controls": "ISSUED",
            "testrail_case_id": 7515
        }
        ])
    @pytest.mark.regression
    def test_close_transaction_rfid_by_updated_issue_qnt_with_clc(self, api, conditions_rfid_close, delete_shipto):
        api.testrail_case_id = conditions_rfid_close["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        ra = RfidApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("type", "RFID")
        setup_location.add_option("rfid_labels", 1)
        setup_location.setup_shipto.add_option("customer.clc")
        setup_location.setup_product.add_option("issue_quantity",1)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_rfid_close["reorder_controls"]})
        response_location = setup_location.setup()

        ra.update_rfid_label(response_location["location_id"], response_location["rfid_labels"][0]["rfid_id"], "AVAILABLE")

        product_dto = pa.get_customer_product(response_location["customer_id"], response_location["product"]["partSku"])[0]
        product_id = product_dto.pop("id")
        product_dto["issueQuantity"] *= response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]
        pa.update_customer_product(dto=product_dto, product_id=product_id)
        time.sleep(5)
        transaction_updated = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        quantity = transaction_updated[0]["reorderQuantity"]
        assert transaction_updated[0]["status"] == "DO_NOT_REORDER"

    @pytest.mark.parametrize("conditions_create_by_pack", [
            {
                "create_pack_conv": 10, 
                "reorder_controls": "MIN",
                "testrail_case_id": 7516
            },
            {
                "create_pack_conv": 2,
                "reorder_controls": "ISSUED",
                "testrail_case_id": 7517
            }
            ])
    @pytest.mark.regression
    def test_create_transaction_by_pack_conversion_update_for_distributor_catalog_only_if_clc_off(self, api, conditions_create_by_pack, delete_customer):
        api.testrail_case_id = conditions_create_by_pack["testrail_case_id"]

        ta = TransactionApi(api)
        pa = ProductApi(api)
        
        setup_location_1 = SetupLocation(api)
        setup_location_1.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_create_by_pack['reorder_controls']})
        setup_location_1.setup_shipto.add_option("customer")
        setup_location_1.setup_shipto.setup_customer.add_option("clc", False)
        setup_location_1.add_option("ohi","MAX")
        setup_location_1.setup_product.add_option("package_conversion", "1")
        response_location_1 = setup_location_1.setup()

        setup_location_2 = SetupLocation(api)
        setup_location_2.setup_shipto.add_option("reorder_controls_settings", {"enable_reorder_control": True,"track_ohi":True, "reorder_controls" :conditions_create_by_pack['reorder_controls']})
        setup_location_2.setup_shipto.add_option("customer")
        setup_location_2.setup_shipto.setup_customer.add_option("clc")
        setup_location_2.add_option("ohi","MAX")
        setup_location_2.add_option("product", response_location_1["product"])
        setup_location_2.setup_product.add_option("package_conversion", "1")
        response_location_2 = setup_location_2.setup()

        customer_product = pa.get_customer_product(response_location_2["customer_id"], response_location_1["product"]["partSku"])[0]
        assert customer_product["variant"] == False

        product_dto = copy.deepcopy(response_location_1["product"])
        product_dto["packageConversion"] = conditions_create_by_pack["create_pack_conv"]
        pa.update_product(dto=product_dto, product_id=response_location_1["product"]["id"])
        time.sleep(5)

        transaction_1 = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]
        assert transaction_1[0]["status"] == "ACTIVE"
        transaction_2 = ta.get_transaction(shipto_id=response_location_2["shipto_id"])
        assert transaction_2["totalElements"] == 0

        customer_product = pa.get_customer_product(response_location_2["customer_id"], response_location_1["product"]["partSku"])[0]
        assert customer_product["variant"] == True
        assert customer_product["packageConversion"] == 1