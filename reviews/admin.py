from django.contrib import admin
from .models import Artist, Genre, Album, Review

admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Review)