import boto3
from src.resources.tools import Tools

class AWS():
    'The parent class for all AWS services'
    def __init__(self, context):
        self.context = context
        self.logger = context.logger
        self.url = context.session_context.url
        self.data = context.data
        if not context.session_context.credentials:
            credentials = Tools.get_dto("creds.json", path="/output/")
            access_key_id = credentials["Credentials"]["AccessKeyId"]
            secret_access_key = credentials["Credentials"]["SecretAccessKey"]
            session_token = credentials["Credentials"]["SessionToken"]
            self.session = boto3.Session(aws_access_key_id=access_key_id,
                                         aws_secret_access_key=secret_access_key,
                                         aws_session_token=session_token)
        else:
            self.session = boto3.Session()
