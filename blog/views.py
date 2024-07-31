from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Q
from django.utils.timezone import now
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.contrib import messages




# Create your views here.


def get_category():
     
     cats = Category.objects.all()
     half = cats.count() // 2
     first_half = cats[:half]
     second_half = cats[half:]
     
     return {'cats1': first_half, 'cats2': second_half}


def category(request, name=None):
     category = get_object_or_404(Category, name=name)
     posts = Post.objects.filter(category=category).order_by('publish_date')
     paginator = Paginator(posts, 3)
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     sign_up_form = SignUpForm()
     context = {'category': category, 'posts': posts, 'sign_up_form': sign_up_form, 'page_obj': page_obj}
     context.update(get_category())
     return render(request, 'blog/index.html', context)

def tag(request, name=None):
     tag = get_object_or_404(Tag, name=name)
     posts = Post.objects.filter(tags=tag).order_by('publish_date')
     paginator = Paginator(posts, 3)
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     sign_up_form = SignUpForm()
     context = {'tag': tag, 'posts': posts, 'sign_up_form': sign_up_form, 'page_obj': page_obj}
     context.update(get_category())
     return render(request, 'blog/index.html', context)


def index(request):

    if request.method == 'POST':
         form = SignUpForm(request.POST)
         if form.is_valid():
              form.save()
              return redirect('index')
    
    
    sign_up_form = SignUpForm()
    posts = Post.objects.all().order_by('publish_date')
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.filter(posts__in=posts)

    context = {'posts': posts, 'tags': tags, 'sign_up_form': sign_up_form, 'page_obj': page_obj}
    context.update(get_category())
    return render(request, 'blog/index.html', context)

def search(request):
     query = request.GET.get('query')
     posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-publish_date')
     sign_up_form = SignUpForm()
     context = {'posts': posts, 'sign_up_form': sign_up_form}
     context.update(get_category())
     return render(request, 'blog/index.html', context)  

@login_required
def create_post(request):
     if request.method == 'POST':
          form = PostForm(request.POST, request.FILES)
          if form.is_valid():
               post = form.save(commit=False)
               user_profile = get_object_or_404(UserProfile, user=request.user)
               post.user = user_profile
               post.save()
               form.save_m2m()
               return redirect('index')
     
     form = PostForm()
     sign_up_form = SignUpForm()
     context = {'form': form, 'sign_up_form': sign_up_form}
     context.update(get_category())
     return render(request, 'blog/create.html', context)
     

def post(request, id=None):
    post = get_object_or_404(Post, pk=id)
    post_comments = post.comments.all().order_by('-publish_date')
    post_likes = post.count_likes()
    if request.method == 'POST':
         form = CommentForm(request.POST)
         if form.is_valid():
              comment = form.save(commit=False)
              comment.post = post
              comment.user = request.user
              comment.save()
              return redirect('post', id = post.id)
     
    form = CommentForm()
    sign_up_form = SignUpForm()
    context = {'post': post, 'comments': post_comments, 'form': form, 'sign_up_form': sign_up_form, 'post_likes': post_likes}
    context.update(get_category())
    return render(request, 'blog/post.html', context)


def edit_post(request, id):
     post = get_object_or_404(Post, pk=id)
     
     if request.method == 'POST':
          form = PostForm(request.POST, request.FILES, instance=post)
          if form.is_valid():
               updated_post = form.save(commit=False)
               updated_post.last_modified = now()
               updated_post.save()
               form.save_m2m()
               return redirect('post', id=post.id)
     
     form = PostForm(instance=post)
     sign_up_form = SignUpForm()
     context = {'form': form, 'sign_up_form': sign_up_form, 'post': post}
     context.update(get_category())
     return render(request, 'blog/edit_post.html', context)


def delete_post(request, id):
     post = get_object_or_404(Post, pk=id)

     if request.method == 'POST':
          if post.user.user == request.user:
               post.delete()
               return redirect('index')
          else:
               messages.error(request, "You are not authorized to delete this post.")
               return redirect('index')


     sign_up_form = SignUpForm()
     context = {'sign_up_form': sign_up_form, 'post': post}
     context.update(get_category())
     return render(request, 'blog/delete_post.html', context)


def like_post(request, id):
     post = get_object_or_404(Post, pk=id)
    
     if request.method == 'POST':
          if request.user in post.likes.all():
               post.likes.remove(request.user)
          
          else:
               post.likes.add(request.user)
           
     return redirect('post', id=post.pk)    
           
 
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = comment.post
    
    if request.method == 'POST':
          if request.user == comment.user or request.user == post.user.user:
               comment.delete()

    return redirect('post', id=post.pk)
  
