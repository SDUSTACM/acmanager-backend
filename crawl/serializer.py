from rest_framework import serializers

from crawl.models import UserOJAccount

class UserOJAccountSerializer(serializers.ModelSerializer):
    class Meta:
        # list_serializer_class = UserOJAccountListSerializer
        model = UserOJAccount
        fields = ('oj_name', 'oj_username', 'oj_password')


class UserOJAccountListSerializer(serializers.ListSerializer):
    child = UserOJAccountSerializer()
    def save(self, **kwargs):
        user_id = kwargs.get("user_id")
        UserOJAccount.objects.filter(user_id=user_id).delete()
        validated_data = [
            dict(list(attrs.items()) + list([("user_id", user_id)]))
            for attrs in self.validated_data
        ]
        for item in validated_data:
            UserOJAccount.objects.create(**item)


