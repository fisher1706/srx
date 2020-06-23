from src.resources.testrail_client import APIClient

class Testrail():
    def __init__(self, user, password):
        self.client = APIClient("https://agilevisionio.testrail.io")
        self.client.user = user
        self.client.password = password

    def run_report(self, report_template_id):
        uri = f"run_report/{report_template_id}"
        return self.client.send_get(uri)

    def get_reports(self, project_id):
        uri = f"get_reports/{project_id}"
        return self.client.send_get(uri)

    def get_tests(self, run_id):
        uri = f"get_tests/{run_id}"
        return self.client.send_get(uri)

    def add_result_for_case(self, run_id, case_id, status_id, comment):
        uri = f"add_result_for_case/{run_id}/{case_id}"
        body = {
            "status_id": status_id,
            "comment": comment
        }
        return self.client.send_post(uri, body)