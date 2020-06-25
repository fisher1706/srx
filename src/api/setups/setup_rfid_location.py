from src.api.setups.setup_location import setup_location
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.location_api import LocationApi
import copy

def setup_rfid_location(context, number_of_labels=None, product_dto=None):
    if (product_dto is None):
        response_location = setup_location(context, location_type="RFID")
    else:
        response_location = setup_location(context, location_type="RFID", product_dto=product_dto)

    rfid_labels = list()

    if (number_of_labels is not None):
        ra = RfidApi(context)
        la = LocationApi(context)
        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        for index in range(0, number_of_labels):
            rfid_labels.append(ra.create_rfid(location_id))

    response = {
        "location": response_location,
        "location_id": location_id,
        "labels": rfid_labels,
        "shipto_id": response_location["shipto_id"],
        "product": response_location["product"]
    }
    
    return copy.deepcopy(response)