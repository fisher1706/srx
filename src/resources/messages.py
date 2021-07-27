class Message():
    'The class contains default message templates'

    assert_status_code = "Incorrect status_code! Expected: {expected}; Actual: {actual}; Repsonse content:\n{content}"
    info_operation_with_expected_code = "{entity} {operation} completed with status_code = '{status_code}', as expected: {content}"
    entity_with_id_operation_done = "{entity} with ID = {id} has been successfully {operation}"
    entity_operation_done = "{entity} has been successfully {operation}"

    def __setattr__(self, key, value):
        if hasattr(key):
            object.__setattr__(key, value)
        else:
            raise TypeError("Cannot create new attribute for class Message")
