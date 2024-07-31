from django.shortcuts import render, redirect
from .models import *
from blog.forms import SignUpForm
from .forms import *
from blog.views import get_category
# Create your views here.


def gallery(request):
    photos = Photo.objects.all()
    sign_up_form = SignUpForm()
    context = {'photos': photos, 'sign_up_form': sign_up_form}
    context.update(get_category())
    return render(request, 'gallery/index.html', context)

def uploads(request):
    if request.method == 'POST':
        imageForm = PhotoForm(request.POST, request.FILES)
        if imageForm.is_valid():
            imageForm.save()
            
            return redirect('gallery')
    
    sign_up_form = SignUpForm()
    imageForm = PhotoForm()
    context = {'imageForm': imageForm, 'sign_up_form': sign_up_form}
    context.update(get_category())
    return render(request, 'gallery/uploads.html', context)