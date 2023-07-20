from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
from .models import Kanji

# Create your views here.
def home(request):
    if request.method == 'POST':
        unicode = ord(request.POST['kanji'])
        kanji = Kanji.objects.filter(unicode=unicode).values()
        print(kanji[0]['unicode'])
        try:
            strokes = kanji[0]['strokes']
        except IndexError as e:
            print(e)
        return render(request, 'home/index.html', {'strokes': strokes})
        
        # print(chr(kanji[0]['unicode']))

    else:
        return render(request, 'home/index.html')