import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Announcement(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=3000)
    user = models.ForeignKey(User, related_name="announcements", on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=datetime.datetime.now())
