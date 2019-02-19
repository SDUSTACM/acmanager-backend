from django.contrib.auth import get_user_model
from rest_framework import viewsets

from rest_api.models.Model import Announcement
from rest_api.serializers.Serializer import AnnouncementSerializer, AnnouncementListSerializer

User = get_user_model()


class AnnouncementView(viewsets.ModelViewSet):
    """
    公告视图
    """
    queryset = Announcement.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AnnouncementListSerializer
        else:
            return AnnouncementSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
