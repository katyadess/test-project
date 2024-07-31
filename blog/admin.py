from django.contrib import admin
from .models import Post, Category, Tag, Comment, Subscriber, UserProfile
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Subscriber)
admin.site.register(UserProfile)
