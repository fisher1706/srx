import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
from warrant.aws_srp import AWSSRP
from src.resources.tools import Tools

class Cognito():
    def __init__(self, username, password, user_pool_id, client_id, credentials, client_secret=None):
        self.USER_POOL_ID = user_pool_id
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.credentials = credentials
        self.initiate_auth(username, password)

    def get_secret_hash(self, username):
        msg = username + self.CLIENT_ID
        dig = hmac.new(str(self.CLIENT_SECRET).encode('utf-8'), msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        return d2

    def initiate_auth(self, username, password):
        if (self.credentials):
            client = boto3.client('cognito-idp', region_name='us-east-1')
        elif (not self.credentials):
            creds = Tools.get_dto("creds.json", path="/output/")
            
            access_key_id = creds["Credentials"]["AccessKeyId"]
            secret_access_key = creds["Credentials"]["SecretAccessKey"]
            session_token = creds["Credentials"]["SessionToken"]

            client = boto3.client('cognito-idp', region_name='us-east-1', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, aws_session_token=session_token)
        if (self.CLIENT_SECRET is not None):
            self.resp = client.admin_initiate_auth(
                UserPoolId=self.USER_POOL_ID,
                ClientId=self.CLIENT_ID,
                AuthFlow="ADMIN_NO_SRP_AUTH",
                AuthParameters = {
                    'USERNAME': username,
                    'SECRET_HASH': self.get_secret_hash(username),
                    'PASSWORD': password
                },
                ClientMetadata={
                    'username': username,
                    'password': password
                })
            self.id_token = self.resp['AuthenticationResult']['IdToken']
        else:
            aws = AWSSRP(username=username, password=password, pool_id=self.USER_POOL_ID, client_id=self.CLIENT_ID)
            tokens = aws.authenticate_user()
            self.id_token = tokens['AuthenticationResult']['IdToken']