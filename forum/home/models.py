from django.db import models
from usermanagement.models import Userinfo
from django.contrib.auth.models import User

# Create your models here.
class Kanji(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    kanji = models.TextField(max_length=20, null=False)
    grade = models.IntegerField(null = True)
    stroke_count = models.IntegerField(null=True)
    frequency = models.IntegerField(null=True)
    jlpt = models.IntegerField(null=True)


class Onyomi(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    kanji_key = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    character = models.TextField(max_length=20, null = True)


class Kunyoumi(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    kanji_key = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    character = models.TextField(max_length=20, null = True)


class Meanings(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    kanji_key = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    character = models.TextField(max_length=100, null = True)


class Post(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    kanji = models.TextField(max_length=1, null=False)
    mnemonic = models.TextField(max_length=500, null=False)
    created = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)


class Likes(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)



