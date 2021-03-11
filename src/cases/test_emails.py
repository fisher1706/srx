import pytest
from src.aws.s3 import S3

class TestEmails():
    @pytest.mark.regression
    def test_accept_distributor_user_invitation(self, api):
        #ui.testrail_case_id = 4095

        s3 = S3(api)
        last_email_key = s3.get_last_modified_object_in_bucket(api.data.email_data_bucket).key

        print(last_email_key)

