from django.contrib import admin

# Register your models here.

from .models import ListCat, Song, List

admin.site.register(ListCat)
admin.site.register(Song)
admin.site.register(List)