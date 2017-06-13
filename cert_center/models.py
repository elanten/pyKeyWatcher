from django.db import models


# Create your models here.
class CertificationCenter(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CertRequirement(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    actual_date = models.DateField(blank=True, null=True)
    center = models.ForeignKey(CertificationCenter)

    def __str__(self):
        return self.name
