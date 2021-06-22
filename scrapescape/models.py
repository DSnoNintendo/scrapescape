from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.conf import settings
import os

class Search(models.Model):
    keyword = models.CharField(max_length=100)
    output = models.IntegerField()

class Stats(models.Model):
    num_searches = models.IntegerField()
    num_scraped = models.IntegerField()