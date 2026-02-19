from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.serializers import UserSerializer
from apps.common.custom_permission import IsAuthenticatedUser


class UserAPIView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
