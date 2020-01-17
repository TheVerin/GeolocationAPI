from ipstack import GeoLookup

from django.conf import settings

from api.tools.exceptions import IPStackError


class IPStackHandler:

    def get_location_data(self, site):
        if not site:
            raise ValueError

        site_type = self.payload_validation(site)

        try:
            geo_lookup = GeoLookup(settings.IPSTACK_KEY)
        except Exception:
            raise IPStackError('IPStack does not response')

        data = geo_lookup.get_location(site_type[0])

        if site_type[1] == 'url':
            data['url'] = site_type[0]

        if not data['continent_name'] and not data['country_name'] and not data['region_name']:
            raise ValueError
        else:
            return data

    @staticmethod
    def payload_validation(site):
        site = site.lower()
        if len(site.split('.')) == 4 or len(site.split(':')) > 2:
            return [site, 'ip']
        elif site.startswith('http') or site.startswith('https'):
            return [site.split('//')[1], 'url']
        else:
            return [site, 'url']