def contact(request):
     contact_info = {
        'phone': '+1 (234) 567-890',
        'email': 'contact@example.com',
        'address': '1234 Street Name, City, State, ZIP Code'
     }
     
     sign_up_form = SignUpForm()
     context = {'contact_info': contact_info, 'sign_up_form': sign_up_form}
     context.update(get_category())
     return render(request, 'blog/contacts.html', context)
  
def services(request):
     sign_up_form = SignUpForm()
     context = {'sign_up_form': sign_up_form}
     context.update(get_category())
     return render(request, 'blog/services.html', context)

def about(request):
     sign_up_form = SignUpForm()
     context = {'sign_up_form': sign_up_form}
     context.update(get_category())
     return render(request, 'blog/about.html', context)

def register_user(request):
     if request.method == 'POST':
        user_registration = User_Registration(request.POST)
        if user_registration.is_valid():
               user = user_registration.save()
               login(request, user)
               return render(request, 'registration/create_profile.html', context)

     sign_up_form = SignUpForm()
     user_registration = User_Registration()
     context = {'sign_up_form': sign_up_form, 'user_registration': user_registration}
     context.update(get_category())
     return render(request, 'registration/register.html', context)


def edit_profile(request):
     if request.method == 'POST':
          profile_form = EditProfile(request.POST, instance = request.user)
          if profile_form.is_valid():
               profile_form.save()
               return redirect('profile')

     profile_form = EditProfile(instance = request.user)
     sign_up_form = SignUpForm()
     context = {'sign_up_form': sign_up_form, 'profile_form': profile_form}
     context.update(get_category())
     return render(request, 'registration/edit_profile.html', context)


class MyLogoutView(View):
     def get(self, request):
          logout(request)
          return redirect('index')
     
class MyPasswordChangeView(PasswordChangeView):
     template_name = 'registration/change_password.html'
     success_url = reverse_lazy('change_password_done')
     
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sign_up_form'] = SignUpForm()
        context.update(get_category())
        return context
     
class MyPasswordResetDoneView(PasswordResetDoneView):
     template_name = 'registration/change_password_done.html'
     
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sign_up_form'] = SignUpForm()
        context.update(get_category())
        return context
     
def create_profile(request):
     if request.method == 'POST':
          create_profile_form = ProfileForm(request.POST, request.FILES)
          if create_profile_form.is_valid():
               profile = create_profile_form.save(commit=False)
               profile.user = request.user
               profile.save()
               return redirect('user_profile', username=profile.user.username)

     create_profile_form = ProfileForm()
     sign_up_form = SignUpForm()
     context = {'sign_up_form': sign_up_form, 'create_profile_form': create_profile_form}
     context.update(get_category())
     return render(request, 'registration/create_profile.html', context)

     
  
def profile(request):
     
     user = request.user
     sign_up_form = SignUpForm()
     context = {'sign_up_form': sign_up_form, 'user': user}
     context.update(get_category())
     return render(request, 'blog/profile.html', context)


def user_profile(request, username=None):
     
     if not request.user.is_authenticated:
         return redirect('register')
     
     user = get_object_or_404(User, username=username)
     profile = get_object_or_404(UserProfile, user=user)     
     posts = Post.objects.filter(user=profile).order_by('-publish_date')
     comments = Comment.objects.filter(user=user).order_by('-post__publish_date')
     sign_up_form = SignUpForm()
     context = {'sign_up_form': sign_up_form, 'profile': profile, 'posts': posts, 'comments': comments}
     context.update(get_category())
     return render(request, 'blog/user_profile.html', context)

def edit_user_profile(request):
     profile = get_object_or_404(UserProfile, user=request.user)
     
     if request.method == 'POST':
          create_profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
          if create_profile_form.is_valid():
               profile.save()
               return redirect('user_profile', profile.user.username)

     create_profile_form = ProfileForm(instance=profile)
     sign_up_form = SignUpForm()
     context = {'sign_up_form': sign_up_form, 'create_profile_form': create_profile_form}
     context.update(get_category())
     return render(request, 'registration/edit_user_profile.html', context)


def delete_user_profile(request):
     
     profile = get_object_or_404(UserProfile, user=request.user)
     
     if request.method == 'POST':
          profile.delete()     
          return redirect('profile')

     sign_up_form = SignUpForm()
     context = {'sign_up_form': sign_up_form, 'profile': profile}
     context.update(get_category())
     return render(request, 'registration/delete_user_profile.html', context)
