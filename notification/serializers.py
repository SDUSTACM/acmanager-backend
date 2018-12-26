from collections import OrderedDict

from rest_framework import serializers
from notification.models import Notification, NotificationBase, NotificationOperatorStatus
from django.contrib.auth import get_user_model

User = get_user_model()
class NotificationBaseSerializer(serializers.ModelSerializer):
    from_user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    class Meta:
        model = NotificationBase
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    to_user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    notification = NotificationBaseSerializer()
    class Meta:
        model = Notification
        # field = ('id', 'from_user', 'verb', 'object',
        #          'description', 'timestramp', 'to_user')
        fields = ('id', 'to_user', 'notification', 'is_read')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        id = ret.pop("id")
        notification = ret.pop("notification")
        base_id = notification.pop("id")
        return OrderedDict(id=id, base_id=base_id, **notification, **ret)


class NotificationCreateSerializer(serializers.Serializer):
    to_user = serializers.ListField(
        child=serializers.CharField(max_length=20)
    )
    notification = NotificationBaseSerializer()

    def create(self, validated_data):
        notification_base_data = validated_data.pop("notification")
        notification_base_data = NotificationBase.objects.create(**notification_base_data)
        notifications = []
        for username in validated_data.pop("to_user"):
            notification = Notification.objects.create(notification=notification_base_data, **validated_data, to_user=User.objects.get(username=username))
            notifications.append(notification)
        return notifications

    def to_representation(self, instance):
        users = [item.to_user.username for item in instance]
        return {"notification": self.fields["notification"].to_representation(instance[0].notification),
                "to_user": users
        }

class NotificationOperatorStatusSerializer(serializers.ModelSerializer):
    # status = serializers.CharField(max_length=20)

    class Meta:
        model = NotificationOperatorStatus
        fields = ('status', 'operator_time')
        extra_kwargs = {
            'operator_time': {'read_only': True}
        }

    def save(self, **kwargs):
        notification = NotificationOperatorStatus.objects.filter(notification=kwargs.get("notification"))
        if notification.exists():
            return notification.update(**self.validated_data)
        else:
            return NotificationOperatorStatus.objects.create(notification=kwargs.get("notification"), **self.validated_data)
