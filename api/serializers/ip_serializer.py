from rest_framework import serializers


class IpSerializer(serializers.Serializer):
    ip = serializers.CharField(max_length=100)
