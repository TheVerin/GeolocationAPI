from rest_framework import serializers

from ..models import Location


class LocationSerializer(serializers.ModelSerializer):
    ip = serializers.IPAddressField()

    class Meta:
        model = Location
        fields = ('ip', 'type', 'continent_code', 'continent_name', 'country_code', 'country_name',
                  'region_code', 'region_name', 'city', 'zip', 'latitude', 'longitude', 'location')
