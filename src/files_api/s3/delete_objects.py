"""Utils for deleting objects in an s3 bucket."""

from typing import Optional

import boto3

try:
    from mypy_boto3_s3 import S3Client
except ImportError:
    ...


def delete_s3_object(bucket_name: str, object_key: str, s3_client: Optional["S3Client"] = None) -> None:
    """
    Delete object from s3 bucket in AWS.

    :param bucket_name: Name of s3 bucket to delete from.
    :param object_key: Key of object to be delete.
    :param s3_client: Optional s3 client used to delete object; creates new client otherwise.
    """
    s3_client = s3_client or boto3.client("s3")
    s3_client.delete_object(Bucket=bucket_name, Key=object_key)
