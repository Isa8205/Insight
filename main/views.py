import http
import json
import os
import re
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Insight import settings
from main.forms import ArticleForm, SignupForm, UserLoginForm
from main.models import ArticleDislikes, ArticleSaves, ArticleViews, Articles, ArticleComments, ArticleLikes, Users


# Create your views here.
def index(request):
    articles = Articles.objects.all()
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

            messages.success(request, f'Account created for {username}! You can now log in.')

            return redirect('login')
        
        else:
            messages.error(request, 'Signup failed. Please check your input and try again.')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


@csrf_protect
def check_username(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    username = data.get('username')

    if not re.match(r'^[\w\-.]+$', username):
        response = {"status": "Invalid", "message": "Username can only contain letters, numbers, underscores, and hyphens."}

    elif not re.match(r'^(?!con$|prn$|aux$|nul$|com[1-9]$|lpt[1-9]$)[\w\-.]+$', username, re.IGNORECASE):

        response = {"status": "Invalid", "message": "Such usernames are not allowed."}
    else:
        user_exists = Users.objects.filter(username=username).exists()

        if user_exists:
            response = {"status": "Unavailable", "message": "Username already in use."}
        else:
            response = {"status": "Available", "message": "Username available."}

    return JsonResponse(response)

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                
                # Success message after login
                messages.success(request, f'Welcome, {username}! You have successfully logged in.')

                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                return redirect('index')
            else:
                # Error message for authentication failure
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            # Error message for form validation failure
            messages.error(request, 'Invalid username or password. Please try again.')

    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})




def logout(request):
    request.session.flush()
    return redirect('index')

@login_required
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
            author_name = Users.objects.get(username = request.user.username)
            article.author = author_name
            article.cover_image = new_cover_img_name
            article.save()

            return render(request, 'upload.html', {'message': 'Upload successful', 'form': ArticleForm()})
        else:
            message = 'Upload failed'
            error = form.errors

            return render(request, 'upload.html', {'form': form, 'message': message, 'error': error})

    return render(request, 'upload.html', {'form': ArticleForm()})

@csrf_protect
def update_view_count(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    articleid =int(data.get('articleId'))
    author = Users.objects.get(username = data.get('author'))
    article = Articles.objects.get(id = articleid)

    view = ArticleViews()
    view.author = author
    view.article = article
    view.save()

    viewcount = ArticleViews.objects.filter(article = article).count()

    return JsonResponse({"status": "Success", "viewcount": viewcount})

@csrf_protect
def update_like_count(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    author = Users.objects.get(username = data.get('author'))
    articleid =int(data.get('articleId'))
    action = data.get('action')
    article = Articles.objects.get(id = articleid)

    if action == 'Add':
        like = ArticleLikes()
        like.author = author
        like.article = article
        like.save()
        status = 'Added'
    else:
        ArticleLikes.objects.filter(author = author, article_id = article).delete()
        status = 'Removed'    
    
    likecount = ArticleLikes.objects.filter(article_id = article).count()

    return JsonResponse({"status": status, 'likecount': likecount})

@csrf_protect
def update_dislike_count(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    author = Users.objects.get(username = data.get('author'))
    articleid =int(data.get('articleId'))
    action = data.get('action')
    article = Articles.objects.get(id = articleid)
    print(data)

    if action == 'Add':
        dislike = ArticleDislikes()
        dislike.author = author
        dislike.article = article
        dislike.save()
        status = 'Added'
    else:
        ArticleDislikes.objects.filter(author = author, article_id = article).delete()
        status = 'Removed'    
    
    dislikecount = ArticleDislikes.objects.filter(article_id = article).count()

    return JsonResponse({"status": status, 'dislikecount': dislikecount})

@csrf_protect
def update_comment_count(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        author = Users.objects.get(username = data.get('author'))
        articleid = int(data.get('articleId'))
        article = Articles.objects.get(id = articleid)
        content = data.get('content')

        comment = ArticleComments()
        comment.author = author
        comment.article = article
        comment.content = content
        comment.save()

        comment_count = ArticleComments.objects.filter(article_id = article).count()

        return JsonResponse({'status': 'Success', 'commentcount': comment_count})        

@csrf_protect
def update_save_count(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    author = Users.objects.get(username = data.get('author'))
    articleid =int(data.get('articleId'))
    action = data.get('action')
    article = Articles.objects.get(id = articleid)

    if action == 'Add':
        bookmark = ArticleSaves()
        bookmark.author = author
        bookmark.article = article
        bookmark.save()
        status = 'Added'
    else:
        ArticleSaves.objects.filter(author = author, article_id = article).delete()
        status = 'Removed'
    
    savecount = ArticleSaves.objects.filter(article_id = article).count()

    return JsonResponse({"status": status, 'savecount': savecount})

@login_required
def single_article(request, article_id):
    article = get_object_or_404(Articles, id=article_id)

    views = ArticleViews.objects.filter(article_id = article)
    view_count = ArticleViews.objects.filter(article_id = article.id).count()
    viewed = ArticleViews.objects.filter(article_id = article.id, author = request.user.id).exists()

    comments = ArticleComments.objects.filter(article_id = article.id)
    commetnt_count = ArticleComments.objects.filter(article_id = article.id).count()
    commented = ArticleComments.objects.filter(article_id = article.id, author = request.user.id).exists()

    likes = ArticleLikes.objects.filter(article_id = article)
    dislikes = ArticleDislikes.objects.filter(article_id = article)
    like_count = ArticleLikes.objects.filter(article_id = article.id).count()
    dislike_count = ArticleDislikes.objects.filter(article_id = article.id).count()
    liked = ArticleLikes.objects.filter(article_id = article.id, author = request.user.id).exists()
    disliked = ArticleDislikes.objects.filter(article_id = article.id, author = request.user.id).exists()

    saves = ArticleSaves.objects.filter(article_id = article)
    save_count = ArticleSaves.objects.filter(article_id = article.id).count()
    saved = ArticleSaves.objects.filter(article_id = article.id, author = request.user.id).exists()

    reactions = {
        'views': views,
        'view_count': view_count,
        'viewed': viewed,
        'likes': likes,
        'like_count': like_count,
        'liked': liked,
        'dislikes': dislikes,
        'dislike_count': dislike_count,
        'disliked': disliked,
        'comments': comments,
        'comment_count': commetnt_count,
        'commented': commented,
        'saves': saves,
        'save_count': save_count,
        'saved': saved,
    }

    context = {
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

