"""acmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from rest_api.views.NotificationView import MessageView, VerifyView
from rest_api.views.UserView import LoginView, RegisterView, UserProfileView, ApplicationView, \
    SessionView, LogoutView, UserManagerView, RoleManagerView
from rest_api.views.TrainingView import TrainingView, TrainingStageView, StageContestView

router = routers.SimpleRouter()
# router.register('users/profile', UserProfileView, base_name='users-profile')
router.register('trainings', TrainingView, base_name='training-view')
# router.register('stages', StageView, base_name='stage-view')


training_router = routers.NestedSimpleRouter(router, r'trainings', lookup='training')
training_router.register(r'stages', TrainingStageView, base_name='training-stage-view')

stage_router = routers.NestedSimpleRouter(training_router, r'stages', lookup='stage')
stage_router.register(r'contests', StageContestView, base_name='training-stage-contest-view')

admin_router = routers.SimpleRouter()
admin_router.register(r'users', UserManagerView, base_name="user-manager-view")
admin_router.register(r'roles', RoleManagerView, base_name="role-manager-view")

user_router = routers.SimpleRouter()
user_router.register(r'profile', UserProfileView, base_name="user-profile-view")

urlpatterns = [
    # path('notifications/', live_all_notification_list, name='notifications'),
    path('admin/', include(admin_router.urls)),
    path('user/', include(user_router.urls)),
    path('login/', LoginView.as_view(), name="login-view"),
    path('logout/', LogoutView.as_view(), name="logout-view"),
    path('session/', SessionView.as_view(), name="session-view"),
    path('register/', RegisterView.as_view(), name="register-view"),
    path(r'application/<type>/', ApplicationView.as_view(), name="account-user-confirm-view"),
    path(r'verify/<pk>/', VerifyView.as_view(), name="verify-view"),
    path(r'message/', MessageView.as_view(), name="message-view"),
    path(r'crawl/', include("crawl.urls"))

    # path('api/', include('rest_api.urls')),
]
urlpatterns += router.urls
urlpatterns += training_router.urls
urlpatterns += stage_router.urls