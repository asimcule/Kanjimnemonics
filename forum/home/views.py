from django.shortcuts import render
from .form import Postform
from django.shortcuts import render, HttpResponse, redirect
from .models import Kanji, Onyomi, Kunyoumi, Meanings, Post, Likes
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import logging


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
            context_dictionary = {
                'form': form
            }
            return render(request, 'home/post.html', context_dictionary)
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
                context_dictionary = {
                    "kanji":kanji, 
                    "onyomi":onyomi, 
                    "kunyoumi":kunyoumi, 
                    "meanings":meanings
                }
                return render(request, 'home/search.html', context_dictionary)
            except IndexError as e:
                logging.error(e)
                return render(request, 'home/search.html')
        except TypeError as e:
            print(e)
            return render(request, 'home/search.html') 
    else:
        return render(request, 'home/search.html')


def homepage(request):
    display_data = []
    posts = get_posts_by_creation()
    for post in posts:
        # Use this kanji_id to query all associated data
        kanji = Kanji.objects.get(kanji=post.kanji)
        display_data.append({'post_id': post.id,
                             'kanji': post.kanji, 
                             'onyomi':[a.character for a in Onyomi.objects.filter(kanji_key_id=kanji.id)], 
                             'meanings':[a.character for a in Meanings.objects.filter(kanji_key_id=kanji.id)], 
                             'kunyoumi': [a.character for a in Kunyoumi.objects.filter(kanji_key_id=kanji.id)], 
                             'stroke_count':kanji.stroke_count, 
                             'mnemonic':post.mnemonic, 
                             'posted_by':post.poster_id,
                             'upvotes':post.upvotes})
    if request.user.is_authenticated:
        return render(request, 'home/homepage.html', {'display_data': display_data, "authenticated": True, "user": request.user})
    else:
        return render(request, 'home/homepage.html', {'display_data': display_data, "authenticated": False})
        

def update_likes(request):
    if request.user.is_authenticated:
        user_id = User.objects.get(username=request.user)
        post_id = Post.objects.get(id=request.POST['postid'][0])
        is_liked = Likes.objects.filter(user=user_id.id, post=post_id.id)
        if is_liked:
            # If the user has already liked a particular post
            print("Already Liked!")
            like_update = Likes.objects.get(user=user_id, post=post_id)
            like_update.delete ()
            post = Post.objects.get(id=post_id.id)
            post.upvotes -= 1
            post.save()
            return JsonResponse({"upvotes": post.upvotes})
        else:
            # If the user is liking the particular post for the first time
            like_update = Likes(user=user_id, post=post_id)
            like_update.save()
            post = Post.objects.get(id=int(request.POST['postid'][0]))
            post.upvotes += 1
            post.save()
            return JsonResponse({"upvotes": post.upvotes})
    else:
        return JsonResponse({})


def get_posts_by_creation():
    """Queries posts by filtering with created date

    Returns:
        posts: Returns an objects containing all post data
    """
    posts = Post.objects.all().order_by('-created')
    return posts


def get_posts_by_upvotes():
    pass