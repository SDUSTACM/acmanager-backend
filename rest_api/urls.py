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

from rest_api.views.UserView import LoginView, RegisterView, BindUserOJAccountView, UserProfileView, UserConfirmView

router = SimpleRouter()
router.register('users/profile', UserProfileView, base_name='users-profile')
urlpatterns = [
    path('login/', LoginView.as_view(), name="login-view"),
    path('register/', RegisterView.as_view(), name="register-view"),
    path('account/ojaccount', BindUserOJAccountView.as_view(), name="ojaccount-view"),
    path(r'account/confirm', UserConfirmView.as_view(), name="account-user-confirm-view")

    # path('api/', include('rest_api.urls')),
]
urlpatterns += router.urls