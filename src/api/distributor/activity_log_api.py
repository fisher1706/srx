import time
from src.api.api import API
from src.resources.tools import Tools
from src.resources.messages import Message
from glbl import LOG, ERROR

class ActivityLogApi(API):
    def get_activity_log(self, size=50, shiptos=None, wait=None):
        if wait is not None:
            time.sleep(wait)
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/activity/search")
        token = self.get_distributor_token()
        dto = Tools.get_dto("activity_feed_dto.json")
        dto["size"] = size
        if shiptos is not None:
            dto["query"]["bool"]["must"] = [{"match_all":{}}, {"terms":{"eventContent.shipToId":shiptos}}]
        response = self.send_post(url, token, dto)
        if response.status_code == 200:
            LOG.info(Message.entity_operation_done.format(entity="Activity Log", operation="got"))
        else:
            ERROR(str(response.content))
        response_json = response.json()
        return response_json["data"]

    @classmethod
    def check_event(cls, event, options):
        if options.get("action") is not None:
            assert event["content"]["entities"][0]["action"] == options["action"], f"Action should be: {options['action']}, but it is {event['content']['entities'][0]['action']}"
        if options.get("event_type") is not None:
            assert event["content"]["entities"][0]["type"] == options["event_type"], f"Type should be: {options['event_type']}, but it is {event['content']['entities'][0]['type']}"
        if options.get("name") is not None:
            assert event["content"]["entities"][0]["eventContent"]["name"] == options["name"], f"Name should be: {options['name']}, but it is {event['content']['entities'][0]['eventContent']['name']}"
