"""Utils functions for writing to s3 an bucket."""

from typing import Optional

import boto3

try:
    from mypy_boto3_s3 import S3Client
except ImportError:
    ...


def upload_s3_object(
    bucket_name: str,
    object_key: str,
    file_content: bytes,
    s3_client: Optional["S3Client"] = None,
    content_type: Optional[str] = None,
) -> None:
    """
    Write an object to an s3 bucket in AWS.

    :param bucket_name: Name of s3 bucket to delete from.
    :param object_key: Key of object to be delete.
    :param file_content: The content to be written to `bucket_name` at `object_key`.
    :param s3_client: Optional s3 client used to delete object; creates new client otherwise.
    :param content_type: MIME type of a file.
    """
    content_type = content_type or "application/octet-stream"
    s3_client = s3_client or boto3.client("s3")
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content, ContentType=content_type)
