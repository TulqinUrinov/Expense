from django.urls import path
from apps.user.views import UserAPIView

urlpatterns = [
    path('info/', UserAPIView.as_view(), name='info'),
]
