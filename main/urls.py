from django.urls import include, path

from Insight import settings
from main import views

urlpatterns = [
    path('signup/', view=views.signup, name='signup'),
    path('upload/', view= views.upload, name = 'upload'),
    path('login', view=views.user_login, name = 'login'),
    path('account/details/<int:user_id>/', views.single_user, name='user_account'),
    path('articles/content/<int:article_id>', views.single_page, name='page'),
    path('check_username/', views.check_username, name='check_username'),
]