from rest_framework import serializers

from django.contrib.auth import get_user_model

from rest_api.models.User import UserProfile, UserOJAccount

User = get_user_model()

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user', 'username', "id")


class RegisterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    def create(self, validated_data):
        user = User()
        user.username = validated_data["username"]
        user.set_password(validated_data["password"])
        user.save()
        profile = validated_data.get("profile", None)
        if profile:
            user_profile = UserProfile()
            user_profile.username = validated_data["username"]
            user_profile.email = profile["email"]
            user_profile.qq = profile["qq"]
            user_profile.phone = profile["phone"]
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


