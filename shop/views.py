from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import *
from cart.cart import Cart
from django.db.models import Q
from blog.forms import EditProfile
from django.urls import reverse
 
def product_list(request, category_slug=None):
    cart = Cart(request)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products, 'cart': cart})

def product_detail(request, id, slug):
    cart = Cart(request)
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    
    category = product.category
    cart_product_form = CartAddForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'cart': cart,
        'category': category,
        'breadcrumbs': [
            {'name': 'Shop', 'url': reverse('shop:product_list')},
            {'name': category.name, 'url': category.get_absolute_url()},
            {'name': product.name}
        ]
    }
    
    return render(request,
                  'shop/product/detail.html', context)
    

def view_or_edit_profile(request):
    
    cart = Cart(request)
    
    if request.method == 'POST':
          profile_form = EditProfile(request.POST, instance = request.user)
          if profile_form.is_valid():
               profile_form.save()
               return redirect('shop:shop_profile')
    
    profile_form = EditProfile(instance=request.user)
    
    return render(request, 'shop/product/profile.html', {'profile_form': profile_form, 'cart': cart})

    
def search(request, category_slug=None):
    cart = Cart(request)
    query = request.GET.get('query')
    products = Product.objects.filter(Q(name__icontains=query))
    category = None
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'products': products, 'cart': cart, 'category': category, 'categories': categories,}
    return render(request, 'shop/product/list.html', context)  
