from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_api.models.User import Role
from rest_api.request import get_all_notifications, send_operator, get_notification
from django.contrib.auth import get_user_model

from rest_api.serializers.NotificationSerializer import VerifySerializer

User = get_user_model()


class MessageView(APIView):
    def get(self, request):
        return Response(data=get_all_notifications(request.user.username))


class VerifyView(generics.CreateAPIView):
    serializer_class = VerifySerializer

    def create(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        notification = get_notification(pk)
        if not notification:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = request.data

        if notification["object"].upper() == "CONFIRM" and data["status"] == "AGREE":
            Role.objects.get(identifier="CONFIRM").user.add(User.objects.get(username=notification["from_user"]))
        send_operator(notification["base_id"], data["status"])
        # 当无返回体时，返回状态码必须是204
        return Response(status=status.HTTP_204_NO_CONTENT)
