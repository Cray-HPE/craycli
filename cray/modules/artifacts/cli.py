#
#  MIT License
#
#  (C) Copyright 2020-2023 Hewlett Packard Enterprise Development LP
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.
#
""" Artifact - thin wrapper over S3 """
# pylint: disable=invalid-name,redefined-outer-name,missing-docstring,unused-argument,broad-except
import datetime
import hashlib
import json
import os
import sys
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

from cray.core import argument
from cray.core import group
from cray.core import pass_context
from cray.echo import echo
from cray.errors import BadResponseError
from cray.rest import request


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError(f"Unknown type: {type(x)}")


def md5(filename):
    """ Utility for md5sum of a file """
    hashmd5 = hashlib.md5()
    with open(filename, "rb") as afile:
        for chunk in iter(lambda: afile.read(4096), b""):
            hashmd5.update(chunk)
    return hashmd5.hexdigest()


def get_s3_client():
    """ Retrieve a boto3 client using creds from STS """
    # Assumes running in Kubernetes somewhere like this
    resp = request('PUT', 'apis/sts/token')
    if not resp.ok:
        raise BadResponseError(resp)
    creds = resp.json()
    echo("S3 credentials retrieved successfully")

    try:
        client = boto3.client(
            's3',
            aws_access_key_id=creds['Credentials']['AccessKeyId'],
            aws_secret_access_key=creds['Credentials']['SecretAccessKey'],
            aws_session_token=creds['Credentials']['SessionToken'],
            endpoint_url=creds['Credentials']['EndpointURL'],
            region_name=''
        )
    except Exception as err:
        sys.exit(err)

    return client


@group()
def cli():
    """ Manage artifacts in S3 """
    pass


@cli.group()
def buckets():
    """ S3 Bucket commands """
    pass


@buckets.command(name='list')
@pass_context
def list_buckets(ctx):
    """List buckets."""
    s3client = get_s3_client()
    try:
        buckets = s3client.list_buckets()
    except ClientError as err:
        sys.exit(str(err))

    return [bucket['Name'] for bucket in buckets.get('Buckets')]


@cli.command(name='list')
@argument('bucket', metavar='BUCKET')
@pass_context
def list_objects(ctx, bucket):
    """ List objects in a bucket """
    # Load config to make sure it exists.
    s3client = get_s3_client()
    try:
        files = []
        paginator = s3client.get_paginator('list_objects')
        pages = paginator.paginate(Bucket=bucket)

        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    files.append(obj)

    except (s3client.exceptions.NoSuchBucket, ClientError) as err:
        sys.exit(str(err))
    return {
        "artifacts": json.loads(json.dumps(files, default=datetime_handler))
    }


@cli.command(name='describe')
@argument('bucket', metavar='BUCKET')
@argument('obj', metavar='OBJECT')
@pass_context
def describe_object(ctx, bucket, obj):
    """ View metadata about an object from a bucket """
    s3client = get_s3_client()
    try:
        files = s3client.head_object(Bucket=bucket, Key=obj)
    except (s3client.exceptions.NoSuchBucket, ClientError) as err:
        sys.exit(str(err))

    files.pop("ResponseMetadata")  # not terribly useful info here
    return {
        "artifact": json.loads(json.dumps(files, default=datetime_handler))
    }


@cli.command(name='create')
@argument('bucket', metavar='BUCKET')
@argument('obj', metavar='OBJECT')
@argument('filename', metavar='FILEPATH')
@pass_context
def upload_object(ctx, bucket, obj, filename):
    """ Create a new object in a bucket """
    # Check if the file exists locally before creating the object
    if not os.path.isfile(filename):
        print(f"Error: File {filename} does not exist")
        sys.exit(1)

    s3client = get_s3_client()
    md5sum = md5(filename)
    obj_id = obj

    # Create the object and then upload the file
    try:
        s3client.put_object(Bucket=bucket, Key=obj_id, ACL='public-read')
    except s3client.exceptions.NoSuchBucket as err:
        sys.exit(str(err))
    except ClientError as err:
        try:
            s3client.delete_object(Bucket=bucket, Key=obj_id)
        except Exception as delete_err:
            echo(
                f"Unsuccessful upload. Unable to delete object: Error:"
                f" {delete_err}"
            )
        sys.exit(str(err))

    try:
        upload_args = (filename, bucket, obj_id)

        config = TransferConfig(use_threads=False)
        upload_kwargs = {
            'Config': config,
            'ExtraArgs': {
                'Metadata': {
                    'md5sum': md5sum,
                }
            }
        }

        s3client.upload_file(*upload_args, **upload_kwargs)

        # Pass back the name/key as well
        return {"artifact": obj_id, "Key": obj}

    except ClientError as err:
        try:
            s3client.delete_object(Bucket=bucket, Key=obj_id)
        except Exception as delete_err:
            echo(
                f"Unsuccessful upload. Unable to delete object: Error:"
                f" {delete_err}"
            )
        sys.exit(str(err))


@cli.command(name='get')
@argument('bucket', metavar='BUCKET')
@argument('obj', metavar='OBJECT')
@argument('filename', metavar='FILEPATH')
@pass_context
def download_object(ctx, bucket, obj, filename):
    """ Download an object from a bucket """
    s3client = get_s3_client()
    config = TransferConfig(use_threads=False)

    try:
        s3client.download_file(bucket, obj, filename, Config=config)
    except (ClientError, s3client.exceptions.NoSuchBucket) as err:
        sys.exit(str(err))


@cli.command(name='delete')
@argument('bucket', metavar='BUCKET')
@argument('obj', metavar='OBJECT')
@pass_context
def delete_object(ctx, bucket, obj):
    """ Delete an object from a bucket """
    s3client = get_s3_client()
    try:
        s3client.head_object(Bucket=bucket, Key=obj)
    except (ClientError, s3client.exceptions.NoSuchKey) as err:
        if "404" in str(err):
            try:
                Buckets = s3client.list_buckets().get('Buckets')
                if bucket in [b['Name'] for b in Buckets]:
                    print("Error: Object was not found in bucket")
                else:
                    print("Error: Bucket does not exist")
            except ClientError as err:
                sys.exit(str(err))
        sys.exit(str(err))
    try:
        output = s3client.delete_object(Bucket=bucket, Key=obj)
        echo(output)
    except (ClientError, s3client.exceptions.NoSuchBucket) as err:
        sys.exit(str(err))
