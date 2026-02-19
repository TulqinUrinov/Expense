import jwt
from django.conf import settings
from django.http import JsonResponse

from apps.bot.models import TelegramUser
from apps.user.models import User


class TelegramUserJWTMiddleware:

    def __init__(self, get_response):
        self.get_repsonse = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = None

        request.bot_user = None

        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

                bot_user_id = payload.get("bot_user_id")
                user_id = payload.get("user_id")

                if bot_user_id:
                    request.bot_user = TelegramUser.objects.filter(id=bot_user_id).first()

                if user_id:
                    request.user = User.objects.filter(id=user_id).first()


            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expired"}, status=401)
            except jwt.DecodeError:
                return JsonResponse({"error": "Invalid token"}, status=401)

        return self.get_repsonse(request)
