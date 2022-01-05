import types

def transaction(status=None, quantity_ordered=None, quantity_shipped=None):
    mapper = types.SimpleNamespace()
    mapper.status = status
    mapper.quantity_ordered = quantity_ordered
    mapper.quantity_shipped = quantity_shipped
    return mapper

def several_transactions(*args):
    mapper = types.SimpleNamespace()
    for index, set in enumerate(args):
        mapper.__setattr__(f"status_{index+1}", set[0])
        mapper.__setattr__(f"quantity_ordered_{index+1}", set[1])
        mapper.__setattr__(f"quantity_shipped_{index+1}", set[2])
    return mapper

