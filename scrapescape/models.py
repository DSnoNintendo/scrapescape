from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.conf import settings
import os

class File(models.Model):
    file = models.FileField(upload_to=os.path.join(MEDIA_ROOT, 'items'))
    format = models.CharField(max_length=255)

    @property
    def relative_path(self):
        return os.path.relpath(self.path, settings.MEDIA_ROOT)