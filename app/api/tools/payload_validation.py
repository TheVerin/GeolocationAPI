class PayloadValidator:

    @staticmethod
    def payload_validation(site):
        site = site.lower()
        is_ip = len(site.split('.'))
        if is_ip == 4 or len(site.split(':')) > 2:
            return [site, 'ip']
        elif site[0] == 'h':
            return [site.split('//')[1], 'url']
        else:
            return [site, 'url']
