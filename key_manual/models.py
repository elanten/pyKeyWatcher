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
    content = models.TextField(blank=True, default='')

    link = models.URLField(blank=True, default='')
    path = models.FilePathField(path='c:/temp', recursive=True, blank=True, null=True)

    type = models.ForeignKey(ManualType, blank=True, null=True)
    tags = models.ManyToManyField(ManualTag, blank=True, null=True)

    def get_all_tags(self):
        return self.tags.all()

    def __str__(self):
        return self.name
