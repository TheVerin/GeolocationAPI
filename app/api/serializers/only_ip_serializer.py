from rest_framework import serializers


class OnlyIPSerializer(serializers.Serializer):
    site = serializers.CharField(max_length=100)
