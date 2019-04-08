from datetime import datetime

from upside.enforcer.util.secret import Secret


def get_parameter_tags(client, secret: Secret):
    return client.list_tags_for_resource(ResourceType='Parameter', ResourceId=secret.key)['TagList']


def add_expiration_tag_to_parameter(client, secret: Secret):
    expiring_secret = client.get_parameter(Name=secret.key)
    if expiring_secret:
        # don't update expiration date on already flagged secrets
        for tag in get_parameter_tags(client, secret):
            if 'expiration_date' in tag['Key']:
                return

        client.add_tags_to_resource(
            ResourceType='Parameter', ResourceId=secret.key, Tags=[{
                'Key': 'expiration_date',
                'Value': str(datetime.now())
            }])
        print('Secret: {} expired'.format(secret.key))
    else:
        print('Secret: {} does not exist to be expired.'.format(secret.key))


def add_secret_key_parameter_tags(client, secret: Secret):
    client.add_tags_to_resource(
        ResourceType='Parameter', ResourceId=secret.key, Tags=[{
            'Key': secret.parent_directory,
            'Value': secret.parent_directory
        }, {
            'Key': secret.name,
            'Value': secret.name
        }])
