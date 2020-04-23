from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.activity_log_api import ActivityLogApi
from src.resources.tools import Tools

def label_transaction_activity_log(case, token):
    case.log_name("Transaction for LABEL and Activity Log")
    #case.testrail_config(2005)

    try:
        ta = TransactionApi(case)
        ala = ActivityLogApi(case)

        activity_log_before = ala.get_activity_log()
        activity_log_records_before = activity_log_before["totalElements"]
        # close all Active transactions
        transactions = ta.get_transaction(status="ACTIVE")
        if (transactions["totalElements"] != 0):
            case.activity.logger.info("There are some active transactions, they will be closed")
            ta.update_transactions_with_specific_status("ACTIVE", 0, "DO_NOT_REORDER")
        ta.create_active_item(case.activity.variables.shipto_id, case.activity.variables.ordering_config_id, repeat=6)
        transactions = ta.get_transaction(status="ACTIVE")
        transaction_id = transactions["entities"][0]["id"]
        assert transactions["totalElements"] != 0, "There is no ACTIVE transaction"
        ta.update_replenishment_item(transaction_id, 0, "DO_NOT_REORDER")
        activity_log_after = ala.get_activity_log()
        activity_log_records_after = activity_log_after["totalElements"]
        assert activity_log_records_before != activity_log_records_after, "There are no new records in activity log"

        case.finish_case()
    except:
        case.critical_finish_case()
    
if __name__ == "__main__":
    case = Case(Activity(api_test=True, smoke=True))
    distributor_token = TransactionApi(case).get_distributor_token()
    label_transaction_activity_log(case, distributor_token)