import os

import boto3


def session(profile=None, region=None):
    if profile and region:
        return boto3.Session(profile_name=profile, region_name=region)
    elif os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
        return boto3.Session(aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    elif os.environ.get('AWS_PROFILE') and os.environ.get('AWS_DEFAULT_REGION'):
        return boto3.Session(profile_name=os.environ.get('AWS_PROFILE'), region_name=os.environ.get('AWS_DEFAULT_REGION'))
