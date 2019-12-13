from src.resources.case import Case
from src.resources.activity import Activity
from src.cases.api import *

if __name__ == "__main__":
    #api tests
    api_activity = Activity(api_test=True)

    zero_transaction_qty (Case(api_activity, 'SUITE'))

    api_activity.logger.output_suite_result()
    api_activity.finish_activity()