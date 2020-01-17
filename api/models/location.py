from django.db import models

from django.contrib.postgres.fields import JSONField


class Location(models.Model):
    url = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True, null=True)
    continent_code = models.CharField(max_length=100, blank=True, null=True)
    continent_name = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=100, blank=True, null=True)
    country_name = models.CharField(max_length=100, blank=True, null=True)
    region_code = models.CharField(max_length=100, blank=True, null=True)
    region_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=19, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=19, decimal_places=16, blank=True, null=True)
    location = JSONField(blank=True, null=True)

    class Meta:
        app_label = 'api'
