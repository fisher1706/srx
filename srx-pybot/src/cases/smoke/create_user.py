from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.user_api import UserApi
from src.resources.tools import Tools

def create_user(case):
    case.log_name("Create/Get/Delete Distributor super user")
    case.testrail_config(2002)

    try:
        ua = UserApi(case)
        user_body = {
            "email": Tools.random_email(20),
            "firstName": Tools.random_string_l(),
            "lastName": Tools.random_string_l()
        }

        user_id = ua.create_distributor_user(user_body)
        response = ua.get_distributor_super_user_by_email(user_body["email"])
        count = len(response)
        assert count == 1, f"Users count is {count}"
        user = response[0]
        email = user["email"]
        name = user["firstName"]
        last_name = user["lastName"]
        assert email == user_body["email"], f"User email is {email}, but should be {user_body['email']}"
        assert name == user_body["firstName"], f"User name is {name}, but should be {user_body['firstName']}"
        assert last_name == user_body["lastName"], f"User last name is {last_name}, but should be {user_body['lastName']}"
        ua.delete_user(user_id)

        case.finish_case()
    except:
        case.critical_finish_case()
    
if __name__ == "__main__":
    case = Case(Activity(api_test=True, smoke=True))
    UserApi(case).get_distributor_token()
    create_user(case)