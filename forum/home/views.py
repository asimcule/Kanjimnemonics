from django.shortcuts import render
from .form import Postform
from django.shortcuts import render, HttpResponse, redirect
from .models import Kanji, Onyomi, Kunyoumi, Meanings, Post
from django.contrib import messages

# Create your views here.
def post(request):
    form = Postform()
    if request.method == 'POST':
        input_kanji = request.POST['kanji']
        input_mnemonic = request.POST['mnemonic']
        kanji = Kanji.objects.filter(kanji=input_kanji).values()
        if kanji:
            # Means the kanji is valid and available in the master kanji database
            post = Post(kanji=input_kanji, mnemonic=input_mnemonic)
            post.save()
        else:
            messages.error(request, "No kanji found")
            return render(request, 'home/post.html', {'form': form})
        return redirect('homepage')

    else:
        return render(request, 'home/post.html', {'form': form})


def search(request):
    if request.method == 'POST':
        try:
            kanji = request.POST['kanji']
            
            try:
                kanji = Kanji.objects.filter(kanji=kanji).values()
                # print(kanji[0]['unicode'])
                id = kanji[0]["id"]
                character = kanji[0]['kanji']
                stroke_count = kanji[0]['stroke_count']
                grade = kanji[0]['grade']
                frequency = kanji[0]['frequency']
                grade = kanji[0]['grade']
                jlpt = kanji[0]['jlpt']
                onyomi_list = []
                kunyoumi_list = []
                meanings_list = []
                onyomi = Onyomi.objects.filter(kanji_key_id=id).values()
                for item in onyomi:
                    onyomi_list.append(item['character'])
                kunyoumi = Kunyoumi.objects.filter(kanji_key_id=id).values()
                for item in kunyoumi:
                    kunyoumi_list.append(item['character'])
                meanings = Meanings.objects.filter(kanji_key_id=id).values()
                for item in meanings:
                    meanings_list.append(item['character'])     
                return render(request, 'home/search.html', {'stroke_count': stroke_count, "grade": grade, "frequency": frequency, "kanji": character, "jlpt": jlpt, "onyomi": onyomi_list, "kunyoumi": kunyoumi_list, "meanings": meanings_list})
            
            except IndexError as e:
                print(e)
                return render(request, 'home/search.html')
        
        except TypeError:
            return render(request, 'home/search.html')
        
    else:
        return render(request, 'home/search.html')


def homepage(request):
    posts = Post.objects.all().order_by('-created').values()
    display_data = []
    print(posts)
    for post in posts:
        input_kanji = post['kanji']
        kanji_info = Kanji.objects.filter(kanji=input_kanji).values()
        print(kanji_info)
        meanings = Meanings.objects.filter(kanji_key_id=kanji_info[0]['id']).values()
        print
        display_data.append({"kanji":input_kanji, "strokes": kanji_info[0]['stroke_count'], "meanings": [a['character'] for a in meanings], "mnemonic":post['mnemonic']})

    return render(request, 'home/homepage.html', {'display_data': display_data})