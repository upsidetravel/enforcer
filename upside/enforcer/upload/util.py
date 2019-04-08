import re
from collections import defaultdict

from botocore import exceptions

from upside.enforcer.upload.chunks import adjust_chunk_size, chunk_secret_value
from upside.enforcer.util.secret import Secret
from upside.enforcer.util.tags import add_expiration_tag_to_parameter, add_secret_key_parameter_tags


def put_parameter(client, secret: Secret, kms_key_id):
    if kms_key_id:
        client.put_parameter(
            Name=secret.key,
            Description=secret.parent_directory + ' secrets',
            Value=secret.value,
            Type='SecureString',
            KeyId=kms_key_id,
            Overwrite=True)
    else:
        #  Uses aws default kms if a custom one is not provided. The system automatically populates Key ID with your default KMS key.
        client.put_parameter(
            Name=secret.key,
            Description=secret.parent_directory + ' secrets',
            Value=secret.value,
            Type='SecureString',
            Overwrite=True)
    add_secret_key_parameter_tags(client, secret)


def upload_secret(client, kms_key_id, secret: Secret):
    store = None
    try:
        # Check if chunks exist for secret, then secret_chunk_000 supercedes secret for history auditing
        # Handles case when a secrets value reduces < 2 chunks over time
        store = lookup_existing_chunked_secrets(client, secret)
        if not store:
            put_parameter(client, secret, kms_key_id)
        else:
            upload_chunked_secret(client, secret, store, kms_key_id)
    except exceptions.ClientError as err:
        if 'length less than or equal to 4096' in err.response['Error']['Message']:
            upload_chunked_secret(client, secret, store, kms_key_id)
        else:
            raise err


def upload_chunked_secret(client, secret: Secret, store, kms_key_id):
    chunks = chunk_secret_value(secret.value, 4095)
    if store:
        chunks = adjust_chunk_size(chunks, store)
        # deprecate old secret if secret becomes secret_chunk_0 + secret_chunk_1
        add_expiration_tag_to_parameter(client, secret)

    for idx, chunk in enumerate(chunks):
        chunked_secret = Secret(key=secret.key + '_chunk_' + "{:03d}".format(idx), value=chunk)

        print(chunked_secret.key)
        put_parameter(client, chunked_secret, kms_key_id)


def add_existing_chunks_to_secret_store(existing_secrets, store, upload_secret: Secret):
    for existing_secret in existing_secrets['Parameters']:
        existing_chunked_secret = Secret(key=existing_secret['Name'], value=existing_secret['Value'])

        if upload_secret.name + '_chunk_' in existing_chunked_secret.name:
            store[existing_chunked_secret.name] = existing_chunked_secret.value


def lookup_existing_chunked_secrets(client, secret: Secret):
    store = defaultdict(dict)

    existing_secrets = client.get_parameters_by_path(
        Path='/' + secret.parent_directory,
        Recursive=True,
        WithDecryption=True)
    add_existing_chunks_to_secret_store(existing_secrets, store, secret)
    if len(existing_secrets['Parameters']) and 'NextToken' in existing_secrets:
        # if there are greater than 10 secrets in the directory keep fetching
        while 'NextToken' in existing_secrets:
            existing_secrets = client.get_parameters_by_path(
                Path='/' + secret.parent_directory,
                Recursive=True,
                WithDecryption=True,
                NextToken=existing_secrets['NextToken'])
            add_existing_chunks_to_secret_store(existing_secrets, store, secret)
        else:
            # update store with the last pagination request
            add_existing_chunks_to_secret_store(existing_secrets, store, secret)

    return store


def secret_key_pattern(value):
    if not re.match("^\/[a-zA-Z0-9._-]+\/[a-zA-Z0-9._-]+$", value):  # noqa: W605
        raise ValueError(value)
    else:
        return value
