from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
from .models import Kanji

# Create your views here.
def home(request):
    if request.method == 'POST':
        try:
            unicode = ord(request.POST['kanji'])
            try:
                kanji = Kanji.objects.filter(unicode=unicode).values()
                print(kanji[0]['unicode'])
                strokes = kanji[0]['strokes']
                return render(request, 'home/index.html', {'strokes': strokes})
            except IndexError as e:
                print(e)
                return render(request, 'home/index.html')
        except TypeError:
            return render(request, 'home/index.html')
        
    else:
        return render(request, 'home/index.html')