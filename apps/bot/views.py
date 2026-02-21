import json
import os

from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import InitDataSerializer
from .models import TelegramUser
from .utils import verify_telegram_data


class JWTTokenGenerator(generics.GenericAPIView):
    serializer_class = InitDataSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        init_data = serializer.validated_data["init_data"]

        is_valid, data = verify_telegram_data(
            init_data,
            os.environ.get("TELEGRAM_BOT_TOKEN")
        )

        if not is_valid:
            raise ValidationError("Invalid Telegram data")

        telegram_user = json.loads(data["user"])
        chat_id = telegram_user["id"]

        bot_user = TelegramUser.objects.select_related("user").filter(
            chat_id=chat_id
        ).first()

        if not bot_user:
            raise ValidationError("Telegram user not registered")

        user = bot_user.user

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
