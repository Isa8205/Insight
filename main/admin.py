from django.contrib import admin

from main.models import Articles, ArticleComments, SiteReviews, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Articles)
admin.site.register(ArticleComments)
admin.site.register(SiteReviews)
