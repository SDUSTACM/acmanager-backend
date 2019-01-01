from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets, mixins, views
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from rest_api.models.User import UserProfile, Role
from rest_api.permissions import IsAdminRole
from rest_api.request import send_message
from rest_api.serializers.UserSerializer import LoginSerializer, RegisterSerializer, \
    UserProfileSerializer, ApplicationSerializer, SessionSerializer, UserManagerSerializer, RoleManagerSerializer, \
    RoleListManagerSerializer, RoleCreateUserManagerSerializer, ResetPasswordSerializer

User = get_user_model()
class LoginView(generics.CreateAPIView):
    """
    用户登陆
    """

    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(data={"message": "登陆成功"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "登陆失败"}, status=status.HTTP_403_FORBIDDEN)


class LogoutView(views.APIView):
    """
    用户注销
    """
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SessionView(views.APIView):
    """
    当前用户信息
    """
    permission_classes = (IsAuthenticated, )
    # serializer_class = SessionSerializer
    def get(self, request, *args, **kwargs):
        return Response(data=SessionSerializer(request.user).data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    """
    注册用户
    """
    queryset = User
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "注册成功"}, status=status.HTTP_200_OK)

# class BindUserOJAccountView(generics.CreateAPIView,
#                         generics.UpdateAPIView,
#                         generics.DestroyAPIView,
#                         generics.ListAPIView):
#     """
#     绑定用户OJ账号
#     """
#
#     queryset = UserOJAccount
#     serializer_class = UserOJAccountSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = UserOJAccount.objects.all()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
#
#     def post(self, request, *args, **kwargs):
#         serializer = UserOJAccountSerializer(data=request.data["data"], many=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data={"message": "创建成功"}, status=status.HTTP_200_OK)


class UserProfileView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    lookup_field = "username"
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        user = self.get_queryset().get(username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = self.get_queryset().get(username=request.user.username)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "更新成功"}, status=status.HTTP_200_OK)

class ApplicationView(APIView):
    def get(self, request, *args, **kwargs):
        application_type = kwargs.get("type")
        if application_type not in Role.ROLE_IDENTIFIER_TYPE:
            return Response(data={"message" : "角色不合法"}, status=status.HTTP_400_BAD_REQUEST)
        # seriailzer = ApplicationSerializer(data=request.data)
        send_message(from_user=request.user, to_role="ADMIN", verb="APPLICATION", obj=application_type)
        # seriailzer.is_valid(raise_exception=True )
        # seriailzer.save()
        return Response(data={"message": "操作成功"}, status=status.HTTP_201_CREATED)


class UserManagerView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserManagerSerializer
    permission_classes = (IsAuthenticated, IsAdminRole)


class RoleManagerView(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Role.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListManagerSerializer
        elif self.action == 'add_user' or self.action == 'remove_user':
            return RoleCreateUserManagerSerializer
        else:
            return RoleManagerSerializer
    # permission_classes = (IsAuthenticated)

    @action(detail=True, methods=['post'])
    def add_user(self, request, pk=None):
        role = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            role.user.add(serializer.validated_data['user'])
            role.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_user(self, request, pk=None):
        role = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            role.user.remove(serializer.validated_data['user'])
            role.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.CreateAPIView):
    queryset = User
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)