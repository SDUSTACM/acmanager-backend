from django.urls import path

from notification.views import NotificationView, NotificationCreateView, NotificationMarkReadView, \
    NotificationMarkUnReadView, NotificationOperatorView, NotificationDetailView

urlpatterns = [
    path('all/<username>', NotificationView.as_view(), name='notifications-list'),
    path('detail/<pk>', NotificationDetailView.as_view(), name='notifications-list'),
    path('create/', NotificationCreateView.as_view(), name='notifications-create'),
    # path('application/', NotificationApplicationCreateView, name='notifications-application-create'),
    path('mark_read/<id>', NotificationMarkReadView.as_view(), name='notifications-create'),
    path('mark_unread/<id>', NotificationMarkUnReadView.as_view(), name='notifications-create'),
    path('operator/<pk>', NotificationOperatorView.as_view(), name='notifications-create'),
    # path('api/', include('rest_api.urls')),
]