from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ExtraCreateFieldMixin():
    """
    混入类
    """
    create_user = models.ForeignKey(User,
                                    related_name="trainings_created",
                                    on_delete=models.CASCADE)
    create_time = models.DateTimeField()


class Training(models.Model, ExtraCreateFieldMixin):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ManyToManyField(User, related_name="trainings")


class Stage(models.Model, ExtraCreateFieldMixin):
    name = models.CharField(max_length=50)
    training = models.ForeignKey(Training, related_name="stages", on_delete=models.CASCADE)
    description = models.CharField(max_length=500)


class Contest(models.Model, ExtraCreateFieldMixin):
    name = models.CharField(max_length=50)
    training = models.ForeignKey(Training, related_name="contests", on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, related_name="stages", on_delete=
                              models.CASCADE)
    description = models.CharField(max_length=500)



