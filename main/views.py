import http
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db import connection
from django.contrib.auth import authenticate, login

from Insight import settings
from main.forms import ArticleForm, LoginForm, SignupForm
from main.models import Articles, Users


# Create your views here.
def index(request):
    articles = Articles.objects.extra(select={'profile_name': 'SELECT profile FROM main_users WHERE username = author', 'user_id':'SELECT id from main_users WHERE username = author'})
    session_data = {}
    session_data['username'] = request.session.get('username', None)
    session_data['name'] = request.session.get('name', None)
    # session_data['name'] = session_data.get('profile', None)

    context = {
        'session_data': session_data.values(),
        'data': articles,
        'MEDIA_URL': settings.MEDIA_URL
    }

    return render(request, 'index.html', context)


@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            profile_image = request.FILES['profile']
            profile_name = profile_image.name
            print(f'Profile image name: {profile_name}')

            new_image_name = f'profiles/{username}.png'
            with open(f'media/{new_image_name}', 'wb+') as destination:
                for chunk in profile_image.chunks():
                    destination.write(chunk)

            user = form.save(commit=False)
            user.profile = new_image_name
            user.save()

            context = {
                'message': 'Signup successful',
                'form': SignupForm()
            }
            return render(request, 'signup.html', context)
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


@csrf_protect
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate user against your custom user model

            user = Users.objects.get(username=username)

            print(user)

            if user is not None:
                # Login the user if authentication succeeds
                # login(request, user)
                request.session['username'] = user.username
                request.session['name'] = user.full_name
                request.session['profile'] = user.profile.name
                return redirect('index')
            else:
                # Handle authentication failure
                context = {
                    'message': "Authentication Failed!",
                    'form': form  # Pass the validated form back to the template
                }
                return render(request, 'login.html', context)
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.flush()
    return redirect('index')


@csrf_protect
def upload(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'upload.html', {'message': 'Upload successful'})
        else:
            form = ArticleForm()

    else:
        form = ArticleForm()

    return render(request, 'upload.html', {'form': form})


def single_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)

    context = {
        'data': user,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'account.html', context)

def single_page(request, article_id):
    return render(request, 'page.html')


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


def delete_session(request):
    try:
        del request.session['username']
    except KeyError:
        print('There was no session')
    return redirect('index')
