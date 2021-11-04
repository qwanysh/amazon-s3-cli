import argparse
import os

import boto3
from botocore.exceptions import ClientError

import config

s3_client = boto3.client(
    service_name='s3',
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        type=action_type,
        help=f"action({', '.join(actions)}) to perform",
    )
    parser.add_argument(
        'file_name',
        type=file_name_type,
        help='file to upload',
    )
    parser.add_argument(
        '-k',
        '--key',
        help='S3 key to upload. If not specified then file_name is used',
    )
    return parser.parse_args()


def get_file_extension(file_name):
    _, extension = os.path.splitext(file_name)
    return extension


def get_content_type(file_name):
    content_types = {'.svg': 'image/svg+xml'}
    return content_types.get(get_file_extension(file_name))


def upload(args):
    extra_args = {}
    content_type = get_content_type(args.file_name)

    if content_type:
        extra_args['ContentType'] = content_type

    try:
        s3_client.upload_file(
            args.file_name,
            config.AWS_BUCKET,
            args.key or args.file_name,
            ExtraArgs=extra_args,
        )
    except ClientError as e:
        print(e)


actions = {'upload': upload}


def action_type(value):
    if value in actions:
        return value

    raise argparse.ArgumentTypeError(f"use one of ({', '.join(actions)})")


def file_name_type(value):
    if os.path.isfile(value):
        return value

    raise argparse.ArgumentTypeError(f'"{value}" file does not exist')


def confirm_action():
    confirmation = input(f'Using {config.AWS_BUCKET} bucket. Y/N? ')
    return confirmation.lower() == 'y'


def main():
    args = get_args()

    if confirm_action():
        actions[args.action](args)


if __name__ == '__main__':
    main()
