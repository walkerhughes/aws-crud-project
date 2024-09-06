import boto3
from mypy_boto3_s3 import S3Client

BUCKET_NAME = "cloud-course-bucket-walker"

session = boto3.Session(profile_name="cloud-course")
s3_client: S3Client = session.client("s3")

response = s3_client.put_object(
    Bucket=BUCKET_NAME, Key="folder/hello.txt", Body="Hello, World!", ContentType="text/plain"
)
