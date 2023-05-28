import io
import json
import boto3
import logging
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from multiprocessing import Pool, cpu_count
from django.db import models
from contextlib import contextmanager
from taggit.models import Tag
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from PIL import Image as PILImage, TiffImagePlugin
from PIL.ExifTags import TAGS

logger = logging.getLogger(__name__)

EXIF_DATA_KEYS = (
    "Make",
    "Flash",
    "Model",
    "Artist",
    "FNumber",
    "DateTime",
    "LensMake",
    "Software",
    "Copyright",
    "LensModel",
    "FocalLength",
    "ExposureTime",
    "ISOSpeedRatings",
    "DateTimeOriginal",
    "ShutterSpeedValue",
)
EXCLUDED_TAGS = (
    'Accessories',
    'Person',
    'Photography',
    'Clothing',
    'Body Part'
)


@contextmanager
def open_file(file):
    try:
        f = file.open('rb')
        yield f
    finally:
        f.close()


rekognition_client = boto3.client(
    'rekognition',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name='us-west-2'
)


def process_image(image):
    if not image.has_exif:
        image.get_exif_data()

    if not image.is_tagged:
        image.tag_image(rekognition_client)


def save_image_and_process(image, rekognition_client):
    image.save(rekognition_client)


class AccessibleImage(AbstractImage):
    """
    Extends the wagtail image model to allow for caption, alt text, extract EXIF data and scan image and tag with AI.
    """
    alt_text = models.TextField(blank=True)
    caption = models.TextField(blank=True)
    is_tagged = models.BooleanField(default=False)
    labels = models.JSONField(default=dict)
    has_exif = models.BooleanField(blank=True, null=True)
    exif_data = models.JSONField(default=dict)
    admin_form_fields = Image.admin_form_fields + (
        'alt_text',
        'caption',
    )

    # Use Pillow to extract camera EXIF data and save to db.
    def get_exif_data(self):
        try:
            with open_file(self.file) as f:
                img = PILImage.open(f)
                dct = {}
                for k, v in img._getexif().items():
                    if k in TAGS and TAGS[k] in EXIF_DATA_KEYS:
                        if isinstance(v, TiffImagePlugin.IFDRational):
                            v = float(v)
                        elif isinstance(v, tuple):
                            v = tuple(
                                float(t) if isinstance(t, TiffImagePlugin.IFDRational) else t for t in v
                            )
                        elif isinstance(v, bytes):
                            v = v.decode(errors="replace")
                        dct[TAGS[k]] = v
                outs = json.dumps(dct)
                exif_data = json.loads(outs)

                self.exif_data = exif_data
                self.has_exif = True
                self.save()

        except IOError as e:
            logger.error("Failed to open image %d: %s", self.id, e)

    # Use AWS Rekognition to scan images and tag automatically
    def tag_image(self, rekognition_client):
        try:
            with open_file(self.file) as f:
                image_data = f.read()

            response = rekognition_client.detect_labels(
                Image={
                    'Bytes': io.BytesIO(image_data).read()
                }
            )

            if "Labels" in response and isinstance(response["Labels"], list) and len(response["Labels"]) > 0:
                tags = [
                    label["Name"] for label in response["Labels"]
                    # xx% confidence or above
                    if label["Confidence"] >= 70.0
                    # Exclude specific tags
                    and label["Name"] not in EXCLUDED_TAGS
                    and not any(parent["Name"] == "Person Description" for parent in label.get("Categories", []))
                    and not any(parent["Name"] == "Apparel and Accessories" for parent in label.get("Categories", []))
                ]

                tag_objs = []
                for tag in tags:
                    tag_obj, created = Tag.objects.get_or_create(
                        name=tag)
                    tag_objs.append(tag_obj)

                self.labels = response
                self.tags.add(*tag_objs)
                self.is_tagged = True
                self.save()

        except Exception as e:
            logger.error(f"Failed to tag image with id {self.id}: {str(e)}")

    def create_renditions(self):
        for filter_spec in ['max-1200x1200', 'max-800x800', 'fill-400x400']:
            rendition = self.get_rendition(filter_spec)
            if rendition is None:
                rendition = self.get_rendition(filter_spec)
                rendition.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.has_exif or not self.is_tagged:
            process_image(self)


@receiver(post_save, sender=AccessibleImage)
def create_renditions(sender, instance, created, **kwargs):
    if created:
        instance.create_renditions()


class AccessibleRendition(AbstractRendition):
    """
    AccessibleRendition Model
    Stores renditions for the custom model.
    """

    image = models.ForeignKey(
        AccessibleImage,
        on_delete=models.CASCADE,
        related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


# Multiprocessing
if __name__ == '__main__':
    images = AccessibleImage.objects.all()

    with Pool(processes=cpu_count()) as pool:
        pool.starmap(save_image_and_process, [
                     (image, rekognition_client) for image in images])
