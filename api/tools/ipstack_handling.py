from ipstack import GeoLookup

from django.conf import settings

from rest_framework.status import HTTP_404_NOT_FOUND

from .payload_validation import PayloadValidator


class IPStackHandler:

    def __init__(self):
        self.validator = PayloadValidator()

    def get_location_data(self, site):
        if site == '':
            return HTTP_404_NOT_FOUND

        site_type = self.validator.payload_validation(site)
        geo_lookup = GeoLookup(settings.IPSTACK_KEY)

        data = geo_lookup.get_location(site_type[0])

        data['ip_with_bars'] = '_'.join(data['ip'].split('.'))
        data['ip_with_bars'] = '_'.join(data['ip_with_bars'].split(':'))

        if site_type[1] == 'url':
            data['url'] = site_type[0]

        if site_type[1] == 'null':
            return HTTP_404_NOT_FOUND

        if not data['continent_name'] and not data['country_name'] and not data['region_name']:
            return HTTP_404_NOT_FOUND
        else:
            return data


