from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import *
from .forms import *
from .cart import *
from django.contrib import messages


# Create your views here.


def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddForm(request.POST, stock=product.stock)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        existing_quantity = cart.get_total_quantity(product_id)
        total_quantity = existing_quantity + quantity
        
        if total_quantity > product.stock:
            return redirect('shop:product_detail', id=product.id, slug=product.slug)
        
        cart.add(product=product, quantity=quantity, update_quantity=cd['update'])
        return redirect('cart:cart_details')

def cart_details(request):
    cart = Cart(request) 
    out_of_stock = False
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        quantity = int(request.POST.get('quantity'))

        if quantity > product.stock:
            return redirect('cart:cart_details')

        
        cart.add(product=product, quantity=quantity, update_quantity=True)
        return redirect('cart:cart_details')

    for item in cart:
        if item['product'].stock == 0:
            out_of_stock = True
    
    return render(request, 'cart/detail.html', {'cart': cart, 'out_of_stock': out_of_stock})

def remove(request, product_id):
    
    cart = Cart(request)
    
    
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    if len(cart) == 0:
        return redirect('shop:product_list')
    
    next_url = request.GET.get('next', 'cart:cart_details')
    return redirect(next_url)