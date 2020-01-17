from rest_framework import serializers


class SiteSerializer(serializers.Serializer):
    site = serializers.CharField(max_length=100)
