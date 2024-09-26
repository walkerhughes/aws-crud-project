"""Utils for reading objects in an s3 bucket."""

from typing import Optional

import boto3

try:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.type_defs import (
        GetObjectOutputTypeDef,
        ListObjectsV2OutputTypeDef,
        ObjectTypeDef,
    )
except ImportError:
    ...


DEFAULT_MAX_KEYS = 1000


def object_exists_in_s3(bucket_name: str, object_key: str, s3_client: Optional["S3Client"] = None) -> bool:
    """
    Check is object exists in s3 bucket in AWS.

    :param bucket_name: Name of s3 bucket to delete from.
    :param object_key: Key of object to be delete.
    :param s3_client: Optional s3 client used to delete object; creates new client otherwise.

    :return: True if exists in s3 bucket, else False.
    """
    s3_client = s3_client or boto3.client("s3")
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return True
    except s3_client.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "404":
            return False
        raise


def fetch_s3_object(
    bucket_name: str, object_key: str, s3_client: Optional["S3Client"] = None
) -> "GetObjectOutputTypeDef":
    """
    Fetch object from s3 bucket in AWS.

    :param bucket_name: Name of s3 bucket to delete from.
    :param object_key: Key of object to be delete.
    :param s3_client: Optional s3 client used to get object; creates new client otherwise.
    """
    s3_client = s3_client or boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    return response


def fetch_s3_objects_using_page_token(
    bucket_name: str,
    continuation_token: str,
    max_keys: int,
    s3_client: Optional["S3Client"] = None,
) -> tuple[list["ObjectTypeDef"], Optional[str]]:
    """
    Fetch list of object keys and their metadata using a continuation token.

    :param bucket_name: Name of the S3 bucket to list objects from.
    :param continuation_token: Token for fetching the next page of results where the last page left off.
    :param max_keys: Maximum number of keys to return within this page.
    :param s3_client: Optional S3 client to use. If not provided, a new client will be created.

    :return: Tuple of a list of objects and the next continuation token.
        1. Possibly empty list of objects in the current page.
        2. Next continuation token if there are more pages, otherwise None.
    """
    s3_client = s3_client or boto3.client("s3")
    response: "ListObjectsV2OutputTypeDef" = s3_client.list_objects_v2(
        Bucket=bucket_name, ContinuationToken=continuation_token, MaxKeys=max_keys or DEFAULT_MAX_KEYS
    )
    files: list["ObjectTypeDef"] = response.get("Contents", [])
    next_continuation_token: str | None = response.get("NextContinuationToken")
    return files, next_continuation_token


def fetch_s3_objects_metadata(
    bucket_name: str,
    prefix: Optional[str] = None,
    max_keys: Optional[int] = DEFAULT_MAX_KEYS,
    s3_client: Optional["S3Client"] = None,
) -> tuple[list["ObjectTypeDef"], Optional[str]]:
    """
    Fetch list of object keys and their metadata.

    :param bucket_name: Name of the S3 bucket to list objects from.
    :param prefix: Prefix to filter objects by.
    :param max_keys: Maximum number of keys to return within this page.
    :param s3_client: Optional S3 client to use. If not provided, a new client will be created.

    :return: Tuple of a list of objects and the next continuation token.
        1. Possibly empty list of objects in the current page.
        2. Next continuation token if there are more pages, otherwise None.
    """
    s3_client = s3_client or boto3.client("s3")
    response: "ListObjectsV2OutputTypeDef" = s3_client.list_objects_v2(
        Bucket=bucket_name, Prefix=prefix or "", MaxKeys=max_keys or DEFAULT_MAX_KEYS
    )
    files: list["ObjectTypeDef"] = response.get("Contents", [])
    next_continuation_token: str | None = response.get("NextContinuationToken")
    return files, next_continuation_token
