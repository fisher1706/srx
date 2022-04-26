class GeneralFunctions():
    @staticmethod
    def fill_location_body(location, product, options, locker_number=None):
        if options.get("locker_location"):
            location["attributeName1"] = "Locker"
            location["attributeValue1"] = locker_number
            location["attributeName2"] = "Door"
            location["attributeValue2"] = "1"
            location["attributeName3"] = "Cell"
            location["attributeValue3"] = "1"
        elif options["location_pairs"] is None:
            location["attributeName1"] = product["partSku"]
            location["attributeValue1"] = product["partSku"]
        else:
            location["attributeName1"] = options["location_pairs"]["attributeName1"] #pylint: disable=E1136
            location["attributeValue1"] = options["location_pairs"]["attributeValue1"] #pylint: disable=E1136
            location["attributeName2"] = options["location_pairs"]["attributeName2"] #pylint: disable=E1136
            location["attributeValue2"] = options["location_pairs"]["attributeValue2"] #pylint: disable=E1136
            location["attributeName3"] = options["location_pairs"]["attributeName3"] #pylint: disable=E1136
            location["attributeValue3"] = options["location_pairs"]["attributeValue3"] #pylint: disable=E1136
            location["attributeName4"] = options["location_pairs"]["attributeName4"] #pylint: disable=E1136
            location["attributeValue4"] = options["location_pairs"]["attributeValue4"] #pylint: disable=E1136

        location_min = product["roundBuy"] if options["min"] is None else options["min"]
        location_max = product["roundBuy"]*3 if options["max"] is None else options["max"]
        location["orderingConfig"] = {
            "product": {
                "partSku": product["partSku"],
            },
            "type": options["type"],
            "currentInventoryControls": {
                "min": location_min,
                "max": location_max
            },
            "criticalMin": options["critical_min"] if options["critical_min"] is not None else None,
        }
        if options["autosubmit"] is not None:
            location["autoSubmit"] = bool(options["autosubmit"])
