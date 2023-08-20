from django.db import models
from django.contrib.auth.models import User


class Userinfo(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    upvotes_obtained = models.IntegerField(default=0)