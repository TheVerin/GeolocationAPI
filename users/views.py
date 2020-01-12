from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from django.contrib.auth.models import Group


class JoinPremium(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

    @staticmethod
    def get(request):
        premium_group = Group.objects.get(name='Premium')
        request.user.groups.add(premium_group)
        return Response({'User successfully upgraded to Premium'})


class LeavePremium(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

    @staticmethod
    def get(request):
        premium_group = Group.objects.get(name='Premium')
        request.user.groups.remove(premium_group)
        return Response({'User successfully leave Premium'})
