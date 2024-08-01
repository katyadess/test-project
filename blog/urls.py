from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .views import MyLogoutView, MyPasswordChangeView, MyPasswordResetDoneView, MyLoginView
from .forms import *


urlpatterns = [
    path('', views.index, name='index'),
    path('post/id=<int:id>', views.post, name='post'),
    path('contact', views.contact, name='contact'),
    path('services', views.services, name='services'),
    path('about', views.about, name='about'), 
    path('category/category=<str:name>', views.category, name='category'),
    path('search', views.search, name='search'),
    path('postform', views.create_post, name='postform'),
    path('tag/tag=<str:name>', views.tag, name='tag'),
    path('login', MyLoginView.as_view(form_class=CustomLoginForm), name='blog_login'),
    path('logout', MyLogoutView.as_view(), name='blog_logout'),
    path('profile', views.profile, name='profile'),
    path('register', views.register_user, name='register'),
    path('edit', views.edit_profile, name='edit'),
    path('password_change', MyPasswordChangeView.as_view(form_class=CustomChangePasswordForm), name='change_password'),
    path('password_change/done', MyPasswordResetDoneView.as_view(), name='change_password_done'),
    path('create_profile', views.create_profile, name='create_profile'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('edit_user_profile', views.edit_user_profile, name='edit_user_profile'),
    path('delete_user_profile', views.delete_user_profile, name='delete_user_profile'),
    path('edit_post/<int:id>', views.edit_post, name='edit_post'),
    path('delete_post/<int:id>', views.delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('like_post/<int:id>', views.like_post, name='like_post'),

]
