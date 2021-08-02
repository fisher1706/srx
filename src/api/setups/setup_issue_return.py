from src.api.checkout.checkout_api import CheckoutApi
from src.api.distributor.location_api import LocationApi

def setup_issue_return(context, shipto_id, product, quantity=None, epc=None, issue_product=None, return_product=None, passcode=None):
    ca = CheckoutApi(context)
    la = LocationApi(context)

    location_response = la.get_location_by_sku(shipto_id, product)
    location = location_response[0]["id"]
    location_type = location_response[0]["orderingConfig"]["type"]

    # check if cart is empry
    cart_response = ca.get_cart(passcode=passcode)
    if cart_response["items"] is None:
        context.logger.info("Cart is empty")
    elif cart_response["items"] is not None:
        context.logger.info(f"Cart have {len(cart_response['items'])}, cart will be closed")
        ca.close_cart(passcode=passcode)

    if location_type == "LABEL":
        if issue_product:
            ca.checkout_cart(location, location_type, quantity=quantity, issue_product=True, passcode=passcode)
            cart_response = ca.get_cart(passcode=passcode)
            location_response[0]["cartItemId"] = cart_response["items"][0]["cartItemId"]
            location_response[0]["quantity"] = quantity
            ca.issue_product(location_response, passcode=passcode)
        if return_product:
            ca.checkout_cart(location, location_type, quantity=quantity, return_product=True, passcode=passcode)
            cart_response = ca.get_cart(passcode=passcode)
            location_response[0]["cartItemId"] = cart_response["items"][0]["cartItemId"]
            location_response[0]["quantity"] = quantity
            ca.return_product(location_response, passcode=passcode)

    if location_type == "RFID":
        if issue_product:
            ca.validate_rfid(location, location_type, epc, issue_product=True, passcode=passcode)
            ca.checkout_cart(location, location_type, epc=epc, issue_product=True, passcode=passcode)
            cart_response = ca.get_cart(passcode=passcode)
            location_response[0]["cartItemId"] = cart_response["items"][0]["cartItemId"]
            location_response[0]["quantity"] = 1
            location_response[0]["epc"] = epc
            ca.issue_product(location_response, passcode=passcode)
        if return_product:
            ca.validate_rfid(location, location_type, epc, return_product=True, passcode=passcode)
            ca.checkout_cart(location, location_type, epc=epc, return_product=True, passcode=passcode)
            cart_response = ca.get_cart(passcode=passcode)
            location_response[0]["cartItemId"] = cart_response["items"][0]["cartItemId"]
            location_response[0]["quantity"] = 1
            location_response[0]["epc"] = epc
            ca.return_product(location_response, passcode=passcode)
