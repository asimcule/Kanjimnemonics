from django.db import models

# Create your models here.
class Kanji(models.Model):
    unicode = models.IntegerField()
    strokes = models.IntegerField()