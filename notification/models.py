from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class NotificationBase(models.Model):
    # choices = (
    #     ()
    # )
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(max_length=20, null=False)
    object = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=100, null=True)
    timestramp = models.DateTimeField(default=datetime.now())


class Notification(models.Model):
    notification = models.ForeignKey(NotificationBase, on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)



class NotificationOperatorStatus(models.Model):
    notification = models.OneToOneField(NotificationBase, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    operator_time = models.DateTimeField(default=datetime.now())