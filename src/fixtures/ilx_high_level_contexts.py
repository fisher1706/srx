import pytest

@pytest.fixture(scope="function")
def ui_ilx(driver_ilx, ilx_context):
    ilx_context_object = ilx_context
    ilx_context_object.ilx_driver = driver_ilx
    return ilx_context_object
