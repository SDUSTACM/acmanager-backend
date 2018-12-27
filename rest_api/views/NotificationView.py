from rest_framework.response import Response
from rest_framework.views import APIView

from rest_api.request import get_all_notifications


class MessageView(APIView):
    def get(self, request):
        return Response(data=get_all_notifications(request.user.username))