from django.db import models

from django.contrib.postgres.fields import JSONField


class Location(models.Model):
    ip = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    continent_code = models.CharField(max_length=100, blank=True)
    continent_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=100, blank=True)
    country_name = models.CharField(max_length=100)
    region_code = models.CharField(max_length=100, blank=True)
    region_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=19, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=19, decimal_places=16, blank=True, null=True)
    location = JSONField(blank=True, null=True)

    class Meta:
        app_label = 'api'
