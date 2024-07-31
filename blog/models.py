from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='photos', null=True, blank=True)  
    country = models.CharField(max_length=50, verbose_name='Country')  
    bio = models.TextField(verbose_name='About Me')
    
    def __str__(self):
        return f'{self.user.username}'
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'  
  
     
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='category_name')

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    
    name = models.CharField(max_length=30, verbose_name='tag_name')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='Post Title')
    image = models.ImageField(upload_to='photos', blank=True, null=True, verbose_name='Preview image')
    content = models.TextField(verbose_name='content')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='publish_date')
    last_modified = models.DateTimeField(auto_created=True, verbose_name='last_modified', null=True, blank=True)
    first_post_image = models.ImageField(upload_to='photos', blank=True, null=True, verbose_name='First Post Image')
    second_post_image = models.ImageField(upload_to='photos', blank=True, null=True, verbose_name='Second Post Image')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='author', related_name='posts', null=True)
    tags = models.ManyToManyField(Tag, verbose_name='tags', related_name='posts')
    likes = models.ManyToManyField(User, related_name='blog_posts', verbose_name='likes')

    def count_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
  
    
class Comment(models.Model):
    
    
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='publish_date')
    last_modified = models.DateTimeField(auto_created=True, verbose_name='last_modified', null=True)
    content = models.TextField(verbose_name='text')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', related_name='comments', null=True)
    
    def __str__(self):
        return f'comment by {self.user.username} on {self.post.title}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f'{self.email}'
    
    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
        

