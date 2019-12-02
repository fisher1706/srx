import boto3

class S3():
    def __init__(self):
        import boto3 
        client = boto3.client('s3')
        print(len(client.list_objects(Bucket='srx-data-bucket-qa', Prefix="auto-test")))

if __name__ == "__main__":
  S3()