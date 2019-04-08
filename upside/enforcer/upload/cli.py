"""
Script to upload secrets to AWS SSM Parameter Store and tag them appropriately
This script will read your secret value from the clipboard automagically
"""

import click
import pyperclip
from colorama import init, Fore

from upside.enforcer.upload.util import upload_secret, secret_key_pattern
from upside.enforcer.util.auth import session
from upside.enforcer.util.secret import Secret

init(autoreset=True)


def secret_key_pattern_check(ctx, param, value):
    try:
        return secret_key_pattern(value)
    except ValueError as e:
        print(Fore.RED + 'Incorrect secret key syntax: {}'.format(e))
        value = click.prompt(param.prompt)
    return secret_key_pattern_check(ctx, param, value)


@click.command()
@click.option('--profile', default=None, help='aws profile')
@click.option('--region', default=None, help='aws region name')
@click.option(
    '--fq_secret_key',
    prompt='Fully Qualified Secret Key [/secret_directory/secret_name]',
    callback=secret_key_pattern_check,
    help='Fully qualified secret e.g /secret_directory/secret_name')
@click.option('--secret_value', prompt='Copy your secret value to the clipboard then press enter', default='', show_default=False, hide_input=False)
@click.option('-k', '--kms_key_id', default=None, help='alias of the AWS KMS Parameter Store Key used to encrypt secrets')
@click.option('-f', '--force', flag_value=True, help='skip confirmation prompt')
def upload(profile, region, fq_secret_key, secret_value, kms_key_id, force):
    client = session(profile, region).client('ssm')

    if not secret_value:
        secret_value = pyperclip.paste()

    print('\nRegion: ' + Fore.GREEN + (region or client.meta.region_name))

    if profile:
        print('Profile: ' + Fore.GREEN + profile)
    if kms_key_id:
        kms_key_id = 'alias/{}'.format(kms_key_id)
        print('AWS KMS: ' + Fore.GREEN + kms_key_id)
    print('Secret Key: ' + Fore.GREEN + fq_secret_key)
    print('Secret Value:')
    print(Fore.GREEN + secret_value + '\n')
    if not force:
        confirm = click.confirm('Does this look correct?')
    else:
        confirm = True

    if confirm:
        upload_secret(client, kms_key_id, Secret(key=fq_secret_key, value=secret_value))
        print(Fore.GREEN + 'Uploaded successfully!')
