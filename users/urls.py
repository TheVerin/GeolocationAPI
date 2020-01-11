from django.urls import path, include
from .views import JoinPremium, LeavePremium

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('join/', JoinPremium.as_view(), name='join'),
    path('leave/', LeavePremium.as_view(), name='leave')
]
