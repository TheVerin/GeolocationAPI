from ipstack import GeoLookup

from django.conf import settings


class IPStackHandler:

    def get_location_data(self, site):
        if not site:
            return False

        site_type = self._payload_validation(site)
        geo_lookup = GeoLookup(settings.IPSTACK_KEY)

        data = geo_lookup.get_location(site_type[0])

        data['ip_with_bars'] = '_'.join(data['ip'].split('.'))
        data['ip_with_bars'] = '_'.join(data['ip_with_bars'].split(':'))

        if site_type[1] == 'url':
            data['url'] = site_type[0]

        if not data['continent_name'] and not data['country_name'] and not data['region_name']:
            return False
        else:
            return data

    @staticmethod
    def _payload_validation(site):
        site = site.lower()
        if len(site.split('.')) == 4 or len(site.split(':')) > 2:
            return [site, 'ip']
        elif site.startswith('http') or site.startswith('https'):
            return [site.split('//')[1], 'url']
        else:
            return [site, 'url']
