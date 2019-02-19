from rest_framework import serializers

from rest_api.models.Model import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Announcement
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True },
            'create_time': {'read_only': True },
        }


class AnnouncementListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Announcement
        exclude = ('content',)
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True },
            'create_time': {'read_only': True },
        }