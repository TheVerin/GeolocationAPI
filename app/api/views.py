from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from .models.location import Location
from .serializers import location_serializer, only_ip_serializer
from .tools.ipstack_handling import IPStackHandler


class LocationViewset(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    queryset = Location.objects.all()
    serializer_class = location_serializer.LocationSerializer

    ipstack_handler = IPStackHandler()

    @swagger_auto_schema(title='create', request_body=only_ip_serializer.OnlyIPSerializer)
    def create(self, request, *args, **kwargs):
        site = request.data['site']

        location_data = self.ipstack_handler.get_location_data(site=site)

        if location_data == status.HTTP_404_NOT_FOUND:
            return Response('Movie does not exists', status.HTTP_400_BAD_REQUEST)

        if Location.objects.filter(ip=location_data['ip']).exists():
            return Response('IP already in db', status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=location_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(title='delete_ip', request_body=only_ip_serializer.OnlyIPSerializer)
    @action(detail=False, methods=['DELETE'])
    def delete_ip(self, request):
        Location.objects.filter(site=request.data['site']).delete()
        return Response(f"Record {request.data['site']} deleted")
