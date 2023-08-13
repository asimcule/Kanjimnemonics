from django.forms import ModelForm
from .models import Post


class Postform(ModelForm):
    class Meta:
        model = Post
        fields = ['kanji', 'mnemonic']

