import click

from upside.enforcer.upload.cli import upload


@click.group(commands={'upload': upload}, help='UPLOAD - uploads secrets to AWS parameter store.')
def enforcer():
    pass


if __name__ == '__main__':
    enforcer()
