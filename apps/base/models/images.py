import io
import json
import boto3
import logging

from django.db import models
from contextlib import contextmanager
from taggit.models import Tag
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from PIL import Image as PILImage, TiffImagePlugin
from PIL.ExifTags import TAGS

logger = logging.getLogger(__name__)

# Define context manager for file access


@contextmanager
def open_file(file):
    try:
        f = file.open('rb')
        yield f
    finally:
        f.close()


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
                    if k in TAGS:
                        if isinstance(v, TiffImagePlugin.IFDRational):
                            v = float(v)
                        elif isinstance(v, tuple):
                            v = tuple(float(t) if isinstance(
                                t, TiffImagePlugin.IFDRational) else t for t in v)
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
    def tag_image(self):
        try:
            client = boto3.client('rekognition', region_name='us-west-2')

            with open_file(self.file) as f:
                image_data = f.read()

            response = client.detect_labels(
                Image={
                    'Bytes': io.BytesIO(image_data).read()
                }
            )

            if "Labels" in response and isinstance(response["Labels"], list) and len(response["Labels"]) > 0:
                tags = [label["Name"] for label in response["Labels"] if label["Confidence"] >= 90.0]
                print(response)
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

    def save(self, *args, **kwargs):
        super(AccessibleImage, self).save(*args, **kwargs)

        if not self.has_exif:
            self.get_exif_data()

        if not self.is_tagged:
            self.tag_image()


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
