from django.shortcuts import render, get_object_or_404
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
        return Notification.objects.filter(to_user__username=self.kwargs["username"])

    serializer_class = NotificationSerializer


class NotificationDetailView(generics.RetrieveAPIView):
    queryset = Notification
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


class NotificationOperatorView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return NotificationBase.objects.all()

    serializer_class = NotificationOperatorStatusSerializer

    def put(self, request, *args, **kwargs):
        notification = self.get_object()
        # notification = NotificationBase.objects.get(id=self.kwargs["pk"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(notification=notification)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        notification = self.get_object()
        instance = get_object_or_404(NotificationOperatorStatus, notification=notification)
        # notification = NotificationBase.objects.get(id=self.kwargs["pk"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        notification = self.get_object()
        instance = get_object_or_404(NotificationOperatorStatus, notification=notification)
        # notification = NotificationBase.objects.get(id=self.kwargs["pk"])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)