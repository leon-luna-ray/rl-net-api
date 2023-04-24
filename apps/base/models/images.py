import json
from django.db import models
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from PIL import Image as PILImage, TiffImagePlugin
from PIL.ExifTags import TAGS


class AccessibleImage(AbstractImage):
    """
    Adds extra fields to wagtail image model.
    """
    alt_text = models.TextField(blank=True)
    caption = models.TextField(blank=True)
    has_exif = models.BooleanField(blank=True, null=True)
    exif_data = models.JSONField(default=dict)
    admin_form_fields = Image.admin_form_fields + (
        'alt_text',
        'caption',
    )

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

    def save(self, *args, **kwargs):
        # Call the save() method of the parent class to save the image object
        super(AccessibleImage, self).save(*args, **kwargs)

        # Call the get_exif_data() method to extract Exif data after the image is saved
        if not self.has_exif:
            self.get_exif_data()


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
