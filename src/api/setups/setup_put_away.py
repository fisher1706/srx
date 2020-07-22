from src.api.setups.setup_location import setup_location
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.settings_api import SettingsApi
from src.resources.tools import Tools
import copy

def setup_put_away(context, transaction=False, transaction_count=None, bulk_putaway=False):
    ta = TransactionApi(context)
    la = LocationApi(context)
    sta = SettingsApi(context)

    #create location
    response_location = setup_location(context)
    product = response_location["product"]["partSku"]
    shipto_id = response_location["shipto_id"]
    

    response = {
        "product": product,
        "shipto_id": shipto_id
    }

    if (transaction == True):
        #get transaction id and make it QUOTED
        sta.set_checkout_software_settings_for_shipto(shipto_id)
        ordering_config_id = la.get_ordering_config_by_sku(shipto_id, product)
        ta.create_active_item(shipto_id, ordering_config_id, repeat=6)
        transaction = ta.get_transaction(sku=product, shipto_id=shipto_id)
        transaction_id = transaction["entities"][0]["id"]
        reorderQuantity = transaction["entities"][0]["reorderQuantity"]
        ta.update_replenishment_item(transaction_id, reorderQuantity, "QUOTED")

        response["reorderQuantity"] = reorderQuantity
        response["transaction_id"] = transaction_id

    return copy.deepcopy(response)

