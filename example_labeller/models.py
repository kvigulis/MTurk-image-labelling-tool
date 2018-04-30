from django.db import models
import os
from image_labelling_tool import models as lt_models

# Create your models here.
class ImageWithLabels (models.Model):
    # image
    image = models.ImageField(blank=True)

    # labels
    labels = models.OneToOneField(lt_models.Labels, related_name='image', on_delete=models.CASCADE)

    def __str__(self):
        #
        return str((self.image))[2:]

    def filename(self):
        return os.path.basename(self.image.name)