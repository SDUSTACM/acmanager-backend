from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import viewsets
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.models import Notification, NotificationOperatorStatus, NotificationBase
from notification.serializers import NotificationSerializer, NotificationCreateSerializer, \
    NotificationOperatorStatusSerializer


class NotificationView(generics.ListAPIView):
    def get_queryset(self):
        return Notification.objects.filter(to_user=self.request.user)

    serializer_class = NotificationSerializer


class NotificationCreateView(generics.CreateAPIView):
    def get_queryset(self):
        return Notification.objects.filter(to_user=self.request.user)

    serializer_class = NotificationCreateSerializer

class NotificationMarkReadView(APIView):
    def post(self, *args, **kwargs):
        id = kwargs.get("id")
        notification = Notification.objects.get(id=id)
        notification.is_read = True
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationMarkUnReadView(APIView):
    def post(self, *args, **kwargs):
        id = kwargs.get("id")
        notification = Notification.objects.get(id=id)
        notification.is_read = False
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationOperatorView(generics.UpdateAPIView):
    def get_queryset(self):
        return NotificationOperatorStatus.objects.all()

    lookup_url_kwarg = "pk"
    lookup_field = "notification__id"
    serializer_class = NotificationOperatorStatusSerializer

    def perform_update(self, serializer):
        serializer.save(notification=NotificationBase.objects.get(id=self.kwargs["pk"]))
