from django.contrib import admin
from .models import Kanji, Onyomi

# Register your models here.
admin.site.register(Kanji)
admin.site.register(Onyomi)