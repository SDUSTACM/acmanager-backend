from collections import OrderedDict
from django.contrib.auth import authenticate
from rest_framework import serializers

from django.contrib.auth import get_user_model

from rest_api.models.User import UserProfile, Role

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class RoleField(serializers.Field):
    def to_representation(self, value):
        return [item.identifier for item in value.all()]

class SessionSerializer(serializers.ModelSerializer):
    nick = serializers.CharField(source="profile.nick", read_only=True)
    roles = RoleField()

    class Meta:
        model = User
        fields = ('username', 'nick', 'roles')


class IsConfirmField(serializers.Field):
    def to_representation(self, value):
        is_confirm = Role.objects.get(identifier="CONFIRM").user.filter(username=value).exists()
        return is_confirm

    def to_internal_value(self, data):
        pass


class UserProfileSerializer(serializers.ModelSerializer):
    is_confirm = IsConfirmField(source="username", read_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', "nick", "class_name", "is_confirm", "email")
        extra_kwargs = {
            'username': {'read_only': True},
            'is_confirm': {'read_only': True},
            'email': {'allow_blank': True},
            # 'phone': {'read_only': False},
            # 'qq': {'read_only': False},
            # 'nick': {'read_only': False},
        }


class RegisterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    def create(self, validated_data):
        user = User()
        user.username = validated_data["username"]
        user.set_password(validated_data["password"])
        profile = validated_data.get("profile", None)
        user_profile = UserProfile()
        user_profile.username = validated_data["username"]
        user_profile.nick = validated_data["username"]
        if profile:
            user_profile.email = profile.get("email", None)
            user_profile.qq = profile.get("qq", None)
            user_profile.phone = profile.get("phone", None)
            user_profile.nick = profile.get("nick", validated_data["username"])
            user_profile.class_name = profile.get("class_name", None)
        user.save()
        user_profile.user = user
        user_profile.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'profile')


# class UserOJAccountListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         books = [UserOJAccount(**item) for item in validated_data]
#         return UserOJAccount.objects.bulk_create(books)
#
#
# class UserOJAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserOJAccount
#         fields = '__all__'
#         list_serializer_class = UserOJAccountListSerializer
#         extra_kwargs = {'oj_password': {'required': False}}


class ApplicationSerializer(serializers.Serializer):
    def validate_identifier(self, value):
        if value.upper() not in Role.ROLE_IDENTIFIER_TYPE:
            raise serializers.ValidationError("申请的类型有误")
        return value

    username = serializers.CharField(max_length=20)
    identifier = serializers.CharField(max_length=20)

    def create(self, validated_data):
        # Role.ROLE_IDENTIFIER_TYPE.CONFIRM
        # user = User.objects.get(username=validated_data["username"])
        # expected_role = Role.objects.get(identifier=validated_data["identifier"].upper())
        # if expected_role not in user.roles.all():
        #     user.roles.add(expected_role)
        return user
#
# class UserRoleSerializer(serializers.ModelSerializer):
#     roles = serializers.SlugRelatedField(slug_field='identifier', queryset=Role.objects.all())
#
#     class Meta:
#         model = User
#         fields = ('roles', )
#
#     def to_representation(self, instance):
#         ret = super().to_representation(instance)
#         return ret["roles"]
#
#     def to_internal_value(self, data):
#         super().to_internal_value(data)
class RoleField(serializers.Field):
    def to_internal_value(self, data):
        super().to_internal_value(data)

    def to_representation(self, value):
        super().to_representation(value)


class UserManagerSerializer(serializers.ModelSerializer):

    roles = serializers.ListField(source="user.roles.all",
        child=serializers.SlugRelatedField(slug_field="identifier", queryset=Role.objects.all())
                                  )
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'nick', 'class_name', 'roles')
        extra_kwargs = {
            "id": {
                "read_only": True
            }
        }

    def update(self, instance, validated_data):
        userprofile = instance
        userprofile.username = validated_data.get("username")
        userprofile.nick = validated_data.get("nick")
        userprofile.class_name = validated_data.get("class_name")
        user = validated_data.get("user")
        userprofile.user.roles.set(user["roles"]["all"])
        userprofile.save()
        return userprofile


class RoleListManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = ('user',)


class RoleManagerSerializer(serializers.ModelSerializer):
    user = serializers.ListSerializer(
        child=serializers.SlugRelatedField(slug_field="username", read_only=True)
    )

    class Meta:
        model = Role
        fields = '__all__'


class RoleCreateUserManagerSerializer(serializers.Serializer):
    """
    角色添加/删除用户序列化器
    """
    user = serializers.CharField(max_length=20)

    def to_internal_value(self, data):
        ret = OrderedDict()
        ret["user"] = User.objects.get(username=data["user"])
        return ret


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=20)
    new_password = serializers.CharField(max_length=20)

    def validate_old_password(self, value):
        """
        Check that the blog post is about Django.
        """
        request = self.context["request"]
        user = request.user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码输入错误！")
        return value
