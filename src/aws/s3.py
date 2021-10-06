import os
import time
from src.aws.aws import AWS

class S3(AWS):
    'The class for using S3 service'

    def __init__(self, context):
        super().__init__(context)
        self.resource = self.session.resource("s3")

    def get_objects_in_bucket(self, bucket_name):
        bucket = self.resource.Bucket(bucket_name)
        bucket_objects = list(bucket.objects.all())
        return bucket_objects

    def get_last_modified_object_in_bucket(self, bucket_name):
        objects = self.get_objects_in_bucket(bucket_name)
        get_last_modified = lambda obj: int(obj.last_modified.strftime('%s'))
        objects = list(sorted(objects, key=get_last_modified))
        return objects[-1]

    def download_by_key(self, bucket_name, key, filename):
        folder = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/output/"
        self.resource.Bucket(bucket_name).download_file(key, folder+filename)
        self.logger.info("File has been succesfully downloaded from S3")

    def clear_bucket(self, bucket_name):
        bucket = self.resource.Bucket(bucket_name)
        bucket.objects.all().delete()
        # for bucket_object in bucket.objects.all():
        #     bucket_object.delete()

    def wait_for_new_object(self, bucket_name, current_count, retries=10):
        for _ in range(retries):
            time.sleep(10)
            objects = self.get_objects_in_bucket(bucket_name)
            objects_count = len(objects)
            if objects_count > current_count:
                self.logger.info("New object has appeared in the bucket")
                break
            else:
                self.logger.info("Waiting for the new object appears in the bucket. Next attempt in 10 seconds")
        else:
            self.logger.error(f"There is no new objects in the bucket after {retries*10} seconds")
