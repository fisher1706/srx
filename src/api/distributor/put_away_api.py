from src.api.api import API
from src.fixtures.decorators import default_expected_code
from src.resources.messages import Message

class PutAwayApi(API):
    @default_expected_code(200)
    def put_away(self, dto, expected_status_code=None):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/putaway")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Put Away", operation="performed"))
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Put", operation="Away", status_code=response.status_code, content=response.content))
