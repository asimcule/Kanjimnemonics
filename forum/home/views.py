from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
from .models import Kanji

# Create your views here.
def home(request):
    if request.method == 'POST':
        try:
            kanji = request.POST['kanji']
            try:
                kanji = Kanji.objects.filter(kanji=kanji).values()
                # print(kanji[0]['unicode'])
                character = kanji[0]['kanji']
                stroke_count = kanji[0]['stroke_count']
                grade = kanji[0]['grade']
                frequency = kanji[0]['frequency']
                grade = kanji[0]['grade']
                jlpt = kanji[0]['jlpt']            
                return render(request, 'home/index.html', {'stroke_count': stroke_count, "grade": grade, "frequency": frequency, "kanji": character, "jlpt": jlpt})
            except IndexError as e:
                print(e)
                return render(request, 'home/index.html')
        except TypeError:
            return render(request, 'home/index.html')
        
    else:
        return render(request, 'home/index.html')