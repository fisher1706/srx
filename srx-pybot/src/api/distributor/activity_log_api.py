from src.api.api import API
import time

class ActivityLogApi(API):
    def __init__(self, case):
        super().__init__(case)

    def get_activity_log(self):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/activity/search")
        token = self.get_distributor_token()
        dto = {
            "query": {
                "bool": {
                    "must":{
                        "match_all":{}
                        }
                    }
                },
            "sort": [{"createdAt":{"order":"desc","missing":"_last"}}],
            "from":0,
            "size":50
            }
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Activity log has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]