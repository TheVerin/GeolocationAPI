import json

from rest_framework import mixins, viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from drf_yasg.utils import swagger_auto_schema

from api.models.location import Location
from api.serializers import location_serializer, only_ip_serializer
from api.tools.ipstack_handling import IPStackHandler
from api.permissions.premium_user import PremiumUser


class LocationViewset(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    queryset = Location.objects.all()
    serializer_class = location_serializer.LocationSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    lookup_field = 'ip_with_bars'
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('ip', 'url')
    filterset_fields = ('type', 'continent_name', 'country_name', 'region_name', 'city')

    ipstack_handler = IPStackHandler()

    @swagger_auto_schema(title='create', request_body=only_ip_serializer.OnlyIPSerializer)
    def create(self, request, *args, **kwargs):
        site = request.data['site']

        try:
            location_data = self.ipstack_handler.get_location_data(site=site)
        except Exception:
            return Response('IPStack service not available!', status.HTTP_400_BAD_REQUEST)

        if not location_data:
            return Response('IP does not exists', status.HTTP_400_BAD_REQUEST)

        if Location.objects.filter(ip=location_data['ip']).exists():
            return Response('IP already in db', status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=location_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SecretMessage(APIView):
    permission_classes = (IsAuthenticated, PremiumUser)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        try:
            with open('api/message.json') as json_file:
                data = json.loads(json_file.read())
                return Response(data['message'])
        except FileNotFoundError:
            return Response('If you want to get secret message you need to look for it in api ;)')
