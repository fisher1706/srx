import pytest
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_rfid import setup_rfid
from src.api.setups.setup_rfid_location import setup_rfid_location
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.settings_api import SettingsApi

class TestRfid():
    @pytest.mark.regression
    def test_rfid_label_crud(self, ui, delete_shipto):
        ui.testrail_case_id = 1918