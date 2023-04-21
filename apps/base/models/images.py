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

    admin_form_fields = Image.admin_form_fields + (
        'alt_text',
        'caption',
    )

    def get_exif_data(self):
        try:
            img = PILImage.open(self.file)
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

            # Todo, futher filter and return only necesary exif data
            return exif_data

        except Exception:
            return None

    def save(self, *args, **kwargs):
        # Call the save() method of the parent class to save the image object
        super(AccessibleImage, self).save(*args, **kwargs)

        # Call the get_exif_data() method to extract Exif data after the image is saved
        if not self.has_exif:
            exif_data = self.get_exif_data()
            print(exif_data)

        # Set the has_exif field based on whether Exif data was extracted
        if exif_data is not None:
            self.has_exif = True
        else:
            self.has_exif = False

        # Save the image object again to update the has_exif field
        super(AccessibleImage, self).save(*args, **kwargs)


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
