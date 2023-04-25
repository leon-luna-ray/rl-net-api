import json
import boto3
from django.db import models
from taggit.models import Tag
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from PIL import Image as PILImage, TiffImagePlugin
from PIL.ExifTags import TAGS


class AccessibleImage(AbstractImage):
    """
    Extends the wagtail image model to allow for caption, alt text, extract EXIF data and scan image and tag with AI.
    """
    alt_text = models.TextField(blank=True)
    caption = models.TextField(blank=True)
    is_tagged = models.BooleanField(default=False)
    has_exif = models.BooleanField(blank=True, null=True)
    exif_data = models.JSONField(default=dict)
    admin_form_fields = Image.admin_form_fields + (
        'alt_text',
        'caption',
    )

    # Use Pillow to extract camera EXIF data and save to db.
    def get_exif_data(self):
        try:
            with self.file.open('rb') as f:
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
            print("Failed to open image: %s" % e)

    # Use AWS Rekognition to scan images and tag automatically
    def tag_image(self):
        client = boto3.client('rekognition', region_name='us-west-2')
        image_data = self.file.read()

        print('📡 Calling AWS Rekognition...')

        response = client.detect_labels(
            Image={
                'Bytes': image_data
            }
        )

        if response:
            tags = [label["Name"] for label in response["Labels"]]

            tag_objs = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(
                    name=tag.strip('\"'))
                tag_objs.append(tag_obj)

            self.tags.add(*tag_objs)
            self.is_tagged = True
            self.save()

            print('💾 Rekognition data saved!')

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
