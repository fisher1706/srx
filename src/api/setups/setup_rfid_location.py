from src.api.setups.setup_location import setup_location
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.location_api import LocationApi
import copy

def setup_rfid_location(context, number_of_labels=None):
    location_response = setup_location(context, location_type="RFID")

    rfid_labels = list()

    if (number_of_labels is not None):
        ra = RfidApi(context)
        la = LocationApi(context)
        location_id = la.get_location_by_sku(location_response["shipto_id"], location_response["product"]["partSku"])[0]["id"]
        for index in range(0, number_of_labels):
            rfid_labels.append(ra.create_rfid(location_id))

    response = {
        "location": location_response,
        "location_id": location_id,
        "labels": rfid_labels,
        "shipto_id": location_response["shipto_id"],
        "product": location_response["product"]
    }
    
    return copy.deepcopy(response)