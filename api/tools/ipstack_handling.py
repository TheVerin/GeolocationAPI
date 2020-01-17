import logging

from ipstack import GeoLookup

from django.conf import settings

from api.tools.exceptions import IPStackError

logger = logging.getLogger(__name__)


class IPStackHandler:

    def get_location_data(self, site):
        if not site:
            logger.error(f'{site} cannot be empty')
            raise ValueError

        site_type = self.payload_validation(site)

        try:
            geo_lookup = GeoLookup(settings.IPSTACK_KEY)
            logger.debug('GeoLookup connection established')
        except Exception:
            logger.error('IPStack does not response')
            raise IPStackError('IPStack does not response')

        data = geo_lookup.get_location(site_type)

        if not data['continent_name'] and not data['country_name'] and not data['region_name']:
            logger.error(f'Site {site_type} does not exist')
            raise ValueError
        else:
            logger.debug(f'Site {site_type} exists')
            return data

    @staticmethod
    def payload_validation(site):

        if type(site) != str:
            logger.error(f'Not valid data type. Expected: string, received {type(site)}')
            raise TypeError

        site = site.lower()
        if site.startswith('http') or site.startswith('https'):
            return site.split('//')[1]
        else:
            return site
