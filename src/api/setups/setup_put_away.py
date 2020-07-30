from src.api.setups.setup_location import setup_location
from src.api.setups.setup_locker_location import setup_locker_location
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.settings_api import SettingsApi
from src.resources.tools import Tools
import copy

def setup_put_away(context, transaction=False, shipto_id=None, is_asset=None, trigger_type="LABEL"):
    ta = TransactionApi(context)
    la = LocationApi(context)
    sta = SettingsApi(context)

    #create location
    if (trigger_type == "LABEL"):
        response_location = setup_location(context, shipto_id=shipto_id, is_asset=is_asset)
    elif (trigger_type == "LOCKER"):
        response_location = setup_locker_location(context, is_asset=is_asset)

    product = response_location["product"]["partSku"]
    shipto_id = response_location["shipto_id"]
    

    response = {
        "partSku": product,
        "shipToId": shipto_id,
        "quantity": response_location["location"]["orderingConfig"]["currentInventoryControls"]["max"]
    }

    if (transaction):
        #get transaction id and make it QUOTED
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        ordering_config_id = la.get_ordering_config_by_sku(shipto_id, product)
        ta.create_active_item(shipto_id, ordering_config_id, repeat=6)
        transaction = ta.get_transaction(sku=product, shipto_id=shipto_id)
        transaction_id = transaction["entities"][0]["id"]
        reorderQuantity = transaction["entities"][0]["reorderQuantity"]
        ta.update_replenishment_item(transaction_id, reorderQuantity, "QUOTED")

        response["quantity"] = reorderQuantity
        response["transactionId"] = transaction_id

    return copy.deepcopy(response)

