from django.urls import include, path

from Insight import settings
from main import views

urlpatterns = [
    path('signup/', view=views.signup, name='signup'),
    path('upload/', view= views.upload, name = 'upload'),
    path('login', view=views.user_login, name = 'login'),
    path('account/details/<int:user_id>/', views.single_user, name='user_account'),
    path('articles/content/<int:article_id>', views.single_article, name='page'),
    path('check_username/', views.check_username, name='check_username'),
    path('articles/remove/<int:article_id>', views.del_article, name='del_article'),
    path('add_article_views/', views.update_view_count, name='article_view_count'),
    path('add_article_likes', views.update_like_count, name='article_like_count'),
    path('add_article_dislikes', views.update_dislike_count, name='article_dislike_count'),
    path('add_article_comments', views.update_comment_count, name='article_comment_count'),
    path('add_article_saves', views.update_save_count, name='article_save_count')
]