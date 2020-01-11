class PayloadValidator:

    @staticmethod
    def payload_validation(site):
        site = site.lower()
        if len(site.split('.')) == 4 or len(site.split(':')) > 2:
            return [site, 'ip']
        elif site.startswith('http') or site.startswith('https'):
            return [site.split('//')[1], 'url']
        else:
            return [site, 'url']
