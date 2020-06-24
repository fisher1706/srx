import pytest
from src.api.distributor.distributor_hardware_api import DistributorHardwareApi
from src.api.admin.admin_hardware_api import AdminHardwareApi

class TestHardware():
    @pytest.mark.smoke
    def test_smoke_get_device_list(self, smoke_api):
        smoke_api.testrail_case_id = 2003

        ha = DistributorHardwareApi(smoke_api)
        response = ha.get_device_list()
        count = len(response)
        assert count != 0, "Device list is empty"