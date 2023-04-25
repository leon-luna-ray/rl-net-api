from django.core.management.base import BaseCommand, CommandError
import boto3

class Command(BaseCommand):
    """ Test Command for extracting image labels with AI and tagging image automatically upon upload to Wagtail"""
    def handle(self, *args, **options):
        print('Calling AWS Rekognition 🤖')

        client = boto3.client('rekognition', region_name='us-west-2')

        response = client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': 'rlp-www-media-store',
                    # This will be the file name in the s3 bucket
                    'Name': f'media/original_images/Cancun-22-069.jpg',
                }
            }
        )
        print(response)


