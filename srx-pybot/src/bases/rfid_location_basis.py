from src.bases.location_basis import location_basis
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.location_api import LocationApi
import copy

def rfid_location_basis(case, number_of_labels=None):
    location_response = location_basis(case, location_type="RFID")

    rfid_labels = list()

    if (number_of_labels is not None):
        ra = RfidApi(case)
        la = LocationApi(case)
        location_id = la.get_location_by_sku(location_response["shipto_number"], location_response["product"]["partSku"])[0]["id"]
        for index in range(0, number_of_labels):
            rfid_labels.append(ra.create_rfid(location_id))

    response = {
        "location": location_response,
        "location_id": location_id,
        "labels": rfid_labels,
        "shipto_id": location_response["shipto_number"],
        "product": location_response["product"]
    }
    
    return copy.deepcopy(response)