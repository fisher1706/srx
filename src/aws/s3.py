from src.aws.aws import AWS
import boto3

class S3(AWS):
    def __init__(self, context):
        super().__init__(context)
        self.resource = self.session.resource("s3")

    def get_objects_in_bucket(self, bucket_name):
        bucket = self.resource.Bucket(bucket_name)
        bucket_objects = [bucket_object for bucket_object in bucket.objects.all()]
        return bucket_objects

    def get_last_modified_object_in_bucket(self, bucket_name):
        objects = self.get_objects_in_bucket(bucket_name)
        get_last_modified = lambda obj: int(obj.last_modified.strftime('%s'))
        objects = [obj for obj in sorted(objects, key=get_last_modified)]
        return objects[-1]

    def download_by_key(self, key, filename):
        pass

