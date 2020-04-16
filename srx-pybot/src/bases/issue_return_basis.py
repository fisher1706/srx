from src.api.checkout.checkout_api import CheckoutApi

from src.api.distributor.location_api import LocationApi
from src.resources.tools import Tools
import copy

def issue_return_basis(case, shipto_id, product, quantity, issue_product=None, return_product=None):
    ca = CheckoutApi(case)
    la = LocationApi(case)

    location_response = la.get_location_by_sku(shipto_id, product)
    location = location_response[0]["id"]
    location_type = location_response[0]["orderingConfig"]["type"]

    # check if cart is empry
    cart_response = ca.get_cart()
    if (cart_response["items"] is None):
        case.activity.logger.info(f"Cart is empty")
    elif (cart_response["items"] is not None):
        case.activity.logger.info(f"Cart have {len(cart_response['items'])}, cart will be closed")
        ca.close_cart()

    if (issue_product is True):
        ca.checkout_cart(location, quantity, location_type, issue_product=True)
        cart_response = ca.get_cart()
        location_response[0]["cartItemId"] = cart_response["items"][0]["cartItemId"]
        location_response[0]["quantity"] = quantity
        ca.issue_product(location_response)
    
    if (return_product is True):
        ca.checkout_cart(location, quantity, location_type, return_product=True)
        cart_response = ca.get_cart()
        location_response[0]["cartItemId"] = cart_response["items"][0]["cartItemId"]
        location_response[0]["quantity"] = quantity
        ca.return_product(location_response)
