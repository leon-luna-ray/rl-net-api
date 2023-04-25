from django.core.management.base import BaseCommand, CommandError
import boto3

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Calling AWS Rekognition 🤖')

        # image_file = options['image_file']

        client = boto3.client('rekognition', region_name='us-west-2')

        response = client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': 'rlp-www-media-store',
                    'Name': f'media/original_images/Cancun-22-069.jpg',
                }
            }
        )
        print(response)


