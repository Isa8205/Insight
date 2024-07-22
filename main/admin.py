from django.contrib import admin

from main.models import Reviews, Articles, Comments, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Articles)
admin.site.register(Comments)
admin.site.register(Reviews)
