import pytest

@pytest.fixture(scope="function")
def ui(driver, base_context):
    context_object = base_context
    context_object.driver = driver
    context_object.testrail_run_id = context_object.data.testrail_run_id
    return context_object

@pytest.fixture(scope="function")
def api(base_context):
    context_object = base_context
    context_object.testrail_run_id = context_object.data.testrail_run_id
    return context_object

@pytest.fixture(scope="function")
def mobile_api(base_context):
    context_object = base_context
    context_object.testrail_run_id = context_object.data.mobile_testrail_run_id
    return context_object

@pytest.fixture(scope="function")
def smoke_ui(driver, smoke_context):
    context_object = smoke_context
    context_object.driver = driver
    context_object.testrail_run_id = context_object.data.smoke_testrail_run_id
    return context_object

@pytest.fixture(scope="function")
def smoke_api(smoke_context):
    context_object = smoke_context
    context_object.testrail_run_id = context_object.data.smoke_testrail_run_id
    return context_object

@pytest.fixture(scope="function")
def permission_ui(driver, permission_context):
    context_object = permission_context
    context_object.driver = driver
    return context_object

@pytest.fixture(scope="function")
def permission_api(permission_context):
    context_object = permission_context
    return context_object

@pytest.fixture(scope="function")
def srx_integration_api(srx_integration_context):
    context_object = srx_integration_context
    context_object.testrail_run_id = context_object.data.ilx_testrail_run_id
    return context_object

@pytest.fixture(scope="function")
def load_api(load_context):
    context_object = load_context
    return context_object
