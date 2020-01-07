from ipstack import GeoLookup

from django.conf import settings

from rest_framework.status import HTTP_404_NOT_FOUND


def get_location_data(site):
    geo_lookup = GeoLookup(settings.IPSTACK_KEY)
    data = geo_lookup.get_location(site)
    if data['ip'] == site:
        return HTTP_404_NOT_FOUND
    else:
        return data
