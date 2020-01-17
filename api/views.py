import os
import logging

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

from api.models.location import Location
from api.serializers import location_serializer, site_serializer, ip_serializer
from api.tools.ipstack_handling import IPStackHandler
from api.permissions.premium_user import PremiumUser
from api.tools.exceptions import IPStackError

logger = logging.getLogger(__name__)


class LocationGet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = Location.objects.all()
    serializer_class = location_serializer.LocationSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('ip',)
    filterset_fields = ('type', 'continent_name', 'country_name', 'region_name', 'city')

    ipstack_handler = IPStackHandler()

    @method_decorator(cache_page(15))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class LocationCreate(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):

    queryset = Location.objects.all()
    serializer_class = site_serializer.SiteSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    ipstack_handler = IPStackHandler()

    def create(self, request, *args, **kwargs):
        site = request.data['site']

        try:
            try:
                location_data = self.ipstack_handler.get_location_data(site=site)
            except ValueError:
                logger.error(f'Site {site} does not exists')
                return Response({'response': 'Site does not exists'}, status.HTTP_400_BAD_REQUEST)
        except IPStackError:
            logger.error('IPStack is not available')
            return Response({'response': 'IPStack service not available'},
                            status.HTTP_400_BAD_REQUEST)

        ip = location_data['ip']

        if Location.objects.filter(ip=ip).exists():
            logger.debug(f"IP {ip} already in db")
            return Response({'response': 'IP already in db'}, status.HTTP_400_BAD_REQUEST)

        serializer = location_serializer.LocationSerializer(data=location_data)

        if serializer.is_valid():
            serializer.save()
            logger.debug(f'{ip} created')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f'Cannot create: {ip}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDelete(mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Location.objects.all()
    serializer_class = ip_serializer.IpSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    lookup_field = 'ip'
    lookup_value_regex = '[0-9.]+'


class SecretMessage(APIView):
    permission_classes = (IsAuthenticated, PremiumUser)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        try:
            logger.debug('Somebody gets secrete message :D')
            return Response({'response': os.environ.get('SECRET_MESSAGE')})

        except FileNotFoundError:
            logger.warning('Somebody wanted to get secret message...')
            return Response({'response': 'If you want to get secret message you need to look for it'
                                         ' in web app ;)'})
