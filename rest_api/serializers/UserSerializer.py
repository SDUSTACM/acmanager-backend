from rest_framework import serializers

from django.contrib.auth import get_user_model

from rest_api.models.User import UserProfile, UserOJAccount, Role

User = get_user_model()

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user', 'username', "id")
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'phone': {'required': False},
            'qq': {'required': False},
            'nick': {'required': False},
        }

class RegisterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    def create(self, validated_data):
        user = User()
        user.username = validated_data["username"]
        user.set_password(validated_data["password"])
        user.save()
        profile = validated_data.get("profile", None)
        user_profile = UserProfile()
        user_profile.username = validated_data["username"]
        user_profile.nick = validated_data["username"]
        if profile:
            user_profile.email = profile.get("email", None)
            user_profile.qq = profile.get("qq", None)
            user_profile.phone = profile.get("phone", None)
            user_profile.nick = profile.get("nick", validated_data["username"])
        user_profile.user = user
        user_profile.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'profile')


class UserOJAccountListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books = [UserOJAccount(**item) for item in validated_data]
        return UserOJAccount.objects.bulk_create(books)


class UserOJAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOJAccount
        fields = '__all__'
        list_serializer_class = UserOJAccountListSerializer
        extra_kwargs = {'oj_password': {'required': False}}


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)

    def create(self, validated_data):
        user = User.objects.get(username=validated_data["username"])
        expected_role = Role.objects.get(identifier=Role.ROLE_IDENTIFIER_TYPE.CONFIRM)
        if expected_role not in user.roles.all():
            user.roles.add(expected_role)
        return user