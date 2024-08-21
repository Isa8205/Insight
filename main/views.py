import http
import json
import os
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db import connection
from django.contrib.auth import authenticate, login

from Insight import settings
from main.forms import ArticleForm, SignupForm, UserLoginForm
from main.models import ArticleDislikes, ArticleSaves, ArticleViews, Articles, ArticleComments, ArticleLikes, Users


# Create your views here.
def index(request):
    articles = Articles.objects.extra(select={'profile_name': 'SELECT profile FROM main_users WHERE username = author', 'author_id':'SELECT id from main_users WHERE username = author'})
    context = {
        'articles': articles,
        'MEDIA_URL': settings.MEDIA_URL
    }

    return render(request, 'index.html', context)


@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')

            if request.FILES:
                profile_image = request.FILES['profile']

                new_image_name = f'profiles/{username}.png'
                with open(f'media/{new_image_name}', 'wb+') as destination:
                    for chunk in profile_image.chunks():
                        destination.write(chunk)
                        
            else:
                new_image_name = "profiles/avatar1.png"

            user = form.save(commit=False)
            user.profile = new_image_name
            user.save()

            return redirect('login')
        
        else:
            print(form.errors)
            message = "Signup failed"

            return render(request, 'signup.html', {'message': message, 'error': form.errors})

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

@csrf_exempt
def check_username(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    username = data.get('username')

    user_exists = Users.objects.filter(username=username).exists()

    if user_exists:
        response = {"status": "Unavailable","message": "Username already in use"}
    else:
        response = {"status": "Available","message": "Username available"}

    return JsonResponse(response)


@csrf_protect
def user_login(request):
    err_msg = None
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)      

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                err_msg = 'Authentication failed'
        else:
            error = form.errors
            return render(request, 'login.html', {'message': err_msg, 'error': error})

    else:
        form = UserLoginForm()

    
    return render(request, 'login.html', {'form':form, 'msg':err_msg})



def logout(request):
    request.session.flush()
    return redirect('index')

@csrf_protect
def upload(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            
            cover_img = request.FILES['cover_image']

            new_cover_img_name = f'Articles/cover_images/{title}.png'
            with open(f'media/{new_cover_img_name}', 'wb+') as destination:
                for chunk in cover_img.chunks():
                    destination.write(chunk)
                    
            article = form.save(commit=False)
            author_name = request.user.username
            article.author = author_name
            article.cover_image = new_cover_img_name
            article.save()

            return render(request, 'upload.html', {'message': 'Upload successful', 'form': ArticleForm()})
        else:
            message = 'Upload failed'
            error = form.errors

            return render(request, 'upload.html', {'form': form, 'message': message, 'error': error})

    return render(request, 'upload.html', {'form': ArticleForm()})

@csrf_exempt
def update_view_count(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    author = data.get('author')
    articleid =int(data.get('articleId'))
    article = Articles.objects.get(id = articleid)

    view = ArticleViews()
    view.author = author
    view.article = article
    view.save()

    viewcount = ArticleViews.objects.filter(article = article).count()

    return JsonResponse({"status": "Success", "viewcount": viewcount})

@csrf_exempt
def update_like_count(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    author = data.get('author')
    articleid =int(data.get('articleId'))
    article = Articles.objects.get(id = articleid)

    like = ArticleLikes()
    like.author = author
    like.article_id = article
    like.save()
    
    likecount = ArticleLikes.objects.filter(article_id = article).count()

    return JsonResponse({"status": 'success', 'likecount': likecount})

@csrf_exempt
def update_dislike_count(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    author = data.get('author')
    articleid =int(data.get('articleId'))
    article = Articles.objects.get(id = articleid)

    dislike = ArticleDislikes()
    dislike.author = author
    dislike.article_id = article
    dislike.save()
    
    dislikecount = ArticleDislikes.objects.filter(article_id = article).count()

    return JsonResponse({"status": 'success', 'dislikecount': dislikecount})

@csrf_exempt
def update_comment_count(request):
    return None

@csrf_exempt
def update_save_count(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    author = data.get('author')
    articleid =int(data.get('articleId'))
    article = Articles.objects.get(id = articleid)

    bookmark = ArticleSaves()
    bookmark.author = Users.objects.get(username = author)
    bookmark.article_id = article
    bookmark.save()
    
    dislikecount = ArticleSaves.objects.filter(article_id = article.id).count()

    return JsonResponse({"status": 'success', 'dislikecount': dislikecount})

def single_article(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    author = Users.objects.get(username = article.author)

    views_count = ArticleViews.objects.filter(article_id = article.id).count()
    viewed = ArticleViews.objects.filter(article_id = article.id, author = request.user.username).exists()

    commetnt_count = ArticleComments.objects.filter(article_id = article.id).count()
    commented = ArticleComments.objects.filter(article_id = article.id, author = request.user.username).exists()

    like_count = ArticleLikes.objects.filter(article_id = article.id).count()
    dislike_count = ArticleDislikes.objects.filter(article_id = article.id).count()
    liked = ArticleLikes.objects.filter(article_id = article.id, author = request.user.id).exists()
    disliked = ArticleDislikes.objects.filter(article_id = article.id, author = request.user.id).exists()

    save_count = ArticleSaves.objects.filter(article_id = article.id).count()
    saved = ArticleSaves.objects.filter(article_id = article.id, author = request.user.id).exists()

    reactions = {
        'viewed': viewed,
        'views': views_count,
        'likes': like_count,
        'liked': liked,
        'dislikes': dislike_count,
        'disliked': disliked,
        'comments': commetnt_count,
        'commented': commented,
        'saves': save_count,
        'saved': saved,
    }

    context = {
        'author': author,
        'article': article,
        'reactions':reactions,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'page.html', context)

def del_article(request, article_id):
    article = Articles.objects.get(id=article_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(article.cover_image))
    
    article.delete()
    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect('index')

def single_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)

    context = {
        'data': user,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'account.html', context)


# views.py
# from django.shortcuts import render, redirect
# from django.core.files.storage import FileSystemStorage
# from .forms import MultiFileUploadForm
#
# def upload_files(request):
#     if request.method == 'POST':
#         form = MultiFileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             files = request.FILES.getlist('files')
#             for file in files:
#                 fs = FileSystemStorage()
#                 filename = fs.save(file.name, file)
#                 # Optionally, save the file information to your model/database
#             return redirect('upload_success')
#     else:
#         form = MultiFileUploadForm()
#     return render(request, 'upload.html', {'form': form})

