import boto3
import botocore.exceptions
import hmac
import hashlib
import base64

class Cognito():
    def __init__(self, activity, username, password):
        self.USER_POOL_ID = activity.USER_POOL_ID
        self.CLIENT_ID = activity.CLIENT_ID
        self.CLIENT_SECRET = activity.CLIENT_SECRET
        self.client = None
        self.initiate_auth(username, password)

    def get_secret_hash(self, username):
        msg = username + self.CLIENT_ID
        dig = hmac.new(str(self.CLIENT_SECRET).encode('utf-8'), msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        return d2

    def initiate_auth(self, username, password):
        client = boto3.client('cognito-idp', region_name='us-east-1')
        self.resp = client.admin_initiate_auth(
            UserPoolId=self.USER_POOL_ID,
            ClientId=self.CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': self.get_secret_hash(username),
                'PASSWORD': password
            },
            ClientMetadata={
                'username': username,
                'password': password
            })
        self.id_token = self.resp['AuthenticationResult']['IdToken']