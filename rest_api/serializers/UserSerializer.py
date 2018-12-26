from collections import OrderedDict

from rest_framework import serializers

from django.contrib.auth import get_user_model

from rest_api.models.User import UserProfile, Role

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class SessionSerializer(serializers.ModelSerializer):
    nick = serializers.CharField(source="profile.nick", read_only=True)

    class Meta:
        model = User
        fields = ('username', 'nick')


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
            'is_confirm': {'read_only': True}
            # 'email': {'read_only': False},
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
        user = User.objects.get(username=validated_data["username"])
        expected_role = Role.objects.get(identifier=validated_data["identifier"].upper())
        if expected_role not in user.roles.all():
            user.roles.add(expected_role)
        return user


class UserManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'nick', 'class_name')
        extra_kwargs = {
            "id": {
                "read_only": True
            }
        }


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
