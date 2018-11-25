from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from rest_api.models.User import UserOJAccount
from rest_api.serializers.UserSerializer import LoginSerializer, RegisterSerializer, UserOJAccountSerializer, \
    UserOJAccountListSerializer

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

class BindUserOJAccountView(generics.CreateAPIView,
                        generics.UpdateAPIView,
                        generics.DestroyAPIView,
                        generics.ListAPIView):
    """
    绑定用户OJ账号
    """

    queryset = UserOJAccount
    serializer_class = UserOJAccountSerializer

    def list(self, request, *args, **kwargs):
        queryset = UserOJAccount.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UserOJAccountSerializer(data=request.data["data"], many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "创建成功"}, status=status.HTTP_200_OK)
