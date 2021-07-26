class Message():
    assert_status_code = "Incorrect status_code! Expected: {expected_status_code}; Actual: {actual_status_code}; Repsonse content:\n{content}"
    info_operation_with_expected_code = "{entity} {operation} completed with status_code = '{status_code}', as expected: {content}"
    entity_with_id_operation_done = "{entity} with ID = {id} has been successfully {operation}"
    entity_operation_done = "{entity} has been successfully {operation}"