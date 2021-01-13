""" Artifact - thin wrapper over S3 with ARS backwards compatibility """
#pylint: disable=invalid-name,redefined-outer-name,missing-docstring,unused-argument,broad-except
import datetime
import hashlib
import json
import sys
import uuid

import click

from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
import boto3

from cray.core import group, argument, option, pass_context
from cray.rest import request
from cray.errors import BadResponseError
from cray.echo import echo


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type: %s" % type(x))


def md5(filename):
    """ Utility for md5sum of a file """
    hashmd5 = hashlib.md5()
    with open(filename, "rb") as afile:
        for chunk in iter(lambda: afile.read(4096), b""):
            hashmd5.update(chunk)
    return hashmd5.hexdigest()


def get_s3_client():
    """ Retrieve a boto3 client using creds from STS """
    # Assumes running in k8s somewhere like this
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
        files = s3client.list_objects(Bucket=bucket).get('Contents', [])
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
@option('--expires', metavar='EXPIRES', help='Seconds until download url expiration.',
        default=60*60)
@pass_context
def upload_object(ctx, bucket, obj, filename, expires):
    """ Create a new object in a bucket """

    #
    # Remove this check along with the --expires parameter when ARS is fully deprecated
    #
    if expires > 3600:
        raise click.ClickException("Maximum download url timeout is 3600 seconds: %d" % expires)

    s3client = get_s3_client()
    md5sum = md5(filename)

    if bucket == 'ars-app':
        # Generate an ID, for compatibility of some services that validate that ARS
        # artifacts are UUID, this must be a UUID and the S3 object must use it as
        # the object name. Can be removed when ARS is fully deprecated.
        obj_id = str(uuid.uuid4())
    else:
        obj_id = obj

    # Create the object and a download url, then upload the file with the ARS-
    # compatible metadata
    try:
        s3client.put_object(Bucket=bucket, Key=obj_id, ACL='public-read')
        url = s3client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': obj_id},
            ExpiresIn=expires,
        )
    except s3client.exceptions.NoSuchBucket as err:
        sys.exit(str(err))
    except ClientError as err:
        try:
            s3client.delete_object(Bucket=bucket, Key=obj_id)
        except Exception as delete_err:
            echo("Unsuccessful upload. Unable to delete object: Error: %s" % delete_err)
        sys.exit(str(err))

    try:
        upload_args = (filename, bucket, obj_id)

        config = TransferConfig(use_threads=False)
        if bucket == 'ars-app':
            # ARS-compatible metadata, remove when ARS is fully deprecated
            upload_kwargs = {
                'Config': config,
                'ExtraArgs': {
                    'Metadata': {
                        'artifact_id': obj_id,
                        'atype': 'generic',
                        'created': datetime.datetime.now().isoformat(),
                        'download_url': url,
                        'md5sum': md5sum,
                        'name': obj,
                        'state': 'upload-complete',
                        'upload_id': obj_id,
                        'uri': '/apis/ars/downloads/' + obj_id,
                        'url': url,
                        'version': '1',
                    }
                }
            }
        else:
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
            echo("Unsuccessful upload. Unable to delete object: Error: %s" % delete_err)
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
        output = s3client.delete_object(Bucket=bucket, Key=obj)
        echo(output)
    except (ClientError, s3client.exceptions.NoSuchBucket) as err:
        sys.exit(str(err))
