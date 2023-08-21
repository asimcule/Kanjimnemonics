from django.shortcuts import render
from .form import Postform
from django.shortcuts import render, HttpResponse, redirect
from .models import Kanji, Onyomi, Kunyoumi, Meanings, Post, Likes
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import logging

# Create your views here.
@login_required(login_url='login')
def post(request):
    form = Postform()
    if request.method == 'POST':
        username = request.user
        user_id = User.objects.get(username=username)
        input_kanji = request.POST['kanji']
        input_mnemonic = request.POST['mnemonic']
        kanji = Kanji.objects.filter(kanji=input_kanji).values()
        print(user_id)
        if kanji:
            # Means the kanji is valid and available in the master kanji database
            post = Post(poster_id=user_id, kanji=input_kanji, mnemonic=input_mnemonic)
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
                kanji = Kanji.objects.get(kanji=kanji)
                onyomi = Onyomi.objects.filter(kanji_key_id=kanji.id)
                kunyoumi = Kunyoumi.objects.filter(kanji_key_id=kanji.id)
                meanings = Meanings.objects.filter(kanji_key_id=kanji.id)
                print(onyomi)
                return render(request, 'home/search.html', {"kanji":kanji, "onyomi":onyomi, "kunyoumi":kunyoumi, "meanings":meanings})
            except IndexError as e:
                logging.error(e)
                return render(request, 'home/search.html')
        except TypeError as e:
            print(e)
            return render(request, 'home/search.html') 
    else:
        return render(request, 'home/search.html')
    

def search_dummy(request):
    if request.method == 'POST':
        try:
            kanji = request.POST['kanji']
            try:
                kanji = Kanji.objects.filter(kanji=kanji).values()
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
                logging.error(e)
                return render(request, 'home/search.html')
        
        except TypeError:
            return render(request, 'home/search.html')
        
    else:
        return render(request, 'home/search.html')


def homepage(request):
    display_data = get_posts()
    if request.user.is_authenticated:
        return render(request, 'home/homepage.html', {'display_data': display_data, "authenticated": True, "user": request.user})
    else:
        return render(request, 'home/homepage.html', {'display_data': display_data, "authenticated": False})
        

@login_required(login_url='login')
def update_likes(request):
    if request.user.is_authenticated:
        user_id = User.objects.get(username=request.user)
        post_id = Post.objects.get(id=request.POST['postid'][0])
        is_liked = Likes.objects.filter(user=user_id.id, post=post_id.id)
        if is_liked:
            print("Already Liked!")
            like_update = Likes.objects.get(user=user_id, post=post_id)
            like_update.delete ()
            post = Post.objects.get(id=post_id.id)
            post.upvotes -= 1
            post.save()
            return JsonResponse({"upvotes": post.upvotes})
        
        else:
            like_update = Likes(user=user_id, post=post_id)
            like_update.save()
            post = Post.objects.get(id=int(request.POST['postid'][0]))
            post.upvotes += 1
            post.save()
            return JsonResponse({"upvotes": post.upvotes})
    else:
        return redirect('login')


def get_posts():
    posts = Post.objects.all().order_by('-created')
    return posts


def get_posts_by_upvotes():
    pass