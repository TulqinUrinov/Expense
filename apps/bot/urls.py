from django.urls import path
from apps.bot.views import JWTTokenGenerator

urlpatterns = [
    path('access/', JWTTokenGenerator.as_view(), name="access"),
]
