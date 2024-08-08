from django.contrib import admin

from main.models import Articles, Comments, SiteReviews, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Articles)
admin.site.register(Comments)
admin.site.register(SiteReviews)
