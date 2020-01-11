from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from django.contrib.auth.models import Group

PREMIUM = Group.objects.get(name='Premium')


class JoinPremium(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

    def get(self, request):
        request.user.groups.add(PREMIUM)
        return Response({'User successfully upgraded to Premium'})


class LeavePremium(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

    def get(self, request):
        request.user.groups.remove(PREMIUM)
        return Response({'User successfully leave Premium'})
