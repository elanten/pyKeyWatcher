import os

from django.db import models


# Create your models here.

class ManualType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class ManualTag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Manual(models.Model):
    name = models.CharField(max_length=255)
    name_full = models.CharField(max_length=255, blank=True, default='')

    content = models.TextField(blank=True, default='')

    link = models.URLField(blank=True, default='')
    path = models.FilePathField(
        path='/path_to_manuals/', match='\.(?:pdf|doc|docx|xls|xlsx)$',
        recursive=True, blank=True, null=True)

    type = models.ForeignKey(ManualType, blank=True, null=True)
    tags = models.ManyToManyField(ManualTag, blank=True)

    def get_all_tags(self):
        return self.tags.all()

    def __str__(self):
        return self.name
