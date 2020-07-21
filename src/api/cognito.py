import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
from warrant.aws_srp import AWSSRP

class Cognito():
    def __init__(self, username, password, user_pool_id, client_id, client_secret=None):
        self.USER_POOL_ID = user_pool_id
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.initiate_auth(username, password)

    def get_secret_hash(self, username):
        msg = username + self.CLIENT_ID
        dig = hmac.new(str(self.CLIENT_SECRET).encode('utf-8'), msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        return d2

    def initiate_auth(self, username, password):
        #client = boto3.client('cognito-idp', region_name='us-east-1')
        client = boto3.client('cognito-idp', region_name='us-east-1', aws_access_key_id="ASIAWFDFNE5NEQX3CTBV", aws_secret_access_key="LAL7yS/i/YN8ch7YaZw/ln1rBYhBE5dHVseJgfhW", aws_session_token="FwoGZXIvYXdzEGEaDMcFUv4XeaxTV/COCiKGAWz4bvJVwXrOYqub+G3ovRqd/EYOGMx80GZso+6AJs4+Vz7T+jwHdlKfDIfNLUB+ws/lAmefKXfEukq1jVnI2Adg5ub+dZcFMtbs4Ukw7VTVW3ModtQ+Y6CzLJZLscYWj0Z5GLmmL6ZA8Wu100SURb7JwW9SQos/bbukvkrdxkYyrmTrTtqkKI3nlfgFMih0yKzr2FASaQnvZy4OHotJ2njEAUikVlAEtLC1ZSyMw6ENPkl0wSTX")
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